
import shutil
import tempfile
from pathlib import Path
from .state import State

class _OpenDirSafer:

  def __init__ (self, path:Path, temp_dir:tempfile.TemporaryDirectory):
    self._path = path
    self._temp_dir = temp_dir
    self._state = State.PENDING

  @property
  def path (self) -> Path:
    return self._path

  @property
  def dir (self) -> tempfile.TemporaryDirectory:
    return self._temp_dir

  def rename (self):
    match self._state:
      case State.PENDING:
        try:
          shutil.rmtree(self._path)
        except FileNotFoundError:
          pass
        shutil.move(self._temp_dir.name, self._path)
        self._state = State.MOVED
      case _:
        raise ValueError()

  def cleanup (self):
    match self._state:
      case State.PENDING:
        self._temp_dir.cleanup()
        self._state = State.CLEANEDUP
      case _:
        raise ValueError()

  def __enter__ (self):
    return Path(self._temp_dir.name)

  def __exit__ (self, exc_type, exc_value, traceback):
    if (exc_type is None and 
        exc_value is None and 
        traceback is None):
      self.rename()
    else:
      self.cleanup()

def open_dir_safer (path:Path|str) -> _OpenDirSafer:

  """指定されたディレクトリを安全に作成します。

  本関数は一時ディレクトリを作成し with コンテキストでの処理の完了後、対象ディレクトリをそのディレクトリに置換します。
  もし with コンテキスト中に例外が発生した場合、対象ディレクトリへの置換操作は行われません。

  Notes
  -----
  本関数は with コンテキスト中での使用を推奨しています。

  Examples
  --------
  >>> from pathlib import Path
  >>>
  >>> with open_dir_safer("sample") as path:
  >>>   with open(path.joinpath("sample.txt"), "x"):
  >>>     pass
  >>> list(Path("sample").walk()) #[(WindowsPath("sample"), [], ["sample.txt"])]

  Parameters
  ----------
  path : Path|str
    作成するディレクトリのパスです。

  Returns
  -------
  _OpenDirSafer
    作成された `_OpenDirSafer` インスタンスです。
  """

  temp_dir = tempfile.TemporaryDirectory(delete=False)
  p = Path(path)
  try:
    for f in p.iterdir():
      fdst = Path(temp_dir.name).joinpath(f.relative_to(p))
      if f.is_dir():
        shutil.copytree(f, fdst)
      else:
        shutil.copy(f, fdst)
  except FileNotFoundError:
    pass
  return _OpenDirSafer(p, temp_dir)
