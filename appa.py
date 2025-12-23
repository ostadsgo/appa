import subprocess
import os
from datetime import datetime, timedelta, timezone

# Run pacman -Q to get the list of installed packages
def get_pkgs_metadata() -> str:
    metadata = None

    try:
        metadata = subprocess.run(
            ["pacman", "-Qi"], capture_output=True, text=True, check=True
        )
        metadata = metadata.stdout
    except Exception as e:
        print(f"Error, {e}")

    return metadata


def get_packages(metadata: str) -> list[str]:
    """Extract each package as list."""
    pkgs = metadata.split("\n\n")
    return [pkg for pkg in pkgs if pkg]


def extract_depend_on(value: str) -> list[str]:
    return value.split("  ")


def extract_optional_deps(value: str) -> list[str]:
    return value.split("  ")




def convert_to_data_type(pkg: dict[str, str]):
    pkg_data = {}
    for name, value in pkg.items():
        if name in ["depends on",  "optional deps"]:
            value = value.split("  ")
        elif name in ["build date", "install date"]:
            datetime_format ='%a %d %b %Y %I:%M:%S %p %z'
            value = datetime.strptime(value, datetime_format)

        pkg_data[name] = value
    return pkg_data
        

def parse_package(raw_package: str) -> dict[str, str]:
    """Parse and extract fields of a package."""
    package = {}
    last_name = None
    lines = raw_package.splitlines()
    for line in lines:
        if not line.startswith(" "):
            name, sep, value = line.partition(":")
            name = name.lower().strip()
            value = value.lower().strip()

            package[name] = value
            last_name = name
        else:
            # This is not a field, it is rest of the value that belong to last field's value
            # Which must added to the last field_value.
            value = package[last_name] + "  " + line.strip().lower()
            package.update({last_name: value})

    return package


def parse_packages(packages):
    packages_list = []

    for package in packages:
        pkg = parse_package(package)
        pkg_data = convert_to_data_type(pkg)
        packages_list.append(pkg_data)

    return packages_list

def main():
    metadata = get_pkgs_metadata()
    row_data = get_packages(metadata)
    packages = parse_packages(row_data)
    print(len(packages))

if __name__ == "__main__":
    main()
