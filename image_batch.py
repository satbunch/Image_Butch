#!/usr/bin/env python3
import argparse
import sys
import re
from pathlib import Path

import pandas as pd
from PIL import Image, ImageOps

# 縦画像・横画像それぞれの出力サイズ
VERTICAL_SIZE = (1050, 1400)  # (幅、高さ)
HORIZONTAL_SIZE = (1400, 1050)

# Excelマッピング用のシート
MAPPING_SHEET = "ポイントSTに在庫のある商品リスト"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="image_batch.py",
        description="ディレクトリ内の画像を一括リサイズ＆リネームして別フォルダへ出力するツール",
    )
    parser.add_argument(
        "-r", "--root", type=Path, required=True, help="作業ディレクトリのパス"
    )
    parser.add_argument(
        "-m",
        "--mapping",
        type=Path,
        required=True,
        help="コードと商品番号対応表のExcelファイルのパス",
    )
    parser.add_argument(
        "--output-subdir",
        type=str,
        default="resize",
        help="リサイズ後ファイルの出力先",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # ルートとマッピングファイルの存在チェック
    if not args.root.is_dir():
        print(f"エラー: rootディレクトリが見つかりません: {args.root}", file=sys.stderr)
        sys.exit(1)
    if not args.mapping.is_file():
        print(f"エラー: Excelファイルが見つかりません: {args.mapping}", file=sys.stderr)
        sys.exit(1)

    # Excelを読み込んで辞書化
    df = pd.read_excel(args.mapping, dtype=str, usecols=[5, 6], engine="openpyxl")
    codes = df.iloc[:, 0]
    prods = df.iloc[:, 1]
    mapping = dict(zip(codes, prods))

    # リサンプルフィルタを固定指定
    resample_filter = Image.Resampling.LANCZOS

    # 上位ディレクトリをスキャン
    for code_dir in sorted(args.root.iterdir()):
        if not code_dir.is_dir():
            continue
        code = code_dir.name
        # ディレクトリ名が4桁の数字でなければスキップ
        if not re.fullmatch(r"\d{4}", code):
            continue

        product_no = mapping.get(code)
        if not product_no:
            print(f"[警告]マッピングに存在しないコードです: {code}", file=sys.stderr)
            continue

        # 出力フォルダ
        out_dir = code_dir / args.output_subdir
        out_dir.mkdir(exist_ok=True)

        # 入力ファイル一覧
        valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
        files = sorted(
            p
            for p in code_dir.iterdir()
            if p.is_file() and p.suffix.lower() in valid_exts
        )

        counter = 1
        for src in files:
            try:
                with Image.open(src) as img:
                    w, h = img.size
                    # 向きに合わせてターゲットサイズを変更
                    target = VERTICAL_SIZE if h > w else HORIZONTAL_SIZE

                    # 指定サイズにリサイズ＆クロップ
                    proc = ImageOps.fit(
                        img,
                        target,
                        method=resample_filter,
                        centering=(0.5, 0.5),
                    )

                # 新ファイル名作成
                ext = src.suffix.lower()
                new_name = f"{product_no}_{counter:03d}{ext}"
                dst = out_dir / new_name
                proc.save(dst)

                # 保存
                print(f"{code}/{src.name} → {out_dir.name}/{new_name}")
                counter += 1

            except Exception as e:
                print(
                    f"[エラー] {code}/{src.name} の処理に失敗: ({e})", file=sys.stderr
                )

    print("処理が完了しました。")


if __name__ == "__main__":
    main()
