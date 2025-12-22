import subprocess
import os


# Run pacman -Q to get the list of installed packages
def get_pkg_metadata():
    metadata = None

    try:
        metadata = subprocess.run(
            ["pacman", "-Qi"], capture_output=True, text=True, check=True
        )
        metadata = metadata.stdout
    except Exception as e:
        print(f"Error, {e}")

    return metadata


def main():
    pkg_metadata = get_pkg_metadata()
    print(pkg_metadata)


if __name__ == "__main__":
    main()
