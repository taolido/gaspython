# 4-4. venv実践ハンズオン

## この節で学ぶこと

- venv（仮想環境）の作成方法
- venvの有効化・無効化
- venv内へのライブラリインストール
- requirements.txtによる環境管理
- 実際にプロジェクトを作成する

---

## Step 1: プロジェクトフォルダを作成する

まず、プロジェクト用のフォルダを作成します。

### Windows（コマンドプロンプト）

```
# デスクトップに移動
cd %USERPROFILE%\Desktop

# プロジェクトフォルダを作成
mkdir sales_tool

# フォルダに移動
cd sales_tool

# 現在地を確認
cd
```

**出力例：**
```
C:\Users\YourName\Desktop\sales_tool
```

### Mac（ターミナル）

```bash
# デスクトップに移動
cd ~/Desktop

# プロジェクトフォルダを作成
mkdir sales_tool

# フォルダに移動
cd sales_tool

# 現在地を確認
pwd
```

**出力例：**
```
/Users/YourName/Desktop/sales_tool
```

---

## Step 2: venvを作成する

### Windows

```
python -m venv venv
```

### Mac

```bash
python3 -m venv venv
```

### 実行後のフォルダ構造

```
sales_tool/
└── venv/                    ← 作成された仮想環境
    ├── Include/
    ├── Lib/
    │   └── site-packages/   ← ここにライブラリが入る
    ├── Scripts/             ← Windows: 有効化スクリプト
    │   ├── activate
    │   ├── activate.bat
    │   └── python.exe
    └── pyvenv.cfg
```

> **解説**
> `python -m venv venv` の意味：
> - `python -m venv`: 「venvモジュールを実行して」
> - `venv`（最後の）: 「venvという名前のフォルダを作って」

---

## Step 3: venvを有効化する

### Windows（コマンドプロンプト）

```
.\venv\Scripts\activate
```

### Windows（PowerShell）

```powershell
.\venv\Scripts\Activate.ps1
```

> **PowerShellでエラーが出る場合：**
> 「スクリプトの実行がポリシーで禁止されています」というエラーが出たら：
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> を実行してから再度試してください。

### Mac

```bash
source venv/bin/activate
```

### 有効化の確認

有効化されると、**プロンプトの先頭に (venv) が表示されます**：

```
# 有効化前
C:\Users\YourName\Desktop\sales_tool>

# 有効化後
(venv) C:\Users\YourName\Desktop\sales_tool>
  ↑
  これが表示されればOK
```

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  (venv) が表示されている状態で pip install すると...        │
│                                                              │
│  → venv内にインストールされる（グローバルを汚染しない）    │
│  → このプロジェクト専用のライブラリになる                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 4: ライブラリをインストールする

venvが有効化された状態で、必要なライブラリをインストールします。

```
(venv) C:\...\sales_tool> pip install pandas openpyxl
```

**出力例：**
```
Collecting pandas
  Downloading pandas-2.0.3-cp311-cp311-win_amd64.whl (10.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.8/10.8 MB 5.2 MB/s eta 0:00:00
Collecting openpyxl
  Downloading openpyxl-3.1.2-py2.py3-none-any.whl (249 kB)
...
Successfully installed pandas-2.0.3 openpyxl-3.1.2 numpy-1.24.0 ...
```

### インストール確認

```
(venv) C:\...\sales_tool> pip list
```

**出力例：**
```
Package         Version
--------------- -------
numpy           1.24.0
openpyxl        3.1.2
pandas          2.0.3
pip             23.2.1
setuptools      65.5.0
```

### Pythonで確認

```
(venv) C:\...\sales_tool> python
```

```python
>>> import pandas as pd
>>> pd.__version__
'2.0.3'
>>> exit()
```

---

## Step 5: requirements.txtを作成する

インストールしたライブラリを「設計図」として保存します。

```
(venv) C:\...\sales_tool> pip freeze > requirements.txt
```

### 作成されたファイルの中身

```
# requirements.txt
et-xmlfile==1.1.0
numpy==1.24.0
openpyxl==3.1.2
pandas==2.0.3
python-dateutil==2.8.2
pytz==2023.3
six==1.16.0
```

### なぜrequirements.txtが重要か

```
┌─────────────────────────────────────────────────────────────┐
│  requirements.txt があれば...                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 環境が壊れても復旧できる                                │
│     venv削除 → 新規作成 → pip install -r requirements.txt │
│                                                              │
│  2. 別のPCでも同じ環境を再現できる                          │
│     requirements.txt をコピー → pip install -r ...         │
│                                                              │
│  3. 何がインストールされているか明確                        │
│     ファイルを見れば一目瞭然                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 6: Pythonスクリプトを作成して実行

### スクリプトを作成

テキストエディタ（メモ帳など）で以下の内容を作成し、`main.py` として保存：

```python
# main.py - 売上集計ツール
import pandas as pd

def main():
    print("===== 売上集計ツール =====")
    print(f"pandas version: {pd.__version__}")

    # サンプルデータを作成
    data = {
        '部署': ['営業部', '開発部', '営業部', '開発部', '総務部'],
        '金額': [10000, 20000, 15000, 25000, 8000]
    }
    df = pd.DataFrame(data)

    print("\n【元データ】")
    print(df)

    # 部署別集計
    result = df.groupby('部署')['金額'].sum()

    print("\n【部署別売上】")
    print(result)

    print("\n処理完了！")

if __name__ == "__main__":
    main()
```

### フォルダ構造

```
sales_tool/
├── venv/
├── main.py              ← 作成したスクリプト
└── requirements.txt
```

### 実行

```
(venv) C:\...\sales_tool> python main.py
```

**出力：**
```
===== 売上集計ツール =====
pandas version: 2.0.3

【元データ】
    部署     金額
0  営業部  10000
1  開発部  20000
2  営業部  15000
3  開発部  25000
4  総務部   8000

【部署別売上】
部署
営業部    25000
開発部    45000
総務部     8000
Name: 金額, dtype: int64

処理完了！
```

---

## Step 7: venvを無効化する

作業が終わったら、venvを無効化します。

```
(venv) C:\...\sales_tool> deactivate

C:\...\sales_tool>
  ↑
  (venv) が消えた
```

---

## Step 8: 環境を再構築する練習

「環境が壊れた」想定で、venvを削除して再構築してみましょう。

### 1. venvフォルダを削除

**Windows:**
```
rmdir /s /q venv
```

**Mac:**
```bash
rm -rf venv
```

### 2. 新しいvenvを作成

**Windows:**
```
python -m venv venv
.\venv\Scripts\activate
```

**Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. requirements.txtから復元

```
(venv) C:\...\sales_tool> pip install -r requirements.txt
```

### 4. 動作確認

```
(venv) C:\...\sales_tool> python main.py
```

**同じ出力が得られればOK！**

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  おめでとうございます！                                      │
│                                                              │
│  これで「環境が壊れても5分で復旧できる」スキルを            │
│  身につけました。                                            │
│                                                              │
│  プロのエンジニアでも環境を壊します。                       │
│  違いは「壊れても5分で復旧できる」こと。                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## venv操作まとめ

### Windows

| 操作 | コマンド |
|------|----------|
| venv作成 | `python -m venv venv` |
| 有効化 | `.\venv\Scripts\activate` |
| 無効化 | `deactivate` |
| venv削除 | `rmdir /s /q venv` |

### Mac

| 操作 | コマンド |
|------|----------|
| venv作成 | `python3 -m venv venv` |
| 有効化 | `source venv/bin/activate` |
| 無効化 | `deactivate` |
| venv削除 | `rm -rf venv` |

### 共通

| 操作 | コマンド |
|------|----------|
| ライブラリインストール | `pip install パッケージ名` |
| インストール一覧 | `pip list` |
| requirements.txt作成 | `pip freeze > requirements.txt` |
| requirements.txtから復元 | `pip install -r requirements.txt` |

---

## よくある質問

### Q: venvフォルダの名前は「venv」じゃなくてもいい？

A: はい。`python -m venv myenv` とすれば `myenv` という名前になります。ただし、`venv` が慣習的に使われるため、この講座では `venv` を使用します。

### Q: venvフォルダをGitにコミットすべき？

A: いいえ。venvフォルダはGitにコミットしません。代わりに `requirements.txt` をコミットします。`.gitignore` に `venv/` を追加しましょう。

### Q: venvを有効化し忘れてpip installしてしまった

A: グローバル環境にインストールされてしまいました。以下で削除できます：
```
pip uninstall パッケージ名
```
今後は「(venv)がプロンプトに表示されているか」を確認する習慣をつけましょう。

---

## この節のまとめ

- `python -m venv venv` でvenvを作成
- 有効化すると「(venv)」がプロンプトに表示される
- 有効化した状態で `pip install` するとvenv内にインストールされる
- `pip freeze > requirements.txt` で環境を保存
- `pip install -r requirements.txt` で環境を復元
- 壊れたらvenvを削除して作り直せばOK

**次の節では、よくあるトラブルとその対処法を学びます。**
