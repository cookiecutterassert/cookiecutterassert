import os
from pathlib import Path
from cookiecutterassert.stale_test_folder_cleanup import is_stale_test_folder, delete_stale_test_folders
from unittest.mock import patch

def test_is_stale_test_folder_returns_true_if_folder_only_has_build_folder():
    testFolder = os.path.dirname(os.path.abspath(__file__))
    fixturePath = Path(testFolder).parent.joinpath("example").joinpath("staleTests").joinpath("stale")
    assert is_stale_test_folder(str(fixturePath)) == True

def test_is_stale_test_folder_returns_true_if_folder_has_test_files():
    testFolder = os.path.dirname(os.path.abspath(__file__))
    fixturePath = Path(testFolder).parent.joinpath("example").joinpath("staleTests").joinpath("notstale_tests")
    assert is_stale_test_folder(str(fixturePath)) == False

def test_is_stale_test_folder_returns_true_if_folder_has_other_files():
    testFolder = os.path.dirname(os.path.abspath(__file__))
    fixturePath = Path(testFolder).parent.joinpath("example").joinpath("staleTests").joinpath("notstale_otherfile")
    assert is_stale_test_folder(str(fixturePath)) == False

def test_is_stale_test_folder_returns_true_if_folder_has_build_file():
    testFolder = os.path.dirname(os.path.abspath(__file__))
    fixturePath = Path(testFolder).parent.joinpath("example").joinpath("staleTests").joinpath("notstale_buildfile")
    assert is_stale_test_folder(str(fixturePath)) == False

@patch('shutil.rmtree')
@patch("cookiecutterassert.stale_test_folder_cleanup.print")
def test_deletes_stale_folders(mock_print, mock_rmtree):
    testFolder = os.path.dirname(os.path.abspath(__file__))
    fixturePath = Path(testFolder).parent.joinpath("example").joinpath("staleTests")
    delete_stale_test_folders(str(fixturePath))
    mock_rmtree.assert_called_once_with(str(fixturePath.joinpath('stale')))
    mock_print.assert_called_once_with(f'Deleted stale test folder ${str(fixturePath.joinpath("stale"))}')
