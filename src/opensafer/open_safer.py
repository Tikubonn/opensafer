
import shutil
import typing
import tempfile
from pathlib import Path
from closeable import ICloseable, Closeable

class _OpenSafer (ICloseable):

  def __init__ (self, path:Path, temp_file, *, make_dir:bool):
    self._path = path
    self._temp_file = temp_file
    self._make_dir = make_dir
    self._closeable = Closeable(self._on_close)

  def _on_close (self, succeeded:bool):
    self._temp_file.close()
    if succeeded:
      if self._make_dir:
        self._path.parent.mkdir(parents=True, exist_ok=True)
      Path(self._temp_file.name).replace(self._path)
    else:
      Path(self._temp_file.name).unlink()

  def close (self, succeeded:bool=True):
    return self._closeable.close(succeeded)

  @property
  def closed (self) -> bool:
    return self._closeable.closed

  @property
  def path (self) -> Path:
    return self._path

  @property
  def temp_file (self):
    return self._temp_file

  @property
  def make_dir (self) -> bool:
    return self._make_dir

  def __enter__ (self):
    return self._temp_file

  def __exit__ (self, exc_type, exc_value, traceback):
    self.close((exc_type is None and exc_value is None and traceback is None))

def open_safer (path:Path|str, mode:str, *, make_dir:bool=False, buffering:int=-1, encoding:str|None=None, errors:str|None=None, newline:str|None=None) -> _OpenSafer|typing.IO:

  """指定されたファイルを比較的安全に作成します。

  本関数は with コンテキスト中のファイル変更を一時ファイルに肩代わりさせ、
  処理の完了後に対象ファイルに置換する操作を行う `_OpenSafer` インスタンスを作成します。
  もし with コンテキスト中に例外が発生した場合、対象ファイルへの反映は行われません。

  Notes
  -----
  本関数は with コンテキスト中での使用を推奨しています。

  Examples
  --------
  >>> with open_safer("sample.txt", "w") as file:
  >>>   print("Overwrite sample.txt when succeed.", file=file)
  >>>
  >>> #Case of same input and output.
  >>> with open_safer("sample.txt", "w") as output_file:
  >>>   with open_safer("sample.txt", "r") as input_file:
  >>>     for line in input_file:
  >>>       output_file.write(line.upper())
  >>>
  >>> #Case of 

  Parameters
  ----------
  path : Path|str
    開くファイルのパスです。
  mode : str
    `open` 関数で使用されるのと同じモードを指定するための文字列です。
    本引数に排他・読み込みモードが指定された場合、本関数は処理を `open` 関数に移譲して終了します。
  make_dir : bool
    本引数が `True` ならばファイルが置換される際に、親ディレクトリも一緒に作成されます。
  buffering : int
    `open` `tempfile.NamedTemporaryFile` 関数に渡される値です。
  encoding : str|None
    `open` `tempfile.NamedTemporaryFile` 関数に渡される値です。
  errors : str|None
    `open` `tempfile.NamedTemporaryFile` 関数に渡される値です。
  newline : str|None
    `open` `tempfile.NamedTemporaryFile` 関数に渡される値です。

  Returns
  -------
  _OpenSafer|typing.IO
    `mode` で排他・読み込みモードが指定された場合に `typing.IO` が返されます。
    `mode` でそれ以外のモードが指定された場合に `_OpenSafer` が返されます。
  """

  if "w" in mode:
    temp_file = tempfile.NamedTemporaryFile(
      mode, 
      delete=False,
      buffering=buffering,
      encoding=encoding,
      errors=errors,
      newline=newline
    )
  elif "r" in mode:
    if "+" in mode:
      if "b" in mode:
        md = "w+b"
      else:
        md = "w+"
      temp_file = tempfile.NamedTemporaryFile(
        md, 
        delete=False,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline
      )
      if "b" in mode:
        md2 = "rb"
      else:
        md2 = "r"
      with open(path, md2) as file:
        shutil.copyfileobj(file, temp_file)
      temp_file.seek(0)
    else:
      return open(
        path, 
        mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline
      )
  elif "a" in mode:
    md = "w"
    if "+" in mode:
      md += "+"
    if "b" in mode:
      md += "b"
    temp_file = tempfile.NamedTemporaryFile(
      md, 
      delete=False,
      buffering=buffering,
      encoding=encoding,
      errors=errors,
      newline=newline
    )
    try:
      if "b" in mode:
        md2 = "rb"
      else:
        md2 = "r"
      with open(path, md2) as file:
        shutil.copyfileobj(file, temp_file)
    except FileNotFoundError:
      pass
  elif "x" in mode:
    return open(
      path, 
      mode,
      buffering=buffering,
      encoding=encoding,
      errors=errors,
      newline=newline
    )
  else:
    raise ValueError()
  return _OpenSafer(Path(path), temp_file, make_dir=make_dir)
