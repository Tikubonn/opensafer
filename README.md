
# opensafer

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

ファイルを比較的安全に保存する機能を提供します。

具体的には「ファイルを作成・編集するときに、ファイルへの変更を一時ファイルに肩代わりさせ、一連の処理が完了した後に対象ファイルを置換する」といった機能を提供します。
これにより、ファイル書き出し中に例外が発生したことによって、空のファイルが作成されてしまったり、
入力元・出力先が同じファイルだったために、おかしな挙動をしてしまう現象を回避することができます。

## Usage

ファイル作成機能の実行例

```py
import opensafer

with opensafer.open_safer("sample.txt", "w") as output_file:
  with open("sample.txt", "r") as input_file:
    for line in input_file:
      output_file.write(line.upper())
```

ディレクトリ作成機能の実行例

```py
import opensafer
from pathlib import Path

with opensafer.open_dir_safer("sample") as path:
  with open(path.joinpath("sample.txt"), "x"):
    pass

list(Path("sample").walk()) #[(WindowsPath("./sample"), [], ["sample.txt"])]
```

## Install

```shell
pip install .
```

### Test

```shell
pip install .[test]
pytest .
```

### Document

```py
import opensafer

help(opensafer)
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2025 tikubonn

opensafer licensed under the [AGPLv3](./LICENSE).
