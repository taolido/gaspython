# 4-5. よくあるトラブルと対処法

## この節で学ぶこと

- ローカル環境でよく遭遇するトラブル
- 各トラブルの原因と解決策
- トラブルを避けるためのTips

---

## トラブル1: venvが有効化されていない

### 症状

```
pip install pandas

# エラーや意図しない動作
# または、グローバル環境にインストールされてしまう
```

### 原因

venvを有効化していない状態で pip install した

### 確認方法

プロンプトに `(venv)` が表示されているか確認：

```
# 有効化されていない
C:\...\sales_tool>

# 有効化されている
(venv) C:\...\sales_tool>
```

### 解決策

```
# Windows
.\venv\Scripts\activate

# Mac
source venv/bin/activate
```

### 予防策

**pip install する前に、必ず (venv) の表示を確認する習慣をつける**

---

## トラブル2: 「モジュールが見つからない」エラー

### 症状

```
ModuleNotFoundError: No module named 'pandas'
```

### 原因

1. ライブラリをインストールしていない
2. venvが有効化されていない（別の環境を見ている）
3. スペルミス

### 解決策

```
# venvが有効化されているか確認
# (venv) が表示されているか？

# インストール済みか確認
pip list

# なければインストール
pip install pandas
```

---

## トラブル3: 依存関係の競合

### 症状

```
ERROR: Cannot install package-A==1.0 and package-B==2.0 because
these package versions have conflicting dependencies.
```

### 原因

2つのパッケージが、同じライブラリの異なるバージョンを要求している

### 解決策

**方法1: 新しいvenvで最小構成から試す**

```
# 現在のvenvを削除
rmdir /s /q venv  # Windows
rm -rf venv       # Mac

# 新しいvenvを作成
python -m venv venv
.\venv\Scripts\activate  # Windows

# 本当に必要なものだけインストール
pip install pandas openpyxl
```

**方法2: AIに質問する**

```
【状況】
pip installで以下のエラーが出ました。解決策を教えてください。

【エラーメッセージ】
[エラーを全文コピペ]

【やりたいこと】
pandas と tensorflow を同じ環境で使いたい
```

---

## トラブル4: 「昨日まで動いていたのに動かない」

### 症状

```
昨日実行できたスクリプトが、今日はエラーになる
```

### 原因

1. 何かをインストール/更新して、依存関係が崩れた
2. venvを有効化し忘れている
3. 別のプロジェクトのvenvを有効化している

### 解決策

**まず確認：**
```
# 正しいディレクトリにいるか
cd

# 正しいvenvが有効化されているか
# (venv) の表示を確認

# 必要なライブラリが入っているか
pip list
```

**それでもダメなら：venvを作り直す**

```
deactivate
rmdir /s /q venv  # Windows
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## トラブル5: PowerShellでスクリプト実行がブロックされる

### 症状（Windows PowerShell）

```
.\venv\Scripts\Activate.ps1 : このシステムではスクリプトの実行が
無効になっているため、ファイル ... を読み込むことができません。
```

### 原因

PowerShellの実行ポリシーが厳しい設定になっている

### 解決策

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

その後、再度有効化：
```powershell
.\venv\Scripts\Activate.ps1
```

---

## トラブル6: pipが古い

### 症状

```
WARNING: You are using pip version 21.x.x; however, version 23.x.x is available.
```

### 解決策

```
# venvを有効化した状態で
pip install --upgrade pip
```

---

## トラブル回避のTips

### Tip 1: 最小構成から始める

```
# 最初から大量にインストールしない
pip install pandas numpy scipy matplotlib seaborn sklearn tensorflow

# 本当に必要なものだけ
pip install pandas openpyxl
```

### Tip 2: requirements.txtを早めに作る

```
# インストールしたらすぐに保存
pip install pandas
pip freeze > requirements.txt
```

### Tip 3: プロジェクトごとにvenvを分ける

```
project_A/
└── venv/  # project_A専用

project_B/
└── venv/  # project_B専用

# 絶対に混ぜない
```

### Tip 4: グローバル環境には何も入れない

```
# これはNG
C:\> pip install pandas

# 必ずvenvを作ってから
C:\project> python -m venv venv
C:\project> .\venv\Scripts\activate
(venv) C:\project> pip install pandas
```

---

## この節のまとめ

- ほとんどのトラブルは「venvの有効化忘れ」が原因
- 依存関係の競合は、venvを作り直すのが最速の解決策
- requirements.txtがあれば、いつでも環境を復元できる
- 迷ったらAIに質問（エラーメッセージを全文コピペ）

**次の節では、作ったツールをexe化して配布する方法を学びます。**
