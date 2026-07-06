# Module: backend/app/utils/file_manager.py


import shutil
from pathlib import Path


def create_directory(directory: str):

    Path(directory).mkdir(parents=True, exist_ok=True)


def delete_file(file_path: str):

    path = Path(file_path)

    if path.exists():
        path.unlink()


def delete_directory(directory: str):

    path = Path(directory)

    if path.exists():
        shutil.rmtree(path)


def move_file(source: str, destination: str):

    shutil.move(source, destination)


def copy_file(source: str, destination: str):

    shutil.copy2(source, destination)


def rename_file(old_name: str, new_name: str):

    Path(old_name).rename(new_name)


def list_files(directory: str):

    return list(Path(directory).iterdir())