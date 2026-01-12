# GAS×Python連携方法リサーチ

## 1. 連携パターン概要

| パターン | 方法 | 難易度 | 用途 |
|----------|------|--------|------|
| **A** | Python → スプレッドシート（gspread直接） | ★★☆ | **メインで扱う** |
| **B** | Python → GAS（WebAPI）→ スプレッドシート | ★★★ | 既存GAS活用 |
| **C** | GAS → Python（Pythonサーバー必要） | ★★★★ | 上級者向け |

---

## 2. パターンA: gspreadでPythonから直接スプレッドシート操作

### 概要

```
Python（gspread）→ Google Sheets API → スプレッドシート
```

**特徴:**
- 最も実用的
- 情報源が豊富
- GASを介さない直接アクセス

### 必要な設定

1. **GCPプロジェクト作成**
2. **API有効化**
   - Google Sheets API
   - Google Drive API
3. **サービスアカウント作成**
4. **JSONキーファイル取得**
5. **スプレッドシートの共有設定**

### 設定手順

#### Step 1: GCPプロジェクト作成

```
1. Google Cloud Console にアクセス
2. 「プロジェクトの選択」→「新しいプロジェクト」
3. プロジェクト名を入力（例：python-sheet-demo）
4. 「作成」
```

#### Step 2: API有効化

```
1. 左メニュー「APIとサービス」→「ライブラリ」
2. 「Google Sheets API」を検索して有効化
3. 「Google Drive API」を検索して有効化
```

#### Step 3: サービスアカウント作成

```
1. 「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「サービスアカウント」
3. 名前と説明を入力
4. ロール：「編集者」を選択
5. 「完了」
```

#### Step 4: JSONキー取得

```
1. 作成したサービスアカウントをクリック
2. 「鍵」タブ
3. 「鍵を追加」→「新しい鍵を作成」→「JSON」
4. JSONファイルがダウンロードされる
```

#### Step 5: スプレッドシート共有

```
1. JSONファイル内の「client_email」を確認
2. スプレッドシートを開く
3. 「共有」→ client_emailを追加（編集権限）
```

### Pythonコード例

```python
# インストール
# pip install gspread

import gspread
from google.oauth2.service_account import Credentials

# 認証設定
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'service_account.json',  # ダウンロードしたJSONファイル
    scopes=scopes
)

gc = gspread.authorize(credentials)

# スプレッドシートを開く
spreadsheet = gc.open('ファイル名')
# または URL で開く
# spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/...')

# シートを選択
worksheet = spreadsheet.sheet1
# または名前で指定
# worksheet = spreadsheet.worksheet('シート名')

# 読み込み
value = worksheet.acell('A1').value  # 単一セル
values = worksheet.get_all_values()   # 全データ
row = worksheet.row_values(1)         # 行
col = worksheet.col_values(1)         # 列

# 書き込み
worksheet.update_cell(1, 1, '値')     # 単一セル
worksheet.append_row(['A', 'B', 'C']) # 行追加
worksheet.update('A1:C3', [[1,2,3],[4,5,6],[7,8,9]])  # 範囲
```

### 情報源

| サイト | URL | 特徴 |
|--------|-----|------|
| たぬハック | tanuhack.com/library-gspread/ | 使い方まとめ |
| 理想の働き方研究室 | pepenoheya.blog | 認証設定詳細 |
| ジコログ | self-development.info | インストール解説 |
| Zenn | zenn.dev/yamagishihrd | 設定手順 |

---

## 3. パターンB: GASをWebAPIとして使う

### 概要

```
Python → HTTP POST → GAS（doPost関数）→ スプレッドシート
```

**特徴:**
- 既存GASスクリプトを活かせる
- GAS側の処理も実行可能
- URL公開が必要

### GAS側コード

```javascript
function doPost(e) {
  // POSTデータを取得
  const data = JSON.parse(e.postData.contents);
  
  // スプレッドシートを開く
  const ss = SpreadsheetApp.openById('スプレッドシートID');
  const sheet = ss.getSheetByName('シート名');
  
  // データを追加
  sheet.appendRow([data.name, data.email, new Date()]);
  
  // レスポンス
  return ContentService.createTextOutput('Success');
}
```

### GASデプロイ手順

```
1. 「デプロイ」→「新しいデプロイ」
2. 「種類の選択」→「ウェブアプリ」
3. 「アクセスできるユーザー」→「全員」
4. 「デプロイ」
5. URLをコピー
```

### Python側コード

```python
import requests
import json

# GASのデプロイURL
url = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"

# 送信データ
data = {
    "name": "太郎",
    "email": "taro@example.com"
}

# POSTリクエスト
response = requests.post(
    url,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)

print(response.text)
```

### 情報源

| サイト | URL | 特徴 |
|--------|-----|------|
| odndo | odndo.com/posts/1628829322483/ | Python→GAS POST解説 |
| Qiita | qiita.com/ema_kurida | ChatGPT+GAS連携 |

---

## 4. パターンC: GAS → Python（制限あり）

### 結論

**GASからローカルPythonを直接呼び出すことは不可能**

### 可能な方法

```
GAS → UrlFetchApp → Pythonサーバー（Flask等）
```

**必要な条件:**
- Pythonをサーバーとして公開
- 固定IPまたはドメイン
- ポート開放

### Pythonサーバー例（Flask）

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    # 処理
    result = process_data(data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### GAS側コード

```javascript
function callPythonAPI() {
  const payload = {
    value: 'GASから送信されたデータ'
  };
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };
  
  const response = UrlFetchApp.fetch(
    'http://your-server-address:5000/receive',
    options
  );
  
  Logger.log(response.getContentText());
}
```

### 情報源

| サイト | URL | 特徴 |
|--------|-----|------|
| monoblog | monoblog.jp/archives/5861 | 制限の解説 |
| あっと寝てく？ | atnettec.com | 双方向連携 |

---

## 5. 本講座での扱い方

### 第5章カリキュラム

```
5-2. PythonからスプレッドシートをDirectに操作（gspread）
├── GCP設定：サービスアカウント作成
├── gspreadインストールと認証
├── 読み書きの基本操作
└── 【実践】スクレイピング結果をスプレッドシートに自動記録

5-3. GASをWebAPIとして使う（発展）
├── doPost関数でデータ受け取り
├── PythonからPOSTリクエスト送信
└── 既存GASスクリプトを活かす方法
```

### 優先度

| パターン | 優先度 | 理由 |
|----------|--------|------|
| A（gspread） | **高** | 最も実用的、初心者にも扱いやすい |
| B（GAS WebAPI） | 中 | 既存GAS資産がある場合に有効 |
| C（GAS→Python） | 低 | サーバー必要、上級者向け |

---

## 6. gspread APIリファレンス（抜粋）

### ワークブック操作

```python
# 開く
gc.open('ファイル名')
gc.open_by_url('URL')
gc.open_by_key('スプレッドシートID')

# 作成
gc.create('新しいスプレッドシート')
```

### シート操作

```python
# 選択
spreadsheet.sheet1
spreadsheet.worksheet('シート名')
spreadsheet.get_worksheet(0)  # インデックス

# シート一覧
spreadsheet.worksheets()

# 追加・削除
spreadsheet.add_worksheet(title='新シート', rows=100, cols=20)
spreadsheet.del_worksheet(worksheet)
```

### セル操作

```python
# 読み込み
worksheet.acell('A1').value
worksheet.cell(1, 1).value
worksheet.get('A1:C3')
worksheet.get_all_values()
worksheet.get_all_records()
worksheet.row_values(1)
worksheet.col_values(1)

# 書き込み
worksheet.update_cell(1, 1, '値')
worksheet.update_acell('A1', '値')
worksheet.update('A1:C3', [[1,2,3],[4,5,6],[7,8,9]])
worksheet.append_row(['A', 'B', 'C'])
worksheet.insert_row(['A', 'B', 'C'], 1)

# 削除
worksheet.delete_rows(2)
worksheet.delete_rows(2, 5)  # 2〜5行目
```

### 検索

```python
# セル検索
worksheet.find('検索文字列')
worksheet.findall('検索文字列')
```
