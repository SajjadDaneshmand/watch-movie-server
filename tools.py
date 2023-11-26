import sys
import os


def os_detector():
    platform = sys.platform
    if platform == 'linux':
        if 'TERMUX_VERSION' in os.environ:
            return 'android'
        return platform
    return platform
