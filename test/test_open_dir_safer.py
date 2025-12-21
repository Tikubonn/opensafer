
import pytest
import shutil
import opensafer
from pathlib import Path

TEST_DIR = Path("./.test/sample")

def setup_function (func):
  TEST_DIR.mkdir(parents=True, exist_ok=True)

def teardown_function (func):
  shutil.rmtree(TEST_DIR)

def test_open_dir_safer ():

  with opensafer.open_dir_safer(TEST_DIR) as d:
    with open(d.joinpath("sample.txt"), "w") as file:
      assert file.write("123") == 3

  with open(TEST_DIR.joinpath("sample.txt"), "r") as file:
    assert file.read() == "123"

def test_open_dir_safer2 ():

  #存在しないディレクトリを指定した場合の動作確認(shutil.move の挙動により親ディレクトリは自動生成される)

  with opensafer.open_dir_safer(TEST_DIR.joinpath("unexists/unexists")) as d:
    with open(d.joinpath("sample.txt"), "w") as file:
      assert file.write("123") == 3

  with open(TEST_DIR.joinpath("unexists/unexists/sample.txt"), "r") as file:
    assert file.read() == "123"

def test_open_dir_safer3 ():

  #既に内容物が存在するディレクトリを指定した場合の動作確認(既存のファイルは複製されます)

  with open(TEST_DIR.joinpath("sample.txt"), "w") as file:
    file.write("abc")

  with opensafer.open_dir_safer(TEST_DIR) as d:
    with open(d.joinpath("sample.txt"), "a") as file:
      file.write("123")

  with open(TEST_DIR.joinpath("sample.txt"), "r") as file:
    assert file.read() == "abc123"
