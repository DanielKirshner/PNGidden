import sys


MAJOR_VERSION_REQUIRED = 3
MINIMUM_MINOR_VERSION_REQUIRED = 10
REQUIRED_PIP_PACKAGES = ["numpy", "pillow", "rich"]


def check_for_python_version():
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro
    
    if (major < MAJOR_VERSION_REQUIRED or (major == MAJOR_VERSION_REQUIRED and minor < MINIMUM_MINOR_VERSION_REQUIRED)):
        print(
            "You are using an old python version "
            f"[{major}.{minor}.{micro}]\n"
            f"Please update your python to {MAJOR_VERSION_REQUIRED}.{MINIMUM_MINOR_VERSION_REQUIRED}+"
        )
        sys.exit()


if __name__ == '__main__':
    check_for_python_version()

    from PNGidden import run_pngidden
    run_pngidden()
