# Standard Libraries
import os
from pathlib import Path
import subprocess
import tempfile as tf

# Dependencies
import numpy as np
import rasterio as rio
from rasterio.control import GroundControlPoint
import pyproj

# Top-Level Imports
import selenography.projections as projections


def apply_gcps(
    src_path: str | os.PathLike,
    prj_path: str | os.PathLike,
    gcps_path: str | os.PathLike,
    gdal_conda_env_name: str = "gdal_only"
) -> None:
    """
    Project the dataset into a coordinate system. Apply GCPs to a raster and
    warp it to georeference the image.

    Parameters
    ----------
    src_path: str | os.PathLike
        Path to the input raster file.
    prj_path: str | os.PathLike
        Path to .prj file with projection information.
    gdal_conda_env_name: str
        Name of the conda environment that has gdal installed.
    """
    src_path = Path(src_path)
    with open(prj_path) as f:
        crs_name = pyproj.Proj(f.read()).crs.name

    with_gcs = tf.NamedTemporaryFile(suffix=".tif")
    with_gcs.close()
    if crs_name == "GCS_Moon_2000":
        _ = projections.gcs_moon_2000(src_path, dst_path=with_gcs.name)
    elif crs_name == "Moon_2000_Equidistant_Cylindrical":
        _ = projections.equidistant_cylindrical_moon(
            src_path, dst_path=with_gcs.name
        )
    else:
        raise ValueError(f"{prj_path} contains an invalid WKT projection.")

    gcps = gcps_from_qgis(with_gcs.name, gcps_path)
    with_gcps = tf.NamedTemporaryFile(suffix=".tif")
    with_gcps.close()
    gdaltrans = gcp_list_to_shell_string(gcps, with_gcs.name, with_gcps.name)

    gcp_path = src_path.with_name(f"{src_path.stem}_gcp.tif")
    gdalwarp = "gdalwarp -r near -tps -t_srs "\
               f"{prj_path} {with_gcps.name} {gcp_path}"

    def run_command_in_conda_env(env_name: str, command_str: str):
        out = subprocess.run(
            f"conda run -n {env_name} {command_str}".split(),
            shell=True, capture_output=True
        )
        print(f"----STDOUT----\n{out.stdout.decode("utf-8")}")
        print(f"----STDERR----\n{out.stderr.decode("utf-8")}")

    run_command_in_conda_env(gdal_conda_env_name, gdaltrans)
    run_command_in_conda_env(gdal_conda_env_name, gdalwarp)


def gcps_from_arcgis(
    src_path: str | os.PathLike,
    points_path: str | os.PathLike
) -> list[GroundControlPoint]:
    """
    Returns a list of GCP objects from reading a .points file returned from
    a hand-georeference in ArcGIS.
    """
    src_path = Path(src_path)
    points_path = Path(points_path)

    gcps_in = np.loadtxt(points_path)
    gcps_out = []
    with rio.open(src_path) as ds:
        for i in range(gcps_in.shape[0]):
            xpixel, ypixel = ds.index(gcps_in[i, 0], gcps_in[i, 1])
            gcps_out.append(GroundControlPoint(
                row=xpixel,
                col=ypixel,
                x=gcps_in[i, 2],
                y=gcps_in[i, 3]
            ))
    return gcps_out


def gcps_from_qgis(
    src_path: str | os.PathLike,
    points_path: str | os.PathLike
) -> list[GroundControlPoint]:
    """
    Returns a list of GCP objects from reading a .points file returned from
    a hand-georeference in ArcGIS.
    """
    src_path = Path(src_path)
    points_path = Path(points_path)

    with open(points_path) as f:
        lines = f.readlines()

    nrow = len(lines) - 2
    gcps_in = np.empty((nrow, 4), dtype=np.float32)
    for n, i in enumerate(lines[2:]):
        row = np.array([float(j) for j in i.split(",")][:4])
        gcps_in[n, :] = row

    gcps_out = []
    with rio.open(src_path) as ds:
        print(f"WIDTH: {ds.width}")
        print(f"HEIGHT: {ds.height}")
        origin_x, pixel_width, _, origin_y, _, pixel_height = \
            ds.transform.to_gdal()

        for i in range(gcps_in.shape[0]):
            xpixel = (gcps_in[i, 2] - origin_x) / pixel_width
            ypixel = (gcps_in[i, 3] - origin_y) / pixel_height
            # xpixel, ypixel = ds.index(gcps_in[i, 0], gcps_in[i, 1])
            gcps_out.append(GroundControlPoint(
                row=ypixel,
                col=xpixel,
                x=gcps_in[i, 0],
                y=gcps_in[i, 1]
            ))
    return gcps_out


def gcp_list_to_shell_string(
    gcp_list: list[GroundControlPoint],
    src: str | os.PathLike,
    dst: str | os.PathLike
) -> str:
    gcp_list_as_strings = [f"{i.col} {i.row} {i.x} {i.y}" for i in gcp_list]
    gcp_str = f"gdal_translate -gcp {' -gcp '.join(gcp_list_as_strings)} "\
              f"{src} {dst}"
    return gcp_str
