"""統括組織ホームページ（home/index.html）の編集用ツール。

home/index.html は Claude Design が書き出したバンドル（フォント等を埋め込んだ1ファイル）。
ページ本体はバンドル内の <script type="__bundler/template"> に JSON 文字列として入っている。
フォント定義（数千行）以外の「ページ本体」を home/src/page.dc.html に取り出して編集し、埋め戻す。

  python tools/home_page.py extract   # バンドル → home/src/page.dc.html
  python tools/home_page.py embed     # home/src/page.dc.html → バンドル

page.dc.html の書式は Claude Design の dc 形式（{{ 値 }}、<sc-for>、<sc-if>、sc-camel-on-click など）。
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "home" / "index.html"
SRC = ROOT / "home" / "src" / "page.dc.html"
TAG = '<script type="__bundler/template">'
START = "<style>\nhtml,body{margin:0"   # ページ本体の始まり（フォント定義の後のスタイル）
END = "</script>"                       # x-dc スクリプトの終わり（テンプレート内で最後のもの）


def load():
    bundle = BUNDLE.read_text(encoding="utf-8")
    a = bundle.find(TAG) + len(TAG)
    b = bundle.find("</script>", a)
    return bundle, a, b, json.loads(bundle[a:b])


def split(tpl):
    i = tpl.find(START)
    j = tpl.rfind(END) + len(END)
    if tpl.count(START) != 1 or j <= i:
        sys.exit("ページ本体の位置が見つかりません")
    return tpl[:i], tpl[i:j], tpl[j:]


def extract():
    _, _, _, tpl = load()
    SRC.parent.mkdir(parents=True, exist_ok=True)
    SRC.write_text(split(tpl)[1], encoding="utf-8", newline="\n")
    print("wrote", SRC.relative_to(ROOT))


def embed():
    bundle, a, b, tpl = load()
    head, _, tail = split(tpl)
    page = SRC.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not page.startswith(START):
        sys.exit("page.dc.html の先頭は " + repr(START) + " で始めてください")
    raw = bundle[a:b]
    # </script> でバンドルのスクリプトが途切れないよう、"</" は "</" にエスケープする（書き出し時と同じ形式）
    enc = json.dumps(head + page + tail, ensure_ascii=False).replace("</", "<\\u002F")
    lead = raw[: len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()):]
    BUNDLE.write_text(bundle[:a] + lead + enc + trail + bundle[b:], encoding="utf-8")
    print("embedded", SRC.relative_to(ROOT), "->", BUNDLE.relative_to(ROOT))


if __name__ == "__main__":
    {"extract": extract, "embed": embed}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
