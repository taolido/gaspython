# 5-3. GASをWebAPIとして使う（発展）

## この節で学ぶこと

- GASをWebAPIとして公開する方法
- PythonからGAS WebAPIを呼び出す
- 既存のGASスクリプトを活かす方法
- gspreadとWebAPIの使い分け

---

## この方法が有効なケース

```
┌─────────────────────────────────────────────────────────────┐
│  GAS WebAPIが有効なケース                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ 既にGASスクリプトがあり、それを活かしたい               │
│  ✓ GASでしかできない処理がある（Gmail送信、カレンダー操作）│
│  ✓ GCPの設定を避けたい（サービスアカウントを作りたくない） │
│  ✓ 複雑な認証設定をしたくない                              │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  gspreadで十分なケース                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ スプレッドシートの読み書きだけしたい                    │
│  ✓ pandas連携が必要                                         │
│  ✓ 大量データを効率的に処理したい                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 仕組みの概要

```
┌─────────────────────────────────────────────────────────────┐
│  GAS WebAPIの仕組み                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Python              インターネット              GAS        │
│  スクリプト          (HTTPS)                     スクリプト  │
│                                                              │
│  ┌─────────┐         ┌─────────┐              ┌──────────┐ │
│  │ requests │ ──────→│  WebApp │ ───────────→│ doPost() │ │
│  │ .post()  │   POST  │   URL   │              │          │ │
│  │          │ ←──────│         │←────────────│ return   │ │
│  └─────────┘   JSON   └─────────┘    JSON     └──────────┘ │
│                                                              │
│  ※ GASをウェブアプリとしてデプロイするとURLが発行される   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: GAS側 - WebAPIを作成

### GASコード（Code.gs）

```javascript
// doGet: GETリクエストを受け取る
function doGet(e) {
  const response = {
    status: 'ok',
    message: 'Hello from GAS!',
    timestamp: new Date().toISOString()
  };

  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

// doPost: POSTリクエストを受け取る
function doPost(e) {
  try {
    // リクエストボディをパース
    const data = JSON.parse(e.postData.contents);

    // 受け取ったデータを処理
    const action = data.action;
    let result;

    switch (action) {
      case 'add_row':
        result = addRowToSheet(data);
        break;
      case 'get_data':
        result = getSheetData(data);
        break;
      case 'send_email':
        result = sendEmail(data);
        break;
      default:
        result = { error: 'Unknown action: ' + action };
    }

    return ContentService
      .createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ error: error.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// スプレッドシートに行を追加
function addRowToSheet(data) {
  const ss = SpreadsheetApp.openById(data.spreadsheet_id);
  const sheet = ss.getSheetByName(data.sheet_name);

  sheet.appendRow(data.row);

  return {
    status: 'ok',
    message: '行を追加しました',
    row: data.row
  };
}

// スプレッドシートからデータを取得
function getSheetData(data) {
  const ss = SpreadsheetApp.openById(data.spreadsheet_id);
  const sheet = ss.getSheetByName(data.sheet_name);

  const values = sheet.getDataRange().getValues();

  return {
    status: 'ok',
    data: values
  };
}

// メールを送信
function sendEmail(data) {
  GmailApp.sendEmail(
    data.to,
    data.subject,
    data.body
  );

  return {
    status: 'ok',
    message: 'メールを送信しました',
    to: data.to
  };
}
```

### コード解説

```javascript
// doPost: POSTリクエストが来たときに呼ばれる関数
function doPost(e) {
  // e.postData.contents にリクエストボディが入っている
  const data = JSON.parse(e.postData.contents);

  // 処理...

  // JSONでレスポンスを返す
  return ContentService
    .createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
```

---

## Step 2: GAS側 - ウェブアプリとしてデプロイ

### デプロイ手順

1. GASエディタで「デプロイ」→「新しいデプロイ」
2. 種類で「ウェブアプリ」を選択
3. 以下を設定：
   - 説明: 任意（例: Python連携API）
   - 次のユーザーとして実行: 自分
   - アクセスできるユーザー: 全員

```
┌─────────────────────────────────────────────────────────────┐
│  新しいデプロイ                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  種類を選択: ウェブアプリ                                    │
│                                                              │
│  説明: Python連携API                                         │
│                                                              │
│  次のユーザーとして実行: 自分（your.email@gmail.com）       │
│                                                              │
│  アクセスできるユーザー: 全員                                │
│  ※ Googleアカウントなしでもアクセス可能                    │
│                                                              │
│  [デプロイ]                                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

4. 「デプロイ」をクリック
5. ウェブアプリのURLが表示される

```
ウェブアプリ URL:
https://script.google.com/macros/s/AKfycbx.../exec
```

**このURLをPythonから呼び出します。**

---

## Step 3: Python側 - WebAPIを呼び出す

### 必要なライブラリ

```
(venv) > pip install requests
```

### 基本的なリクエスト

```python
# call_gas_api.py - GAS WebAPIを呼び出す
import requests
import json

# GAS WebAppのURL（デプロイ時に取得したURL）
GAS_URL = 'https://script.google.com/macros/s/AKfycbx.../exec'

# 1. GETリクエスト
print("【GETリクエスト】")
response = requests.get(GAS_URL)
print(response.json())
print()

# 2. POSTリクエスト（データを送信）
print("【POSTリクエスト - スプレッドシートにデータ追加】")
data = {
    'action': 'add_row',
    'spreadsheet_id': 'あなたのスプレッドシートID',
    'sheet_name': '売上データ',
    'row': ['2024/01/15', '商品D', 20, 500]
}

response = requests.post(
    GAS_URL,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)

print(response.json())
```

**出力：**
```
【GETリクエスト】
{'status': 'ok', 'message': 'Hello from GAS!', 'timestamp': '2024-01-15T05:30:45.123Z'}

【POSTリクエスト - スプレッドシートにデータ追加】
{'status': 'ok', 'message': '行を追加しました', 'row': ['2024/01/15', '商品D', 20, 500]}
```

---

## Step 4: 実践例 - データ取得とメール送信

### スプレッドシートのデータを取得

```python
# get_data_from_gas.py
import requests
import json
import pandas as pd

GAS_URL = 'https://script.google.com/macros/s/AKfycbx.../exec'

# スプレッドシートからデータを取得
data = {
    'action': 'get_data',
    'spreadsheet_id': 'あなたのスプレッドシートID',
    'sheet_name': '売上データ'
}

response = requests.post(
    GAS_URL,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)

result = response.json()

if result.get('status') == 'ok':
    # データをpandas DataFrameに変換
    values = result['data']
    df = pd.DataFrame(values[1:], columns=values[0])  # 1行目がヘッダー

    print("【取得したデータ】")
    print(df)

    # pandasで集計
    df['数量'] = pd.to_numeric(df['数量'])
    df['単価'] = pd.to_numeric(df['単価'])
    df['金額'] = df['数量'] * df['単価']

    print("\n【合計売上】")
    print(f"{df['金額'].sum():,}円")
else:
    print(f"エラー: {result.get('error')}")
```

**出力：**
```
【取得したデータ】
         日付    商品 数量  単価
0  2024/01/01  商品A   10  1000
1  2024/01/02  商品B    5  2000
2  2024/01/03  商品A    8  1000
3  2024/01/15  商品D   20   500

【合計売上】
38,000円
```

### 処理結果をメールで送信

```python
# send_report_email.py
import requests
import json
import pandas as pd

GAS_URL = 'https://script.google.com/macros/s/AKfycbx.../exec'

# 1. データを取得
get_data = {
    'action': 'get_data',
    'spreadsheet_id': 'あなたのスプレッドシートID',
    'sheet_name': '売上データ'
}

response = requests.post(
    GAS_URL,
    data=json.dumps(get_data),
    headers={'Content-Type': 'application/json'}
)

result = response.json()
values = result['data']
df = pd.DataFrame(values[1:], columns=values[0])

# 2. pandasで集計
df['数量'] = pd.to_numeric(df['数量'])
df['単価'] = pd.to_numeric(df['単価'])
df['金額'] = df['数量'] * df['単価']

summary = df.groupby('商品')['金額'].sum()
total = df['金額'].sum()

# 3. メール本文を作成
body = f"""売上レポート

【商品別売上】
{summary.to_string()}

【合計売上】
{total:,}円

※ このメールはPythonから自動送信されました。
"""

print("【メール本文】")
print(body)

# 4. GAS経由でメール送信
send_data = {
    'action': 'send_email',
    'to': 'report@example.com',
    'subject': '【自動レポート】売上集計',
    'body': body
}

response = requests.post(
    GAS_URL,
    data=json.dumps(send_data),
    headers={'Content-Type': 'application/json'}
)

print("\n【送信結果】")
print(response.json())
```

**出力：**
```
【メール本文】
売上レポート

【商品別売上】
商品
商品A    18000
商品B    10000
商品D    10000
Name: 金額, dtype: int64

【合計売上】
38,000円

※ このメールはPythonから自動送信されました。

【送信結果】
{'status': 'ok', 'message': 'メールを送信しました', 'to': 'report@example.com'}
```

---

## gspread vs GAS WebAPI

```
┌─────────────────────────────────────────────────────────────┐
│  どちらを使うべきか                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  gspreadを選ぶケース:                                        │
│  ・スプレッドシートの読み書きが中心                         │
│  ・pandas連携が必要                                          │
│  ・大量データの処理                                          │
│  ・GCPの設定ができる                                         │
│                                                              │
│  GAS WebAPIを選ぶケース:                                     │
│  ・既存のGASスクリプトを活かしたい                          │
│  ・Gmail、カレンダーなどGAS特有の機能を使う                 │
│  ・GCPの設定を避けたい                                       │
│  ・認証なしで呼び出したい                                    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  両方使うケース:                                             │
│                                                              │
│  ・gspreadでデータ取得・処理                                 │
│  ・GAS WebAPIでメール送信やカレンダー登録                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## セキュリティ上の注意

### 1. URLの管理

```
┌─────────────────────────────────────────────────────────────┐
│  ウェブアプリのURLは秘密にする                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ・URLを知っていれば誰でもアクセスできる                    │
│  ・Gitにコミットしない                                       │
│  ・環境変数やconfigファイルで管理                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**推奨: 環境変数で管理**

```python
import os

GAS_URL = os.environ.get('GAS_WEBAPP_URL')
if not GAS_URL:
    raise ValueError('GAS_WEBAPP_URL environment variable is not set')
```

### 2. 入力値の検証（GAS側）

```javascript
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    // 必須パラメータの検証
    if (!data.action) {
      throw new Error('action is required');
    }

    // 許可されたactionのみ受け付ける
    const allowedActions = ['add_row', 'get_data', 'send_email'];
    if (!allowedActions.includes(data.action)) {
      throw new Error('Invalid action');
    }

    // 処理...

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ error: error.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

### 3. アクセス制限

```
デプロイ設定で「アクセスできるユーザー」を制限:

・全員: URLを知っていれば誰でもアクセス可能
・自分のみ: 開発・テスト用
・組織内のユーザー: Google Workspaceの同じ組織のユーザーのみ
```

---

## よくあるエラーと対処法

### エラー1: デプロイ後にコード変更が反映されない

```
コードを修正したのに、動作が変わらない
```

**対処法：**
1. 「デプロイ」→「デプロイを管理」
2. 新しいバージョンをデプロイ
3. URLは変わらないが、コードが更新される

### エラー2: CORS エラー（ブラウザから直接呼び出す場合）

```
Access to fetch at 'https://script.google.com/...' has been blocked by CORS policy
```

**対処法：**
ブラウザのJavaScriptから直接呼び出す場合は、GAS側でCORS対応が必要。
Pythonからの呼び出しでは発生しません。

### エラー3: 認証エラー

```
{"error":"Script function not found: doPost"}
```

**対処法：**
1. GASのコードに `doPost` 関数があるか確認
2. 再デプロイして新しいバージョンを公開

### エラー4: タイムアウト

```
requests.exceptions.ReadTimeout
```

**対処法：**
```python
# タイムアウト時間を延長
response = requests.post(
    GAS_URL,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'},
    timeout=60  # 60秒
)
```

---

## この節のまとめ

- GASを「ウェブアプリ」としてデプロイするとURLが発行される
- Pythonから `requests` でPOST/GETリクエストを送信
- 既存のGASスクリプトを活かしながらPythonの処理能力を使える
- Gmail、カレンダーなどGAS特有の機能をPythonから呼び出せる
- URLの管理と入力値の検証に注意

**次の節では、Python学習の次のステップと、業界別の活用アイデアを紹介します。**
