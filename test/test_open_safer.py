
import io
import pytest
import shutil
import opensafer
from pathlib import Path

TEST_FILE = Path("./.test/sample.txt")
TEST_FILE_DATA = "abc"

def setup_function (func):
  TEST_FILE.parent.mkdir(parents=True, exist_ok=True)
  with open(TEST_FILE, "w") as file:
    file.write(TEST_FILE_DATA)

def teardown_function (func):
  shutil.rmtree(TEST_FILE.parent)

#読み込みモードの動作確認

def test_open_safer_read (): #r

  #読み込みモードならば open 関数と同じ挙動をします。

  with opensafer.open_safer(TEST_FILE, "r") as file:
    assert file.read() == TEST_FILE_DATA

    #読み込みモードならば .write することはできません。

    with pytest.raises(io.UnsupportedOperation):
      file.write("123")

  #存在しないファイルが指定されたならば FileNotFoundError が送出されます。

  with pytest.raises(FileNotFoundError):
    with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "r") as file:
      pass

def test_open_safer_read2 (): #rb

  #読み込みモードならば open 関数と同じ挙動をします。

  with opensafer.open_safer(TEST_FILE, "rb") as file:
    assert file.read() == TEST_FILE_DATA.encode("ascii")

    #読み込みモードならば .write することはできません。
    
    with pytest.raises(io.UnsupportedOperation):
      file.write(b"123")

  #存在しないファイルが指定されたならば FileNotFoundError が送出されます。

  with pytest.raises(FileNotFoundError):
    with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "rb") as file:
      pass

def test_open_safer_read3 (): #r+

  #r+ による更新モードならば読み書き両方を行えます。

  with opensafer.open_safer(TEST_FILE, "r+") as file:
    assert file.read() == TEST_FILE_DATA
    assert file.write("123") == 3
    assert file.seek(0) == 0
    assert file.read() == TEST_FILE_DATA + "123"

  #存在しないファイルが指定されたならば FileNotFoundError が送出されます。

  with pytest.raises(FileNotFoundError):
    with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "r+") as file:
      pass

def test_open_safer_read4 (): #r+b

  #r+ による更新モードならば読み書き両方を行えます。

  with opensafer.open_safer(TEST_FILE, "r+b") as file:
    assert file.read() == TEST_FILE_DATA.encode("ascii")
    assert file.write(b"123") == 3
    assert file.seek(0) == 0
    assert file.read() == TEST_FILE_DATA.encode("ascii") + b"123"

  #存在しないファイルが指定されたならば FileNotFoundError が送出されます。

  with pytest.raises(FileNotFoundError):
    with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "r+b") as file:
      pass

def test_open_safer_read5 (): #r mode and make_dir=True

  #存在しないファイルが指定されたならば FileNotFoundError が送出されます。

  with pytest.raises(FileNotFoundError):
    with opensafer.open_safer(TEST_FILE.parent.joinpath("unexists/unexists.txt"), "r", make_dir=True) as file:
      pass

#書き込みモードの動作確認

def test_open_safer_write (): #w

  with opensafer.open_safer(TEST_FILE, "w") as file:
    assert file.write("123") == 3

    #書き込みモードならば .read することはできません。

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "r") as file:
    assert file.read() == "123"

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "w") as file:
    assert file.write("123") == 3

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "r") as file:
    assert file.read() == "123"

def test_open_safer_write2 (): #wb

  with opensafer.open_safer(TEST_FILE, "wb") as file:
    assert file.write(b"123") == 3

    #書き込みモードならば .read することはできません。

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "rb") as file:
    assert file.read() == b"123"

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "wb") as file:
    assert file.write(b"123") == 3

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "rb") as file:
    assert file.read() == b"123"

def test_open_safer_write3 (): #w+

  with opensafer.open_safer(TEST_FILE, "w+") as file:
    assert file.write("123") == 3
    assert file.seek(0) == 0
    assert file.read() == "123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "r") as file:
    assert file.read() == "123"

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "w+") as file:
    assert file.write("123") == 3
    assert file.seek(0) == 0
    assert file.read() == "123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "r") as file:
    assert file.read() == "123"

def test_open_safer_write4 (): #w+b

  with opensafer.open_safer(TEST_FILE, "w+b") as file:
    assert file.write(b"123") == 3
    assert file.seek(0) == 0
    assert file.read() == b"123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "rb") as file:
    assert file.read() == b"123"

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "w+b") as file:
    assert file.write(b"123") == 3
    assert file.seek(0) == 0
    assert file.read() == b"123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "rb") as file:
    assert file.read() == b"123"

def test_open_safer_write5 (): #w mode and make_dir=True

  with opensafer.open_safer(TEST_FILE.parent.joinpath("unexists/unexists.txt"), "w", make_dir=True) as file:
    assert file.write("123") == 3

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.parent.joinpath("unexists/unexists.txt"), "r") as file:
    assert file.read() == "123"

#追記モードの動作確認

def test_open_safer_append (): #a
  
  with opensafer.open_safer(TEST_FILE, "a") as file:
    assert file.write("123") == 3

    #追記モードならば .read することはできません。

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "r") as file:
    assert file.read() == TEST_FILE_DATA + "123"
  
  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "a") as file:
    assert file.write("123") == 3

    #追記モードならば .read することはできません。

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "r") as file:
    assert file.read() == "123"

def test_open_safer_append2 (): #ab
  
  with opensafer.open_safer(TEST_FILE, "ab") as file:
    assert file.write(b"123") == 3

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "rb") as file:
    assert file.read() == TEST_FILE_DATA.encode("ascii") + b"123"
  
  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "ab") as file:
    assert file.write(b"123") == 3

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "rb") as file:
    assert file.read() == b"123"

def test_open_safer_append3 (): #a+
  
  with opensafer.open_safer(TEST_FILE, "a+") as file:
    assert file.write("123") == 3
    assert file.seek(0) == 0
    assert file.read() == TEST_FILE_DATA + "123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "r") as file:
    assert file.read() == TEST_FILE_DATA + "123"
  
  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "a+") as file:
    assert file.write("123") == 3
    assert file.seek(0) == 0
    assert file.read() == "123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "r") as file:
    assert file.read() == "123"

def test_open_safer_append4 (): #a+b
  
  with opensafer.open_safer(TEST_FILE, "a+b") as file:
    assert file.write(b"123") == 3
    assert file.seek(0) == 0
    assert file.read() == TEST_FILE_DATA.encode("ascii") + b"123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE, "rb") as file:
    assert file.read() == TEST_FILE_DATA.encode("ascii") + b"123"
  
  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "a+b") as file:
    assert file.write(b"123") == 3
    assert file.seek(0) == 0
    assert file.read() == b"123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "rb") as file:
    assert file.read() == b"123"

def test_open_safer_append5 (): #a mode and make_dir=True

  with opensafer.open_safer(TEST_FILE.parent.joinpath("unexists/unexists.txt"), "a", make_dir=True) as file:
    assert file.write("123") == 3

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.parent.joinpath("unexists/unexists.txt"), "r") as file:
    assert file.read() == "123"

#排他モードの動作確認

def test_open_safer_exclusive (): #x

  #排他モードならば open 関数と同じ挙動をします。

  with pytest.raises(FileExistsError):
    with opensafer.open_safer(TEST_FILE, "x") as file:
      pass

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "x") as file:
    assert file.write("123")

    #排他モードならば .write することはできません。

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "r") as file:
    assert file.read() == "123"

def test_open_safer_exclusive2 (): #xb

  #排他モードならば open 関数と同じ挙動をします。

  with pytest.raises(FileExistsError):
    with opensafer.open_safer(TEST_FILE, "xb") as file:
      pass

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "xb") as file:
    assert file.write(b"123")

    #排他モードならば .write することはできません。

    with pytest.raises(io.UnsupportedOperation):
      file.read()

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "rb") as file:
    assert file.read() == b"123"

def test_open_safer_exclusive3 (): #x+

  #排他モードならば open 関数と同じ挙動をします。

  with pytest.raises(FileExistsError):
    with opensafer.open_safer(TEST_FILE, "x+") as file:
      pass

  #x+ による更新モードならば読み書き両方を行えます。

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "x+") as file:
    assert file.write("123")
    assert file.seek(0) == 0
    assert file.read() == "123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "r") as file:
    assert file.read() == "123"

def test_open_safer_exclusive4 (): #x+b

  #排他モードならば open 関数と同じ挙動をします。

  with pytest.raises(FileExistsError):
    with opensafer.open_safer(TEST_FILE, "x+b") as file:
      pass

  #x+ による更新モードならば読み書き両方を行えます。

  with opensafer.open_safer(TEST_FILE.with_stem("unexists.txt"), "x+b") as file:
    assert file.write(b"123")
    assert file.seek(0) == 0
    assert file.read() == b"123"

  #一時ファイルへの変更が対象ファイルに適切に反映されたかを確認します。

  with open(TEST_FILE.with_stem("unexists.txt"), "rb") as file:
    assert file.read() == b"123"

def test_open_safer_exclusive5 (): #x mode and make_dir=True

  with pytest.raises(FileNotFoundError):
    with opensafer.open_safer(TEST_FILE.parent.joinpath("unexists/unexists.txt"), "x", make_dir=True) as file:
      pass

#未定義のオープンモード

def test_open_safer_error ():

  #未定義のモードが指定されたならば ValueError が送出されます。

  with pytest.raises(ValueError):
    with opensafer.open_safer(TEST_FILE, "1") as file:
      pass
