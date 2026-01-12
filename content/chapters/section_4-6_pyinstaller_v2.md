# 4-6. PyInstallerでexe化する

## この節で学ぶこと

- PyInstallerとは何か
- Pythonスクリプトをexeファイルに変換する方法
- 「ダブルクリックで実行」できるツールを作る
- exe配布時の注意点

---

## PyInstallerとは

**PyInstaller** は、Pythonスクリプトを実行可能ファイル（exe）に変換するツールです。

```
┌─────────────────────────────────────────────────────────────┐
│  PyInstallerでできること                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  main.py → main.exe                                         │
│                                                              │
│  ✓ Pythonがインストールされていないパソコンでも動作        │
│  ✓ ダブルクリックで実行できる                              │
│  ✓ 他の人に配布できる                                      │
│  ✓ ライブラリも一緒にパッケージされる                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### GASとの違い

```
GAS:
・Googleのサーバーで実行される
・配布 = スクリプトへのアクセス権を共有
・相手もGoogleアカウントが必要

Python + exe:
・相手のパソコンで実行される
・配布 = exeファイルを渡すだけ
・相手はPythonもGoogleアカウントも不要
```

---

## Step 0: 変換用のPythonスクリプトを準備

まず、exe化するシンプルなスクリプトを作成します。

### sales_summary.py

```python
# sales_summary.py - 売上集計ツール
import pandas as pd
import os
import sys

def main():
    print("=" * 50)
    print("  売上集計ツール v1.0")
    print("=" * 50)
    print()

    # サンプルデータを作成
    data = {
        '日付': ['2024/01/01', '2024/01/02', '2024/01/03', '2024/01/04', '2024/01/05'],
        '商品': ['商品A', '商品B', '商品A', '商品C', '商品B'],
        '数量': [10, 5, 8, 3, 12],
        '単価': [1000, 2000, 1000, 3000, 2000]
    }
    df = pd.DataFrame(data)
    df['金額'] = df['数量'] * df['単価']

    print("【元データ】")
    print(df.to_string(index=False))
    print()

    # 商品別集計
    summary = df.groupby('商品')['金額'].sum().reset_index()
    summary.columns = ['商品', '売上合計']

    print("【商品別売上】")
    print(summary.to_string(index=False))
    print()

    total = df['金額'].sum()
    print(f"【総売上】 {total:,}円")
    print()

    print("処理が完了しました！")
    print()

    # exeで実行した場合、すぐに閉じないようにする
    input("Enterキーを押すと終了します...")

if __name__ == "__main__":
    main()
```

### フォルダ構造

```
sales_tool/
├── venv/
├── sales_summary.py    ← 変換対象
└── requirements.txt
```

### 動作確認

```
(venv) C:\...\sales_tool> python sales_summary.py
```

**出力：**
```
==================================================
  売上集計ツール v1.0
==================================================

【元データ】
       日付   商品  数量  単価    金額
2024/01/01  商品A    10  1000   10000
2024/01/02  商品B     5  2000   10000
2024/01/03  商品A     8  1000    8000
2024/01/04  商品C     3  3000    9000
2024/01/05  商品B    12  2000   24000

【商品別売上】
  商品  売上合計
商品A     18000
商品B     34000
商品C      9000

【総売上】 61,000円

処理が完了しました！

Enterキーを押すと終了します...
```

---

## Step 1: PyInstallerをインストール

venvを有効化した状態でインストールします。

```
(venv) C:\...\sales_tool> pip install pyinstaller
```

**出力例：**
```
Collecting pyinstaller
  Downloading pyinstaller-6.3.0-py3-none-win_amd64.whl (1.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 5.2 MB/s eta 0:00:00
...
Successfully installed pyinstaller-6.3.0 pyinstaller-hooks-contrib-2024.0
```

### インストール確認

```
(venv) C:\...\sales_tool> pyinstaller --version
```

**出力：**
```
6.3.0
```

---

## Step 2: exeを作成する

### 基本的なコマンド

```
(venv) C:\...\sales_tool> pyinstaller --onefile sales_summary.py
```

**オプションの意味：**
- `--onefile`: すべてを1つのexeファイルにまとめる

**出力：**
```
118 INFO: PyInstaller: 6.3.0
118 INFO: Python: 3.11.5
119 INFO: Platform: Windows-10-10.0.19045-SP0
...
5234 INFO: Building EXE from EXE-00.toc completed successfully.
```

### 作成されたファイル

```
sales_tool/
├── venv/
├── sales_summary.py
├── sales_summary.spec       ← 設定ファイル（自動生成）
├── build/                   ← ビルド中間ファイル（削除OK）
│   └── sales_summary/
└── dist/                    ← ★ここにexeが作成される
    └── sales_summary.exe    ← これが配布用ファイル
```

### exeの実行

```
C:\...\sales_tool\dist> sales_summary.exe
```

または、エクスプローラーで `dist` フォルダを開いて `sales_summary.exe` をダブルクリック。

**出力：**
```
==================================================
  売上集計ツール v1.0
==================================================

【元データ】
       日付   商品  数量  単価    金額
2024/01/01  商品A    10  1000   10000
...

Enterキーを押すと終了します...
```

---

## Step 3: よく使うオプション

### オプション一覧

| オプション | 説明 |
|-----------|------|
| `--onefile` | 1つのexeにまとめる |
| `--noconsole` | コンソールウィンドウを表示しない（GUI用） |
| `--name 名前` | exeファイル名を指定 |
| `--icon アイコン.ico` | アイコンを設定 |
| `--add-data "ファイル;."` | 追加ファイルを含める |

### 実用的なコマンド例

```
# シンプルなexe（コンソール表示あり）
pyinstaller --onefile sales_summary.py

# 名前を変更
pyinstaller --onefile --name 売上集計ツール sales_summary.py

# アイコンを設定
pyinstaller --onefile --icon myicon.ico sales_summary.py

# GUIアプリ（コンソールなし）
pyinstaller --onefile --noconsole gui_app.py
```

> **注意**
> `--noconsole` を使う場合、`print()` の出力は見えません。
> コンソールアプリには使わないでください。

---

## Step 4: 配布時の注意点

### ファイルサイズ

```
┌─────────────────────────────────────────────────────────────┐
│  exeのファイルサイズ                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  元のPythonスクリプト: 1 KB                                 │
│  生成されたexe:       約 50〜150 MB                         │
│                                                              │
│  理由:                                                       │
│  ・Python本体が含まれる                                     │
│  ・使用しているライブラリがすべて含まれる                   │
│  ・pandas, numpy などは大きい                               │
│                                                              │
│  これは正常です。                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### ウイルス対策ソフトの誤検知

```
┌─────────────────────────────────────────────────────────────┐
│  よくある問題：ウイルス対策ソフトがブロックする            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  原因:                                                       │
│  ・PyInstallerで作成したexeは、ウイルスと誤検知されやすい  │
│  ・署名されていないexeは疑われる                           │
│                                                              │
│  対策:                                                       │
│  1. ウイルス対策ソフトで「除外」に追加                      │
│  2. 相手にも同様の対応をお願いする                          │
│  3. 会社のIT部門に相談                                       │
│                                                              │
│  重要:                                                       │
│  ・自分で作ったexeなので、実際にはウイルスではない          │
│  ・しかし、配布には注意が必要                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 配布のベストプラクティス

```
┌─────────────────────────────────────────────────────────────┐
│  配布方法のおすすめ                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  社内配布の場合:                                             │
│  1. 共有フォルダにexeを置く                                 │
│  2. 使い方のREADME.txtも一緒に置く                         │
│  3. IT部門に許可をもらう                                    │
│                                                              │
│  社外配布の場合:                                             │
│  1. ZIPファイルにまとめる                                   │
│  2. ファイル共有サービスでリンクを送る                     │
│  3. 「セキュリティソフトが警告を出すことがある」と伝える   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 5: 実践 - Excelファイルを処理するexe

より実用的な例として、Excelファイルを処理するexeを作成します。

### excel_processor.py

```python
# excel_processor.py - Excelファイル処理ツール
import pandas as pd
import os
import sys
from datetime import datetime

def get_desktop_path():
    """デスクトップのパスを取得"""
    return os.path.join(os.path.expanduser("~"), "Desktop")

def main():
    print("=" * 50)
    print("  Excel処理ツール v1.0")
    print("=" * 50)
    print()

    # デスクトップにサンプルExcelを作成
    desktop = get_desktop_path()
    sample_file = os.path.join(desktop, "sample_sales.xlsx")
    output_file = os.path.join(desktop, "sales_report.xlsx")

    # サンプルデータ作成
    print("サンプルExcelファイルを作成中...")
    data = {
        '日付': ['2024/01/01', '2024/01/02', '2024/01/03', '2024/01/04', '2024/01/05'],
        '部署': ['営業部', '開発部', '営業部', '総務部', '開発部'],
        '担当者': ['田中', '鈴木', '佐藤', '高橋', '伊藤'],
        '売上': [150000, 80000, 200000, 50000, 120000]
    }
    df = pd.DataFrame(data)
    df.to_excel(sample_file, index=False)
    print(f"作成: {sample_file}")
    print()

    # ファイルを読み込んで処理
    print("ファイルを処理中...")
    df = pd.read_excel(sample_file)

    print("\n【元データ】")
    print(df.to_string(index=False))

    # 部署別集計
    summary = df.groupby('部署')['売上'].agg(['sum', 'mean', 'count']).reset_index()
    summary.columns = ['部署', '売上合計', '平均', '件数']

    print("\n【部署別集計】")
    print(summary.to_string(index=False))

    # 結果をExcelに出力
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='元データ', index=False)
        summary.to_excel(writer, sheet_name='部署別集計', index=False)

    print(f"\n結果を出力: {output_file}")
    print()

    total = df['売上'].sum()
    print(f"【総売上】 {total:,}円")
    print()

    print("処理が完了しました！")
    print(f"デスクトップに '{os.path.basename(output_file)}' を作成しました。")
    print()

    input("Enterキーを押すと終了します...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print()
        input("Enterキーを押すと終了します...")
```

### exeを作成

```
(venv) C:\...\sales_tool> pyinstaller --onefile --name Excel処理ツール excel_processor.py
```

**出力：**
```
...
Building EXE from EXE-00.toc completed successfully.
```

### 作成されたexeを実行

```
dist/Excel処理ツール.exe をダブルクリック
```

**出力：**
```
==================================================
  Excel処理ツール v1.0
==================================================

サンプルExcelファイルを作成中...
作成: C:\Users\YourName\Desktop\sample_sales.xlsx

ファイルを処理中...

【元データ】
       日付    部署 担当者    売上
2024/01/01  営業部   田中  150000
2024/01/02  開発部   鈴木   80000
2024/01/03  営業部   佐藤  200000
2024/01/04  総務部   高橋   50000
2024/01/05  開発部   伊藤  120000

【部署別集計】
    部署  売上合計       平均  件数
  営業部    350000  175000.0     2
  開発部    200000  100000.0     2
  総務部     50000   50000.0     1

結果を出力: C:\Users\YourName\Desktop\sales_report.xlsx

【総売上】 600,000円

処理が完了しました！
デスクトップに 'sales_report.xlsx' を作成しました。

Enterキーを押すと終了します...
```

デスクトップに `sales_report.xlsx` が作成され、2つのシート（元データ、部署別集計）が含まれています。

---

## よくあるエラーと対処法

### エラー1: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'pandas'
```

**原因：** venvを有効化していない状態でPyInstallerを実行した

**対処法：**
```
# venvを有効化してから実行
.\\venv\\Scripts\\activate
pip install pyinstaller pandas openpyxl
pyinstaller --onefile sales_summary.py
```

### エラー2: exeが動作しない

```
exe をダブルクリックしても一瞬で閉じる
```

**原因：** エラーが発生しているがすぐに閉じてしまう

**対処法：** スクリプトの最後に `input()` を追加

```python
try:
    main()
except Exception as e:
    print(f"エラー: {e}")
finally:
    input("Enterキーを押すと終了します...")
```

### エラー3: ファイルパスのエラー

```
FileNotFoundError: [Errno 2] No such file or directory
```

**原因：** exe化すると作業ディレクトリが変わる

**対処法：** 絶対パスを使う

```python
# 相対パスはNG
df = pd.read_excel('data.xlsx')

# 絶対パスを使う
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(script_dir, 'data.xlsx'))
```

### エラー4: ビルドが遅い・固まる

```
ビルドに10分以上かかる、または途中で止まる
```

**原因：** 大量のライブラリがインストールされている

**対処法：** 最小構成のvenvを作り直す

```
deactivate
rmdir /s /q venv
python -m venv venv
.\\venv\\Scripts\\activate
pip install pandas openpyxl pyinstaller
pyinstaller --onefile sales_summary.py
```

---

## クリーンアップ

exe作成後、不要なファイルを削除できます。

```
sales_tool/
├── venv/
├── sales_summary.py
├── sales_summary.spec       ← 削除OK（設定を変更しないなら）
├── build/                   ← 削除OK（中間ファイル）
└── dist/
    └── sales_summary.exe    ← ★これだけ残す（配布用）
```

**削除コマンド：**
```
rmdir /s /q build
del sales_summary.spec
```

配布するときは、`dist/sales_summary.exe` だけを渡せばOKです。

---

## GAS経験者への補足

```
┌─────────────────────────────────────────────────────────────┐
│  GASとPython exeの違い                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GAS:                                                        │
│  ・コードはGoogleのサーバーにある                          │
│  ・実行もGoogleのサーバーで行われる                        │
│  ・相手はブラウザでアクセスする                            │
│  ・Googleアカウントが必要                                   │
│                                                              │
│  Python exe:                                                 │
│  ・コードは相手のPCにある（exe内部）                       │
│  ・実行も相手のPCで行われる                                │
│  ・相手はダブルクリックするだけ                            │
│  ・何のアカウントも不要                                     │
│                                                              │
│  使い分け:                                                   │
│  ・社内でGoogle Workspaceを使っているなら → GAS           │
│  ・社外配布や、Googleなしの環境なら → Python exe          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## この節のまとめ

- PyInstallerで `.py` → `.exe` に変換できる
- `pyinstaller --onefile script.py` で1つのexeを作成
- exeは約50〜150MBになる（Pythonとライブラリが含まれる）
- ウイルス対策ソフトに誤検知されることがある
- 配布は `dist/` フォルダ内のexeファイルだけでOK
- エラー対策として `input()` で終了前に待機させる

**次の節では、ローカル環境でのトラブルに対応するためのAIプロンプトテンプレートを紹介します。**
