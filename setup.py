import sys
import subprocess
import pkg_resources


MAJOR_VERSION_REQUIRED = 3
MINIMUM_MINOR_VERSION_REQUIRED = 10
REQUIRED_PIP_PACKAGES = {"numpy", "pillow", "rich"}


def check_for_python_version() -> None:
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


def get_missing_pip_packages() -> set:
    current_pip_packages = {pkg.key for pkg in pkg_resources.working_set}
    return REQUIRED_PIP_PACKAGES - current_pip_packages


def install_pip_packages(packages: set) -> None:
    python_path = sys.executable
    try:
        subprocess.check_call([python_path, '-m', 'pip', 'install', *packages], stdout=subprocess.DEVNULL)
    except Exception:
        print("Failed installing pip packages. Abort.")
        sys.exit()


if __name__ == '__main__':
    
    # -------- Verifying python version
    check_for_python_version()

    # -------- Verifying pip packages
    missing_pip_packages = get_missing_pip_packages()
    if(len(missing_pip_packages) > 0):
        print(
            f"You are missing {len(missing_pip_packages)} pip packages."
            "\nDo you want to install them now? [yes/no] -> "
        )
        user_choice = input()
        # -------- Install missing pip packages
        if(user_choice.lower() == 'yes'):
            install_pip_packages(missing_pip_packages)
        else:
            sys.exit()
    
    # -------- All good
    print("Finished setup.\nYou can now run PNGidden.py")
