from enum import Enum


class PyarrSortDirection(str, Enum):
    """Pyarr sort direction"""

    ASC = "ascending"
    DEFAULT = "default"
    DESC = "descending"
