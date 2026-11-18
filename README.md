# KU-Saitenjikkou-HP

関西大学 祭典実行委員会サイトの下書きです。

- `home/` … 統括組織ホームページ（下書き）
- `template/` … 学部委員会サイトのテンプレート。`template/?faculty=商学部` のように学部を指定できます
- `template-apple/` … テンプレートのApple風版（作業中）。余白を8の倍数に統一、重ねた影、スクロール連動の演出を追加

## 統括組織ホームページの編集

`home/index.html` はフォントを埋め込んだ1ファイルなので、直接は編集しにくい。ページ本体は `home/src/page.dc.html` を編集し、次のコマンドで埋め戻す。

```
python tools/home_page.py embed
```

バンドルから取り出し直すときは `python tools/home_page.py extract`。
