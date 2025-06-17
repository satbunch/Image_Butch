# Image Batch Tool

## 概要

Pictures 配下の 4 桁コードディレクトリ内の画像を再帰的に走査し、Excel マッピングを参照してリサイズ＆リネームを行う Python 製 CLI ツールです。

* 4 桁コード（例: `8000`）のディレクトリを検出
* Excel ファイルの A 列にコード、B 列に商品番号をマッピング
* 縦画像は 800×1000、横画像は 1000×800 にトリミング＆リサイズ
* リネーム形式: `<商品番号>_<連番>.<拡張子>`
* 出力先は各コードディレクトリ内の `resized/` サブフォルダ（デフォルト）

## 前提

* Python 3.8 以上がインストールされていること
* 対応プラットフォーム: Windows / macOS / Linux
* Excel マッピングファイル（コード ⇔ 商品番号）が用意されていること

## インストール手順

### 1. Python のインストール

#### Windows

1. Microsoft Store または [https://www.python.org/downloads](https://www.python.org/downloads) から Python 3.8+ をインストール
2. インストール時に「Add Python to PATH」にチェックを入れる

#### macOS

```bash
brew install python
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

### 2. リポジトリのクローン

```bash
git clone https://github.com/<ユーザー名>/<リポジトリ名>.git
cd <リポジトリ名>
```

### 3. 仮想環境の作成と有効化

**Unix 系 (macOS / Linux)**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

※ `requirements.txt` は以下の内容です：

```
pillow
pandas
openpyxl
```

## 使い方

```bash
./image_batch.py \
  --root /path/to/Pictures \
  --mapping /path/to/mapping.xlsx \
  [--output-subdir resized]
```

* `--root`           : Pictures ルートディレクトリのパス
* `--mapping`        : Excel マッピングファイルのパス（A列=コード、B列=商品番号）
* `--output-subdir`  : 各コードディレクトリ内の出力フォルダ名（デフォルト: `resized`）

### 実行例

```bash
./image_batch.py -r ~/Pictures/test -m ~/Downloads/mapping.xlsx
```

## スクリプト説明

* `image_batch.py` 本体：

  * `parse_args()` で引数を取得
  * `pandas.read_excel(..., usecols=[0,1], sheet_name=MAPPING_SHEET)` でマッピング読み込み
  * 各コードディレクトリを走査し、Pillow (`ImageOps.fit`) でトリミング＋リサイズ
  * 連番付きで商品番号\_連番.jpg として出力

## ライセンス

MIT License

---

ご不明点や改善要望があればお気軽に Issue を立ててください！
