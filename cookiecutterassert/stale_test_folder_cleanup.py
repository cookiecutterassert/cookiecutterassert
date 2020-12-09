import os
from pathlib import Path
import shutil

def is_stale_test_folder(folder):
    children = os.listdir(folder)
    if ('build' in children and os.path.isdir(folder+"/build")):
        children.remove('build')
    return len(children) == 0

def delete_stale_test_folders(tests_folder):
    tests_folder_path = Path(tests_folder)
    for child in tests_folder_path.iterdir():
        if child.is_dir() and is_stale_test_folder(str(child)):
            shutil.rmtree(str(child))
            print(f'Deleted stale test folder ${str(child)}')
