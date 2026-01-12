# 4-7. AIプロンプトテンプレート（ローカル環境編）

## この節で学ぶこと

- ローカル環境のトラブルをAIに質問する方法
- 効果的なプロンプトの書き方
- 具体的なプロンプトテンプレート集

---

## ローカル環境でAIに質問するコツ

ローカル環境のトラブルは、ColabよりもAIへの伝え方が重要です。

```
┌─────────────────────────────────────────────────────────────┐
│  AIに伝えるべき情報                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. OS（Windows / Mac）                                     │
│  2. Pythonのバージョン                                      │
│  3. venvを使っているか                                      │
│  4. エラーメッセージ（全文コピペ）                          │
│  5. 何をしようとしたか                                      │
│  6. 期待した結果と実際の結果                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### なぜ詳しい情報が必要か

```
悪い質問:
「pip installでエラーが出ます。どうすればいいですか？」

→ AIの反応:
  「どんなエラーですか？OSは何ですか？venvは有効化していますか？」
  と質問で返ってくる

良い質問:
「Windows 11でPython 3.11を使っています。
venvを有効化した状態で pip install pandas を実行したら
以下のエラーが出ました：
[エラーメッセージ全文]」

→ AIの反応:
  具体的な解決策が返ってくる
```

---

## プロンプトテンプレート集

### テンプレート1: pip installのエラー

```
【環境】
- OS: Windows 11（またはMac）
- Python: 3.11.5
- venv: 有効化している

【状況】
pip install で以下のエラーが出ました。

【コマンド】
pip install pandas

【エラーメッセージ】
[ここにエラーメッセージを全文コピペ]

【質問】
このエラーの原因と解決方法を教えてください。
```

**使用例：**

```
【環境】
- OS: Windows 11
- Python: 3.11.5
- venv: 有効化している

【状況】
pip install で以下のエラーが出ました。

【コマンド】
pip install tensorflow

【エラーメッセージ】
ERROR: Could not find a version that satisfies the requirement tensorflow
ERROR: No matching distribution found for tensorflow

【質問】
このエラーの原因と解決方法を教えてください。
```

**AIからの回答例：**

```
このエラーは、お使いのPythonバージョンに対応したtensorflowが
見つからないことを意味します。

考えられる原因：
1. Python 3.12を使っている（tensorflowは3.12未対応の場合がある）
2. 32bit版Pythonを使っている

解決策：
1. Pythonのバージョンを確認
   python --version

2. Python 3.11以前を使用するか、tensorflow-cpu を試す
   pip install tensorflow-cpu

3. 公式サポート状況を確認
   https://www.tensorflow.org/install/pip
```

---

### テンプレート2: venvのトラブル

```
【環境】
- OS: Windows 11（またはMac）
- Python: 3.11.5

【状況】
venvの操作で問題が発生しました。

【実行したコマンド】
[ここにコマンドを記載]

【発生した問題】
[何が起きたか、エラーメッセージがあれば全文コピペ]

【期待した動作】
[本来どうなるべきだったか]

【質問】
この問題の原因と解決方法を教えてください。
```

**使用例：**

```
【環境】
- OS: Windows 11
- Python: 3.11.5

【状況】
venvの有効化でエラーが発生しました。

【実行したコマンド】
.\venv\Scripts\Activate.ps1

【発生した問題】
.\venv\Scripts\Activate.ps1 : このシステムではスクリプトの実行が
無効になっているため、ファイル C:\...\Activate.ps1 を読み込むことが
できません。

【期待した動作】
(venv) がプロンプトに表示されて有効化される

【質問】
この問題の原因と解決方法を教えてください。
```

**AIからの回答例：**

```
これはPowerShellの実行ポリシーによるブロックです。

解決策：

方法1: 実行ポリシーを変更する
PowerShellで以下を実行してください：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

その後、再度有効化を試してください：
.\venv\Scripts\Activate.ps1

方法2: コマンドプロンプトを使う
PowerShellの代わりにコマンドプロンプト（cmd）を使い：
.\venv\Scripts\activate.bat
```

---

### テンプレート3: 「昨日まで動いていたのに」問題

```
【環境】
- OS: Windows 11（またはMac）
- Python: 3.11.5
- venv: 使用している

【状況】
昨日まで動いていたスクリプトが動かなくなりました。

【スクリプト名】
main.py

【エラーメッセージ】
[ここにエラーメッセージを全文コピペ]

【最近変更したこと】
- 何かインストールした / していない
- スクリプトを編集した / していない
- PCを再起動した / していない

【質問】
原因の切り分け方法と解決策を教えてください。
```

**使用例：**

```
【環境】
- OS: Windows 11
- Python: 3.11.5
- venv: 使用している

【状況】
昨日まで動いていたスクリプトが動かなくなりました。

【スクリプト名】
sales_analysis.py

【エラーメッセージ】
ModuleNotFoundError: No module named 'pandas'

【最近変更したこと】
- 新しいプロジェクト用にpip installした
- スクリプトは編集していない
- PCは再起動していない

【質問】
原因の切り分け方法と解決策を教えてください。
```

**AIからの回答例：**

```
「ModuleNotFoundError: No module named 'pandas'」は、
venvが正しく有効化されていない可能性が高いです。

確認手順：

1. venvが有効化されているか確認
   プロンプトに (venv) が表示されていますか？
   表示されていなければ：
   .\venv\Scripts\activate

2. pandasがインストールされているか確認
   pip list | findstr pandas

3. 正しいディレクトリにいるか確認
   cd
   プロジェクトフォルダにいますか？

4. 別のプロジェクトのvenvを有効化していないか確認
   複数プロジェクトがある場合、正しいvenvを有効化していますか？

よくある原因：
新しいプロジェクトで作業した後、元のプロジェクトに戻るときに
venvの有効化を忘れている
```

---

### テンプレート4: PyInstallerのエラー

```
【環境】
- OS: Windows 11（またはMac）
- Python: 3.11.5
- PyInstaller: [バージョン]
- venv: 使用している

【状況】
PyInstallerでexe化しようとしたらエラーが発生しました。

【実行したコマンド】
pyinstaller --onefile main.py

【エラーメッセージ】
[ここにエラーメッセージを全文コピペ]

【スクリプトが使っているライブラリ】
- pandas
- openpyxl
- [その他]

【質問】
このエラーの原因と解決方法を教えてください。
```

**使用例：**

```
【環境】
- OS: Windows 11
- Python: 3.11.5
- PyInstaller: 6.3.0
- venv: 使用している

【状況】
PyInstallerでexe化しようとしたらエラーが発生しました。

【実行したコマンド】
pyinstaller --onefile sales_tool.py

【エラーメッセージ】
RecursionError: maximum recursion depth exceeded

【スクリプトが使っているライブラリ】
- pandas
- openpyxl
- matplotlib

【質問】
このエラーの原因と解決方法を教えてください。
```

**AIからの回答例：**

```
RecursionErrorは、PyInstallerが大きなライブラリを処理する際に
発生することがあります。

解決策：

方法1: .specファイルで再帰上限を引き上げる

1. まず通常通りビルドを試みる（失敗してもOK）
   pyinstaller --onefile sales_tool.py

2. 生成された sales_tool.spec を編集
   ファイルの先頭に追加：
   import sys
   sys.setrecursionlimit(5000)

3. specファイルからビルド
   pyinstaller sales_tool.spec

方法2: 最小構成のvenvを作り直す
不要なライブラリが多いとビルドが複雑になります。
必要最小限のライブラリだけでvenvを再構築してみてください。
```

---

### テンプレート5: exeが動作しない

```
【環境】
- OS: Windows 11（またはMac）
- Python: 3.11.5
- PyInstaller: [バージョン]

【状況】
作成したexeが正常に動作しません。

【症状】
- ダブルクリックすると一瞬で閉じる
- エラーメッセージ: [表示されれば記載]

【元のスクリプト】
python main.py で実行すると正常に動作する

【ビルドコマンド】
pyinstaller --onefile main.py

【質問】
exeが動作しない原因と対処法を教えてください。
```

**使用例：**

```
【環境】
- OS: Windows 11
- Python: 3.11.5
- PyInstaller: 6.3.0

【状況】
作成したexeが正常に動作しません。

【症状】
- ダブルクリックすると一瞬で閉じる
- エラーメッセージは見えない（すぐ閉じるため）

【元のスクリプト】
python sales_tool.py で実行すると正常に動作する

【ビルドコマンド】
pyinstaller --onefile sales_tool.py

【質問】
exeが動作しない原因と対処法を教えてください。
```

**AIからの回答例：**

```
exeが一瞬で閉じる場合、エラーが発生している可能性が高いです。
エラーを確認するために以下を試してください。

方法1: コマンドプロンプトから実行
1. コマンドプロンプトを開く
2. exeのあるフォルダに移動
   cd C:\path\to\dist
3. exeを実行
   sales_tool.exe
4. エラーメッセージが表示される

方法2: スクリプトに終了待機を追加
main()の呼び出しを以下のように変更：

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        input("Enterキーを押すと終了します...")

その後、再度ビルドしてください。

よくある原因：
1. ファイルパスの問題（相対パスを使っている）
2. 必要なファイルがexeに含まれていない
3. 使用しているライブラリの互換性問題
```

---

### テンプレート6: 依存関係の競合

```
【環境】
- OS: Windows 11（またはMac）
- Python: 3.11.5
- venv: 使用している

【状況】
pip install で依存関係の競合エラーが出ました。

【インストールしようとしたもの】
pip install [パッケージ名]

【エラーメッセージ】
[ここにエラーメッセージを全文コピペ]

【既にインストールしているもの】
[pip list の結果、または主要なパッケージ]

【やりたいこと】
[最終的にどのパッケージを使いたいか]

【質問】
この競合を解決する方法を教えてください。
```

**使用例：**

```
【環境】
- OS: Windows 11
- Python: 3.11.5
- venv: 使用している

【状況】
pip install で依存関係の競合エラーが出ました。

【インストールしようとしたもの】
pip install tensorflow

【エラーメッセージ】
ERROR: Cannot install tensorflow==2.15.0 and numpy==2.0.0 because
these package versions have conflicting dependencies.
tensorflow 2.15.0 requires numpy<2.0.0,>=1.23.5

【既にインストールしているもの】
pandas 2.2.0
numpy 2.0.0

【やりたいこと】
pandas と tensorflow を両方使いたい

【質問】
この競合を解決する方法を教えてください。
```

**AIからの回答例：**

```
numpyのバージョン競合です。tensorflowはnumpy 2.0未満を要求しています。

解決策：

方法1: 新しいvenvで最小構成から試す
最も確実な方法です。

1. 現在のvenvを無効化
   deactivate

2. venvを削除
   rmdir /s /q venv

3. 新しいvenvを作成
   python -m venv venv
   .\venv\Scripts\activate

4. tensorflow を先にインストール（依存関係で適切なnumpyが入る）
   pip install tensorflow

5. 次に pandas をインストール
   pip install pandas

6. 動作確認
   python -c "import tensorflow; import pandas; print('OK')"

方法2: numpyのバージョンを下げる
pip install numpy<2.0.0
pip install tensorflow

ポイント：
インストール順序が重要です。依存関係が厳しいパッケージを先に
インストールすると、競合が起きにくくなります。
```

---

## 万能プロンプト

どのテンプレートを使うか迷ったときは、これを使ってください。

```
【環境情報】
- OS: [Windows 11 / Mac]
- Python: [python --version の結果]
- venv: [使用している / していない]
- エディタ: [使用しているエディタ]

【状況説明】
[何をしようとしていたか]

【実行したコマンドまたはコード】
[実際に実行したもの]

【発生した問題】
[何が起きたか]

【エラーメッセージ】
[エラーがあれば全文コピペ]

【期待していた動作】
[本来どうなるべきだったか]

【既に試したこと】
[あれば記載]

【質問】
この問題を解決するにはどうすればいいですか？
```

---

## AIへの質問のコツ

### 1. エラーメッセージは全文コピペ

```
悪い例:
「エラーが出ました」

良い例:
「以下のエラーが出ました:
ModuleNotFoundError: No module named 'pandas'
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    import pandas as pd
...」
```

### 2. 環境情報を最初に伝える

```
悪い例:
「venvが有効化できません」

良い例:
「Windows 11、Python 3.11.5を使っています。
PowerShellで .\venv\Scripts\Activate.ps1 を実行したら
以下のエラーが出ました...」
```

### 3. やったことを時系列で伝える

```
悪い例:
「pip install したらエラーが出ました」

良い例:
「1. python -m venv venv を実行
2. .\venv\Scripts\activate を実行
3. pip install pandas を実行
4. 以下のエラーが発生...」
```

### 4. 期待と現実のギャップを伝える

```
悪い例:
「動きません」

良い例:
「期待: exeをダブルクリックしたらウィンドウが開いて処理が実行される
現実: 一瞬黒い画面が出てすぐに閉じる」
```

---

## この節のまとめ

- ローカル環境の問題は、環境情報（OS、Pythonバージョン、venv）を伝える
- エラーメッセージは必ず全文コピペする
- テンプレートを使うと、必要な情報を漏れなく伝えられる
- 「何をしようとして」「何が起きて」「何を期待していたか」を伝える
- 試したことがあれば、それも伝える

**次の章では、より高度なPython活用として、Web APIやデータベースとの連携を学びます。**
