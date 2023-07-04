from enum import Enum


class LinkType(Enum):
    en = 0
    ru = 1
    en_not_found_status_code = 500
    ru_not_found_status_code = 404


class VideoQuality(Enum):
    _1080 = 1080
    _720 = 720
    _480 = 480
    _360 = 360
