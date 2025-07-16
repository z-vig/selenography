# Standard Libraries
import os
from pathlib import Path

# Dependencies
import rasterio as rio

# Top-Level Imports
from selenography import lunar_regional_bounding_boxes as bboxes


def crop_with_bbox(
    src: str | os.PathLike,
    crs: str,
    bbox: tuple[float, float, float, float] | None = None,
    region_name: str | None = None
) -> None:
    """
    Crops image to a defined bounding box.

    Parameters
    ----------
    src: str of Path-Like
        Path to image to crop.
    crs: str
        Coordinate Reference system (either 'gcs' or 'edcm')
    bbox: tuple of floats, optional
        Bounding box coordinates. If None, the region name must be specified.
    region_name: str, optional
        One of the implemented regions of the Moon. See
        `lunar_regional_bounding_boxes.py`. If None, `bbox` must be specified.

    Returns
    -------
    None
    """
    p = Path(src)  # Handles path.

    # Handles bbox values.
    if bbox is None:
        if region_name is None:
            raise ValueError(
                "Must define either a bbox tuple or one of the implemented"
                f"region names: {bboxes.search.keys()}"
            )
        else:
            if crs == 'gcs':
                bbox = bboxes.search_gcs.get(region_name)
            elif crs == 'edcm':
                bbox = bboxes.search_edcm.get(region_name)
            else:
                raise ValueError(f"{crs} is an invalid CRS.")
            save_path = p.with_name(
                f"{p.stem}_{region_name.replace(" ", "_")}.tif"
            )
            if bbox is None:
                raise ValueError(
                    f"{region_name} is invalid. Please choose a valid region:"
                    f"{bboxes.search.keys()}"
                )
    else:
        bbox_str = f"{bbox[0]:.1f}_{bbox[1]:.1f}_{bbox[2]:.1f}_{bbox[3]:.1f}"
        save_path = p.with_name(f"{p.stem}_{bbox_str}.tif")

    # Crops the image.
    with rio.open(p) as ds:
        print(f"Cropping to {bbox}")
        window = rio.windows.from_bounds(*bbox, transform=ds.transform)
        transform = ds.window_transform(window)
        kwargs = ds.meta.copy()
        kwargs.update({
            'height': window.height,
            'width': window.width,
            'transform': transform
        })

        with rio.open(save_path, 'w', **kwargs) as dst:
            for i in range(1, ds.count + 1):
                data = ds.read(i, window=window)
                dst.write(data, i)
