# 情報源マッピング

## 全体サマリー

| 章 | テーマ | 主要ソース | 補助ソース | 充足度 |
|---|--------|-----------|-----------|--------|
| 第0章 | 挫折ポイント | 技術評論社「10の壁」 | 各種挫折記事 | ⚪ |
| 第1章 | Colab + 文法 | Python-izm、東大Python入門 | python.jp | ⚪ |
| 第2章 | AI活用 | 「ChatGPTと学ぶPython入門」書籍 | Claude記事 | ⚪ |
| 第3章 | Excel×Python | Python-izm、FastClassInfo | openpyxl公式 | ⚪ |
| 第4章 | venv + 環境 | Python公式、DevelopersIO | Qualiteg記事 | ⚪ |
| 第5章 | GAS×Python | たぬハック、gspread系記事 | Qiita、odndo | ⚪ |

---

## Tier1: 主要情報源（体系的・高品質）

### Python-izm
- **URL:** https://www.python-izm.com/
- **特徴:** 
  - 入門編(8) / 基礎編(22) / 応用編(49) / 豆知識(10) / サードパーティ(21)
  - 全158コンテンツ
  - 完全無料
  - 辞書的に使える構造
- **本講座での用途:** 第1章（文法基礎）、第3章（Excel操作）
- **特に有用なセクション:**
  - サードパーティ > Excel操作 > OpenPyXL
  - 基礎編 > 文字列、リスト、辞書
  - 応用編 > ファイル操作

### 東大Pythonプログラミング入門
- **URL:** https://utokyo-ipp.github.io/
- **特徴:**
  - 大学講義ベースで正確
  - 体系的な構成
  - Google Colab使用前提
- **本講座での用途:** 第1章（文法基礎）の正確性担保

### FastClassInfo
- **URL:** https://fastclassinfo.com/
- **特徴:**
  - Excel×Python実践事例40+
  - 具体的なユースケース豊富
- **本講座での用途:** 第3章（Excel操作）の実践例

---

## Tier2: 補助情報源（特定トピック特化）

### openpyxl入門ガイド (programming-mondai.com)
- **URL:** https://programming-mondai.com/top/excel/
- **特徴:** Excel自動化完全特化
- **用途:** 第3章の補足

### Pythonのソバ (pythonsoba.tech)
- **URL:** https://pythonsoba.tech/
- **特徴:** 自動化ツール具体例53選
- **用途:** 実践アイデアの参考

### python.jp入門講座
- **URL:** https://python.jp/train/index.html
- **特徴:** Google Colab使用、初心者向け
- **用途:** 第1章の補足

---

## Tier3: 特定トピック情報源

### GAS vs Python比較

| サイト | URL | 特徴 |
|--------|-----|------|
| YesNoCode | engineer-life.dev/python-gas/ | 徹底比較記事 |
| life-table.com | life-table.com/python-gas-study/ | 実践者視点 |
| 隣IT | tonari-it.com | VBA/GAS/Python比較 |

### AI活用学習

| サイト/書籍 | 特徴 |
|-------------|------|
| 「ChatGPTと学ぶPython入門」（翔泳社） | 書籍、AI活用メソッドの参考 |
| Claude Code完全ガイド (magazine.code-college.jp) | Claude活用 |
| ChatGPT/Gemini/Claude比較 (generative-ai.sejuku.net) | ツール比較 |

### 環境構築・venv

| サイト | URL | 特徴 |
|--------|-----|------|
| Python公式 | packaging.python.org/ja/latest/ | venvの正式ドキュメント |
| DevelopersIO | dev.classmethod.jp | pip依存関係解説 |
| Qualiteg | blog.qualiteg.com | 依存関係エラー解決 |
| Tech Home | rush-up.co.jp/media/venvpython-setup-fast-os-vscode-zero-conflict/ | venv詳細解説 |

### 挫折ポイント

| サイト/書籍 | 特徴 |
|-------------|------|
| 「Pythonでチャレンジする入門」（技術評論社） | 「10の壁」フレームワーク |
| WEBCAMP MEDIA | 9割挫折データ |
| エンベーダー | 環境構築挫折解説 |

---

## GAS×Python連携情報源

### gspread関連

| サイト | URL | 特徴 |
|--------|-----|------|
| たぬハック | tanuhack.com/library-gspread/ | gspread使い方まとめ |
| 理想の働き方研究室 | pepenoheya.blog/python-library-gspread-certification/ | 認証設定詳細 |
| ジコログ | self-development.info | gspreadインストール解説 |
| Zenn (yamagishihrd) | zenn.dev/yamagishihrd/articles/2022-09_01-google-spreadsheet-with-python | 設定手順 |

### GAS WebAPI連携

| サイト | URL | 特徴 |
|--------|-----|------|
| odndo | odndo.com/posts/1628829322483/ | Python→GAS POST解説 |
| あっと寝てく？ | atnettec.com | Python×GAS連携ガイド |
| Qiita (ema_kurida) | qiita.com/ema_kurida/items/45bbdb007ed169521afc | ChatGPT+GAS連携 |
| monoblog | monoblog.jp/archives/5861 | GAS→Python制限解説 |

---

## 書籍参考（購入検討）

| 書籍名 | 出版社 | 用途 |
|--------|--------|------|
| 「ChatGPTと学ぶPython入門」 | 翔泳社 | AI活用メソッド参考 |
| 「Pythonでチャレンジする入門」 | 技術評論社 | 挫折ポイント参考 |

---

## 非採用情報源

### PyQ
- **理由:** ドリル形式で外部から参照しにくい
- **ただし:** 講座の「次のステップ」として紹介は有効

---

## 情報源選定基準

1. **体系性:** 断片的ではなく、全体像が見える
2. **正確性:** 公式ドキュメントとの整合性
3. **参照しやすさ:** 講座作成時に引用・参照しやすい
4. **更新性:** 古すぎない（Python 3.x系対応）
5. **無料アクセス:** 有料会員限定でない
