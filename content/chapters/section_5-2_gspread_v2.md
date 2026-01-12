# 5-2. PythonからスプレッドシートをDirectに操作（gspread）

## この節で学ぶこと

- GCPでサービスアカウントを作成する
- gspreadでスプレッドシートを操作する
- 読み込み・書き込みの基本操作
- pandasとの連携

---

## 全体像

```
┌─────────────────────────────────────────────────────────────┐
│  gspreadの仕組み                                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Python                 Google Cloud              スプレッド │
│  スクリプト             Platform                   シート    │
│                                                              │
│  ┌─────────┐           ┌─────────────┐         ┌─────────┐ │
│  │ gspread │ ───────→ │ Sheets API  │ ──────→ │  Sheet  │ │
│  └─────────┘   認証     └─────────────┘  操作   └─────────┘ │
│       ↑                                                      │
│       │                                                      │
│  credentials.json                                            │
│  （サービスアカウントキー）                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

GASと違い、PythonからGoogleスプレッドシートを操作するには **認証設定** が必要です。

---

## Step 1: GCPでプロジェクトを作成

### 1-1. Google Cloud Consoleにアクセス

```
https://console.cloud.google.com/
```

Googleアカウントでログインします。

### 1-2. 新しいプロジェクトを作成

1. 画面上部の「プロジェクトを選択」をクリック
2. 「新しいプロジェクト」をクリック
3. プロジェクト名を入力（例: `python-spreadsheet`）
4. 「作成」をクリック

```
┌─────────────────────────────────────────────────────────────┐
│  新しいプロジェクト                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  プロジェクト名: python-spreadsheet                         │
│  プロジェクトID: python-spreadsheet-123456（自動生成）      │
│  場所: 組織なし                                              │
│                                                              │
│  [作成]                                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 2: APIを有効化

### 2-1. Google Sheets APIを有効化

1. 左メニュー「APIとサービス」→「ライブラリ」
2. 検索欄に「Google Sheets API」と入力
3. 「Google Sheets API」をクリック
4. 「有効にする」をクリック

### 2-2. Google Drive APIを有効化

1. 再度「ライブラリ」に戻る
2. 検索欄に「Google Drive API」と入力
3. 「Google Drive API」をクリック
4. 「有効にする」をクリック

```
┌─────────────────────────────────────────────────────────────┐
│  有効にするAPI（両方必要）                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ☑ Google Sheets API   ← スプレッドシートの読み書き        │
│  ☑ Google Drive API    ← ファイルへのアクセス権限          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 3: サービスアカウントを作成

### 3-1. サービスアカウント作成

1. 左メニュー「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「サービスアカウント」
3. 以下を入力：
   - サービスアカウント名: `spreadsheet-access`
   - サービスアカウントID: 自動入力される
4. 「作成して続行」をクリック
5. ロールは空白のまま「続行」
6. 「完了」をクリック

### 3-2. キー（JSONファイル）を作成

1. 作成したサービスアカウントをクリック
2. 「キー」タブを選択
3. 「鍵を追加」→「新しい鍵を作成」
4. 「JSON」を選択して「作成」
5. JSONファイルがダウンロードされる

**ダウンロードされたファイル例：**
```
python-spreadsheet-123456-abc123def456.json
```

### 3-3. ファイル名を変更

わかりやすいように名前を変更します。

```
credentials.json
```

**このファイルは秘密情報です。Gitにコミットしないでください。**

---

## Step 4: スプレッドシートにアクセス権を付与

### 4-1. サービスアカウントのメールアドレスを確認

credentials.json を開くと `client_email` があります。

```json
{
  "type": "service_account",
  "client_email": "spreadsheet-access@python-spreadsheet-123456.iam.gserviceaccount.com",
  ...
}
```

### 4-2. スプレッドシートで共有設定

1. 操作したいスプレッドシートを開く
2. 右上の「共有」をクリック
3. サービスアカウントのメールアドレスを入力
4. 権限を「編集者」に設定
5. 「送信」をクリック

```
┌─────────────────────────────────────────────────────────────┐
│  共有設定                                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ユーザーやグループを追加:                                   │
│  spreadsheet-access@python-spreadsheet-123456.iam...        │
│                                                              │
│  権限: [編集者 ▼]                                           │
│                                                              │
│  [送信]                                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**これでPythonからこのスプレッドシートにアクセスできます。**

---

## Step 5: gspreadをインストール

### プロジェクトフォルダの準備

```
spreadsheet_project/
├── venv/
├── credentials.json    ← ダウンロードしたキー
├── main.py
└── requirements.txt
```

### ライブラリのインストール

```
(venv) > pip install gspread google-auth pandas
```

**出力：**
```
Collecting gspread
  Downloading gspread-5.12.0-py3-none-any.whl
Collecting google-auth
  Downloading google_auth-2.25.2-py2.py3-none-any.whl
...
Successfully installed gspread-5.12.0 google-auth-2.25.2 ...
```

### requirements.txtを作成

```
(venv) > pip freeze > requirements.txt
```

---

## Step 6: 基本操作 - 読み込み

### テスト用スプレッドシートを準備

Googleスプレッドシートで以下のようなシートを作成し、サービスアカウントと共有してください。

**シート名: `売上データ`**

| 日付 | 商品 | 数量 | 単価 |
|------|------|------|------|
| 2024/01/01 | 商品A | 10 | 1000 |
| 2024/01/02 | 商品B | 5 | 2000 |
| 2024/01/03 | 商品A | 8 | 1000 |

**スプレッドシートID（URLから取得）：**
```
https://docs.google.com/spreadsheets/d/【このID】/edit
```

### 読み込みコード

```python
# read_sheet.py - スプレッドシートの読み込み
import gspread
from google.oauth2.service_account import Credentials

# 認証設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'credentials.json',
    scopes=SCOPES
)

# gspreadクライアントを作成
gc = gspread.authorize(credentials)

# スプレッドシートを開く（URLのIDを使用）
SPREADSHEET_ID = 'あなたのスプレッドシートID'
spreadsheet = gc.open_by_key(SPREADSHEET_ID)

# シートを選択
worksheet = spreadsheet.worksheet('売上データ')

# 全データを取得
data = worksheet.get_all_values()

print("【全データ】")
for row in data:
    print(row)

print()

# ヘッダー付きで辞書として取得
records = worksheet.get_all_records()

print("【辞書形式】")
for record in records:
    print(record)
```

**出力：**
```
【全データ】
['日付', '商品', '数量', '単価']
['2024/01/01', '商品A', '10', '1000']
['2024/01/02', '商品B', '5', '2000']
['2024/01/03', '商品A', '8', '1000']

【辞書形式】
{'日付': '2024/01/01', '商品': '商品A', '数量': 10, '単価': 1000}
{'日付': '2024/01/02', '商品': '商品B', '数量': 5, '単価': 2000}
{'日付': '2024/01/03', '商品': '商品A', '数量': 8, '単価': 1000}
```

### コード解説

```python
# 認証に必要なスコープ（権限範囲）
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',  # スプレッドシート操作
    'https://www.googleapis.com/auth/drive'          # ドライブアクセス
]

# credentials.jsonを使って認証情報を作成
credentials = Credentials.from_service_account_file(
    'credentials.json',
    scopes=SCOPES
)

# gspreadクライアントを作成（これでAPIにアクセス可能に）
gc = gspread.authorize(credentials)

# スプレッドシートをIDで開く
spreadsheet = gc.open_by_key(SPREADSHEET_ID)

# シート名でワークシートを選択
worksheet = spreadsheet.worksheet('売上データ')

# get_all_values(): 全データをリストのリストで取得
# get_all_records(): ヘッダー行をキーにした辞書のリストで取得
```

---

## Step 7: 基本操作 - 書き込み

### 書き込みコード

```python
# write_sheet.py - スプレッドシートへの書き込み
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 認証設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'credentials.json',
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

SPREADSHEET_ID = 'あなたのスプレッドシートID'
spreadsheet = gc.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.worksheet('売上データ')

# 1. 特定のセルに書き込み
worksheet.update_acell('E1', '金額')
print("E1に「金額」を書き込みました")

# 2. 行を追加
new_row = ['2024/01/04', '商品C', 7, 1500]
worksheet.append_row(new_row)
print(f"新しい行を追加しました: {new_row}")

# 3. 範囲で書き込み（複数セル一括）
values = [
    ['処理日時', datetime.now().strftime('%Y/%m/%d %H:%M:%S')],
    ['ステータス', '完了']
]
worksheet.update('G1:H2', values)
print("G1:H2に情報を書き込みました")

# 4. 書き込み後のデータを確認
print("\n【更新後のデータ】")
data = worksheet.get_all_values()
for row in data:
    print(row)
```

**出力：**
```
E1に「金額」を書き込みました
新しい行を追加しました: ['2024/01/04', '商品C', 7, 1500]
G1:H2に情報を書き込みました

【更新後のデータ】
['日付', '商品', '数量', '単価', '金額', '', '処理日時', '2024/01/15 14:30:45']
['2024/01/01', '商品A', '10', '1000', '', '', 'ステータス', '完了']
['2024/01/02', '商品B', '5', '2000', '', '', '', '']
['2024/01/03', '商品A', '8', '1000', '', '', '', '']
['2024/01/04', '商品C', '7', '1500', '', '', '', '']
```

### 書き込みメソッドの比較

| メソッド | 用途 | 例 |
|----------|------|-----|
| `update_acell('A1', '値')` | 単一セル | `worksheet.update_acell('A1', 'Hello')` |
| `append_row([...])` | 最終行に追加 | `worksheet.append_row(['a', 'b', 'c'])` |
| `update('A1:C2', [[...]])` | 範囲指定 | `worksheet.update('A1:C2', values)` |
| `update_cell(row, col, '値')` | 行列番号で指定 | `worksheet.update_cell(1, 1, 'A1')` |

---

## Step 8: pandasとの連携

### pandasでデータを読み込む

```python
# pandas_read.py - pandasでスプレッドシートを読み込み
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 認証設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'credentials.json',
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

SPREADSHEET_ID = 'あなたのスプレッドシートID'
spreadsheet = gc.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.worksheet('売上データ')

# スプレッドシート → pandas DataFrame
records = worksheet.get_all_records()
df = pd.DataFrame(records)

print("【DataFrameとして取得】")
print(df)
print()

# pandasで集計
print("【商品別売上】")
df['金額'] = df['数量'] * df['単価']
summary = df.groupby('商品')['金額'].sum()
print(summary)
```

**出力：**
```
【DataFrameとして取得】
         日付    商品  数量   単価
0  2024/01/01  商品A    10  1000
1  2024/01/02  商品B     5  2000
2  2024/01/03  商品A     8  1000
3  2024/01/04  商品C     7  1500

【商品別売上】
商品
商品A    18000
商品B    10000
商品C    10500
Name: 金額, dtype: int64
```

### pandasの結果をスプレッドシートに書き込む

```python
# pandas_write.py - 処理結果をスプレッドシートに書き込み
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 認証設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'credentials.json',
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

SPREADSHEET_ID = 'あなたのスプレッドシートID'
spreadsheet = gc.open_by_key(SPREADSHEET_ID)

# 元データを読み込み
worksheet_source = spreadsheet.worksheet('売上データ')
records = worksheet_source.get_all_records()
df = pd.DataFrame(records)

# pandasで集計
df['金額'] = df['数量'] * df['単価']
summary = df.groupby('商品').agg({
    '数量': 'sum',
    '金額': 'sum'
}).reset_index()

print("【集計結果】")
print(summary)

# 新しいシートを作成（または既存シートを使用）
try:
    worksheet_result = spreadsheet.worksheet('集計結果')
    worksheet_result.clear()  # 既存データをクリア
except gspread.exceptions.WorksheetNotFound:
    worksheet_result = spreadsheet.add_worksheet(title='集計結果', rows=100, cols=20)

# DataFrameをスプレッドシートに書き込み
# ヘッダー + データを結合
header = summary.columns.tolist()
values = summary.values.tolist()
all_data = [header] + values

worksheet_result.update('A1', all_data)

print("\n「集計結果」シートに書き込みました！")
```

**出力：**
```
【集計結果】
    商品  数量    金額
0  商品A    18  18000
1  商品B     5  10000
2  商品C     7  10500

「集計結果」シートに書き込みました！
```

---

## GASとgspreadの比較

```javascript
// GAS: スプレッドシートの読み込み
function readSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('売上データ');
  const data = sheet.getDataRange().getValues();
  Logger.log(data);
}
```

```python
# Python + gspread: スプレッドシートの読み込み
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
gc = gspread.authorize(credentials)

spreadsheet = gc.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.worksheet('売上データ')
data = worksheet.get_all_values()
print(data)
```

```
┌─────────────────────────────────────────────────────────────┐
│  比較                                                        │
├──────────────────┬────────────────────┬─────────────────────┤
│  項目            │  GAS               │  gspread            │
├──────────────────┼────────────────────┼─────────────────────┤
│  認証            │  不要              │  サービスアカウント │
│  セットアップ    │  なし              │  GCP設定が必要      │
│  コード量        │  少ない            │  やや多い           │
│  データ処理      │  限定的            │  pandas連携可能     │
│  実行時間制限    │  6分               │  なし               │
│  ローカル実行    │  不可              │  可能               │
└──────────────────┴────────────────────┴─────────────────────┘
```

---

## よくあるエラーと対処法

### エラー1: APIが有効化されていない

```
google.api_core.exceptions.PermissionDenied: 403 Google Sheets API has not been enabled
```

**対処法：** GCPコンソールで「Google Sheets API」を有効化

### エラー2: スプレッドシートへのアクセス権限がない

```
gspread.exceptions.SpreadsheetNotFound: Spreadsheet not found
```

**対処法：**
1. スプレッドシートIDが正しいか確認
2. サービスアカウントのメールアドレスでスプレッドシートを共有

### エラー3: credentials.jsonが見つからない

```
FileNotFoundError: [Errno 2] No such file or directory: 'credentials.json'
```

**対処法：**
1. credentials.jsonがスクリプトと同じフォルダにあるか確認
2. ファイル名が正しいか確認

### エラー4: APIの呼び出し制限

```
gspread.exceptions.APIError: {'code': 429, 'message': 'Quota exceeded'}
```

**対処法：**
1. 短時間に大量のリクエストを送らない
2. ループ内で `time.sleep(1)` を入れる
3. バッチ処理（`update()`で一括更新）を使う

---

## この節のまとめ

- GCPでプロジェクト作成 → API有効化 → サービスアカウント作成
- credentials.jsonをダウンロードして保管
- スプレッドシートをサービスアカウントと共有
- gspreadで読み込み・書き込み
- pandasと連携することで強力なデータ処理が可能

**次の節では、GASをWebAPIとして使う方法（発展）を学びます。**
