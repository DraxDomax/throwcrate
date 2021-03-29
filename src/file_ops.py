import os
import hashlib
import pathlib


def get_current_catalog(current_dir):
    subdirectories, files_hashes = [], []

    with os.scandir(current_dir) as dir_entry_iterator:
        for entry in dir_entry_iterator:
            if entry.is_dir():
                subdirectories.append(entry.path)
            if entry.is_file():
                files_hashes.append([entry.path, md5(entry.path)])

        for current_dir in list(subdirectories):
            current_subdirectories, current_files_hashes = get_current_catalog(current_dir)
            subdirectories.extend(current_subdirectories)
            files_hashes.extend(current_files_hashes)

        return subdirectories, files_hashes


def get_current_catalog_dictionary(root):
    subdirectories_local, files_hashes_local = get_current_catalog(root)
    result = {
        "subdirectories": remove_root_and_standardize_dir_sep(root, subdirectories_local),
        "files_hashes": remove_root_and_standardize_dir_sep(root, files_hashes_local),
    }
    return result


def md5(file):  # https://stackoverflow.com/a/3431838/3617811
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_root_and_standardize_dir_sep(root, list_of_entries):
    full_root = root + "\\"
    result = []
    for current_entry in list_of_entries:
        if type(current_entry) == list:
            file = current_entry[0].replace(full_root, "/")
            file = file.replace("\\", "/")  # Too lazy to check if method chaining works
            result.append([file, current_entry[1]])
        else:
            folder = current_entry.replace(full_root, "/")
            folder = folder.replace("\\", "/")  # Yeah, this repetition is not the best, either...
            result.append(folder)

    return result


def rmdir(directory):  # https://stackoverflow.com/a/49782093/3617811
    directory = pathlib.Path(directory)
    if directory.exists():  # Not optimal, many checks expected to fail, but will do for now...
        for item in directory.iterdir():
            if item.is_dir():
                rmdir(item)
            else:
                item.unlink()
        directory.rmdir()