"""
### Selenography

A collection of common selenographic mapping utilities for Python Users.
Package functionalities include:
- Projecting datasets into lunar coordinate systems
- Aligning different satellite datasets to form equal-sized arrays.
- Applying Ground Control Points to an image using a gdal command-line call.
- Image cropping to defined regions of lunar geologic interest.
- Image conversion into common formats such as GeoTiff or ENVI.
"""

from .align_pixels import align_pixels
from .image_conversion import convert_to_gtif, convert_to_8bit_2D
from .crop_with_bbox import crop_with_bbox
from .apply_gcps import (
    apply_gcps, gcps_from_arcgis, gcps_from_qgis, gcp_list_to_shell_string
)

from . import projections
from . import lunar_regional_bounding_boxes

from . import utils

__all__ = [
    "project_to_GCSMoon2000",
    "align_pixels",
    "convert_to_gtif",
    "convert_to_8bit_2D",
    "crop_with_bbox",
    "apply_gcps",
    "gcps_from_arcgis",
    "gcps_from_qgis",
    "gcp_list_to_shell_string",
    "projections",
    "lunar_regional_bounding_boxes",
    "utils"
]
