# 4-3. Pythonのインストール

## この節で学ぶこと

- WindowsへのPythonインストール方法
- MacへのPythonインストール方法
- インストールの確認方法
- よくあるインストールトラブルの解決

---

## Windows編

### Step 1: ダウンロード

1. ブラウザで以下のURLにアクセス：
   ```
   https://www.python.org/downloads/
   ```

2. 「Download Python 3.x.x」ボタンをクリック
   - 最新の安定版がダウンロードされる
   - 2025年時点では Python 3.11 または 3.12 推奨

### Step 2: インストール

1. ダウンロードしたインストーラー（python-3.x.x-amd64.exe）をダブルクリック

2. **重要！** 「Add python.exe to PATH」にチェックを入れる

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Python 3.11.x Setup                                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ [✓] Add python.exe to PATH  ← ★ここにチェック！        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  [Install Now]    [Customize installation]                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

3. 「Install Now」をクリック

4. インストール完了まで待つ

5. 「Setup was successful」と表示されたら完了

### Step 3: インストール確認

コマンドプロンプトまたはPowerShellを開いて確認：

```
# Windowsキー + R → 「cmd」と入力 → Enter

# Pythonのバージョン確認
python --version
```

**期待される出力：**
```
Python 3.11.5
```

```
# pipの確認
pip --version
```

**期待される出力：**
```
pip 23.2.1 from C:\Python311\Lib\site-packages\pip (python 3.11)
```

### トラブルシューティング（Windows）

**問題：「'python' は、内部コマンドまたは外部コマンドとして認識されていません」**

**原因：** PATHが通っていない

**解決策：**
1. Pythonを再インストール
2. 今度は「Add python.exe to PATH」にチェックを入れる

または、手動でPATHを設定：
1. Windowsキー → 「環境変数」で検索
2. 「システム環境変数の編集」を開く
3. 「環境変数」ボタンをクリック
4. 「Path」を選択して「編集」
5. 以下を追加（バージョンに合わせて変更）：
   - `C:\Python311`
   - `C:\Python311\Scripts`

---

## Mac編

### 方法1: 公式インストーラー（推奨・初心者向け）

1. ブラウザで以下のURLにアクセス：
   ```
   https://www.python.org/downloads/macos/
   ```

2. 「Download Python 3.x.x」をクリック

3. ダウンロードした `.pkg` ファイルをダブルクリック

4. インストーラーの指示に従ってインストール

### インストール確認（Mac）

ターミナルを開いて確認：

```bash
# ターミナルを開く: Cmd + Space → 「terminal」と入力

# Pythonのバージョン確認（Macでは python3 を使う）
python3 --version
```

**期待される出力：**
```
Python 3.11.5
```

```bash
# pipの確認
pip3 --version
```

**期待される出力：**
```
pip 23.2.1 from /Library/Frameworks/Python.framework/... (python 3.11)
```

### 方法2: Homebrew（経験者向け）

Homebrewがインストールされている場合：

```bash
# Pythonをインストール
brew install python

# 確認
python3 --version
```

---

## Windows / Mac 共通：PythonとPython3の違い

```
┌─────────────────────────────────────────────────────────────┐
│  コマンドの違い                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Windows:                                                    │
│    python --version        ← python を使う                  │
│    pip install pandas                                        │
│                                                              │
│  Mac:                                                        │
│    python3 --version       ← python3 を使う                 │
│    pip3 install pandas                                       │
│                                                              │
│  ※ Macの python はシステム標準のPython 2系を指すことがある │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### この講座での表記

```
この講座では、以下のように表記します：

Windows: python, pip
Mac: python3, pip3

Macユーザーは、「python」と書いてあったら「python3」に
読み替えてください。
```

---

## 確認用コマンド一覧

```bash
# Pythonバージョン
python --version  # Windows
python3 --version # Mac

# pipバージョン
pip --version     # Windows
pip3 --version    # Mac

# インストール場所
where python      # Windows
which python3     # Mac

# インストール済みパッケージ一覧
pip list          # Windows
pip3 list         # Mac
```

---

## よくあるインストールトラブル

### トラブル1: 複数バージョンがインストールされている

**症状：**
```
python --version
Python 3.9.7

python3 --version
Python 3.11.5
```

**対処法：**
- 混乱を避けるため、venvを使う
- venv内ではバージョンが固定される

### トラブル2: Microsoft Storeが起動する（Windows）

**症状：**
`python` と入力するとMicrosoft Storeが開く

**対処法：**
1. Windowsキー → 「アプリ実行エイリアスの管理」
2. 「アプリ インストーラー python.exe」をオフ
3. 「アプリ インストーラー python3.exe」をオフ

### トラブル3: SSLエラーが出る

**症状：**
```
pip install でSSL関連のエラーが出る
```

**対処法（Windows）：**
```
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org パッケージ名
```

---

## この節のまとめ

- Windows: 公式インストーラーで「Add to PATH」にチェック
- Mac: 公式インストーラーまたはHomebrew
- インストール後は `python --version` で確認
- Mac では `python3`, `pip3` を使う
- トラブルが起きたらAIに質問

**次の節では、いよいよvenv（仮想環境）を実際に作成します。**
