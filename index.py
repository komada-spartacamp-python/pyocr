# 光学文字認識（Optical Character Recognition）は、画像の文字を文字コードの列に変換することを言い、一般にはそのソフトウェアです
from PIL import Image
import pyocr
import pyocr.builders
import glob
import datetime
import os

# OCRエンジンの取得
# pyocr.get_available_tools()で使用可能なOCRエンジンを取得できます。今回はTesseractしかインストールしていない状態なので、tools[0]で取得できます
tools = pyocr.get_available_tools()
tool = tools[0]

# tesseract_layoutの選び方
# 0 オリエンテーションとスクリプト検出（OSD）のみ。
# 1 自動ページ分割とOSD。
# 2 自動ページ分割、ただしOSD、またはOCRはなし。(未実装)
# 3 完全自動ページ分割、ただしOSDなし。(初期設定)
# 4 サイズの異なるテキストが1列に並んでいると仮定します。
# 5 縦書きの一様なテキストブロックを想定しています。
# 6 一様なテキストブロックを想定しています。
# 7 画像を1つのテキスト行として扱う。
# 8 画像を1つの単語として扱う。
# 9 画像を円内の単一単語として扱う。
# 10 画像を1つの文字として扱う。
# 11 疎なテキスト。できるだけ多くのテキストを順不同に探します。
# 12 OSDでテキストを疎にする。
# 13 生の行。画像を1つのテキスト行として扱います。
# Tesseract 固有のハックを回避することができます。

# tesseract_layout=6を使わないと45が読み取れなかったため採用。デフォルト設定は、tesseract_layout=3。
def image_to_text(file_path):
    # ＯＣＲ実行
    # OCRで文字認識を行うにはimage_to_string()関数を呼び出します。この関数には、画像、言語の他に、builderとして文字認識用のTextBuilder()を指定します。
    # TextBuilder	文字列を認識
    # WordBoxBuilder	単語単位で文字認識 + BoundingBox
    # LineBoxBuilder	行単位で文字認識 + BoundingBox
    # DigitBuilder	数字 / 記号を認識	今回はこれを採用
    # DigitLineBoxBuilder	数字 / 記号を認識 + BoundingBox
    # 文字の枠はWordBoxBuilder
    # 行のリスト(文字の行のピクセル等)はLineBoxBuilder
    txt = tool.image_to_string(
        # 原稿画像の読み込み
        # 画像の読み込みには、PyOCRと一緒にインストールされたPillowを用います。from PIL import ImageでインポートしたImageからopen()関数を呼び出します。
        Image.open(file_path),  # OCRする画像
        lang="jpn",  # 学習済み言語データ
        builder=pyocr.builders.DigitBuilder(tesseract_layout=6),  # 期待される出力のタイプを指定
    )

    return txt


def main():
    # イメージに入っている写真をアスタリスクで全件取得
    file_paths = glob.glob("images/*")  # 置き換え
    to_dir = "outputs"

    for file_path in file_paths:
        txt = image_to_text(file_path)
        # os なしだと同じファイルの中に上書きを5回される
        # パスからファイル名のみ(拡張子なし)を取得
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # 出力先のパスを生成
        to_path = os.path.join(to_dir, filename + ".txt")

        # 出力先を生成したパスに変更text.txt
        # with openはcloseをしなくてよくなる。openのみだとcloseしないといけない。mode="w"はwriteの略で書き込みでfはファイルの略でasで省略している
        with open(to_path, mode="w") as f:
            f.writelines(txt)


def read():
    file_paths2 = glob.glob("outputs/*")
    a = []
    for file_path2 in file_paths2:
        with open(file_path2, mode="r") as f:
            # print(file_path2)ファイル名を取り出す
            s = f.read()
            s = int(s)
            # a = [] これをここに書くと一個一個に配列が追加される
            # s += s これだと同じファイル内での足し算
            a.append(s)
    sum_number = 0
    for r in range(0, len(a)):
        number = int(a[r])
        sum_number += number
    return sum_number


def text():
    datetime_format = datetime.datetime(2017, 11, 12, 9, 55, 28)
    c = datetime_format.strftime("%Y/%m/%d")
    print(f"{c}の摂取カロリーは{read()}kcalです。")


# def read():
#     with open("outputs/01.txt", mode="r") as f:
#         s = f.read()
#         print(s)


# だめだった int(txt)
if __name__ == "__main__":
    main()
    text()
