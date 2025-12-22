import subprocess
import os


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
    """ Extract each package as list. """
    pkgs = metadata.split("\n\n") 
    return [pkg for pkg in pkgs if pkg]
    


def parse_package(raw_package: str) -> dict[str, str]:
    """ Parse and extract fields of a package. """
    package = {}
    last_name = None
    lines = raw_package.splitlines()
    for line in lines:
        if not line.startswith(' '):
            name, sep, value = line.partition(':')
            name = name.lower()
            value = value.lower()
            package[name] = value
            last_name = name

        else:
            # This is not a field, it is rest of the value that belong to last field's value
            # Which must added to the last field_value.
            print(last_name)
            value = package[last_name] + "  " + line.strip().lower()
            package.update({last_name : value})

    return package

def parse_packages(packages):
    pass

def main():
    metadata = get_pkgs_metadata()
    pkgs = get_packages(metadata)
    pkg = parse_package(pkgs[0])
    for line, val in pkg.items():
        print(line, '--->', val)


if __name__ == "__main__":
    main()
