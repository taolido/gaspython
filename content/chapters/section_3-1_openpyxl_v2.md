# 3-1. openpyxl入門：Excelファイルを読み書き

Pythonで Excel ファイル（.xlsx）を操作する方法を学びます。
**このセクションのコードはすべてColabでコピペして動きます。**

---

## このセクションのゴール

- openpyxlをインストールして使えるようにする
- Excelファイルを読み込んでデータを取り出す
- 新しいExcelファイルを作成して保存する
- GASのスプレッドシート操作との違いを理解する

所要時間：約20分

---

## openpyxlとは

**openpyxl**（オープン・パイ・エクセル）は、PythonでExcelファイルを操作するライブラリです。

GASで `SpreadsheetApp` を使ってスプレッドシートを操作したように、openpyxlを使えばPythonでExcelを自由に操作できます。

### GASとの対応関係

| GAS | openpyxl | 説明 |
|-----|----------|------|
| SpreadsheetApp | openpyxl | ライブラリ本体 |
| Spreadsheet | Workbook | ファイル全体 |
| Sheet | Worksheet | シート |
| Range | Cell | セル |

---

## Step 1：openpyxlをインストールする

Colabにはopenpyxlが入っていないので、最初にインストールします。

```python
# ===================================================
# Step 1: openpyxlをインストールする
# Colabで最初に1回だけ実行すればOK
# ===================================================

!pip install openpyxl
```

**実行結果：**
```
Collecting openpyxl
  Downloading openpyxl-3.1.2-py2.py3-none-any.whl (249 kB)
Successfully installed openpyxl-3.1.2
```

> **GAS経験者へ**
>
> GASでは「インストール」という概念がありませんでした。`SpreadsheetApp`は最初から使えましたよね。
>
> Pythonでは、標準ライブラリ以外は`pip install`でインストールが必要です。
>
> Colabの場合、セッションが切れる（ブラウザを閉じる等）と再インストールが必要になります。
> でも心配いりません。上のコマンドを再実行するだけです。

---

## Step 2：練習用のExcelファイルを作る

まず、練習用のExcelファイルを作成します。

```python
# ===================================================
# Step 2: 練習用のExcelファイルを作る
# このコードを実行すると「社員名簿.xlsx」が作られます
# ===================================================

import openpyxl

# 新しいワークブック（Excelファイル）を作成
wb = openpyxl.Workbook()

# アクティブなシートを取得（新規作成時は「Sheet」という名前）
ws = wb.active

# シート名を変更
ws.title = "社員一覧"

# ヘッダー行を入力
ws['A1'] = '社員ID'
ws['B1'] = '名前'
ws['C1'] = '部署'
ws['D1'] = '年齢'
ws['E1'] = '入社年'

# データを入力
employees = [
    ['E001', '田中太郎', '営業部', 28, 2020],
    ['E002', '佐藤花子', '開発部', 32, 2018],
    ['E003', '鈴木一郎', '総務部', 25, 2023],
    ['E004', '高橋美咲', '営業部', 30, 2019],
    ['E005', '伊藤健太', '開発部', 27, 2021],
    ['E006', '渡辺由美', '総務部', 35, 2015],
    ['E007', '山本大輔', '営業部', 29, 2020],
    ['E008', '中村さくら', '開発部', 26, 2022],
]

# 2行目からデータを書き込み
for i, emp in enumerate(employees, start=2):
    ws[f'A{i}'] = emp[0]  # 社員ID
    ws[f'B{i}'] = emp[1]  # 名前
    ws[f'C{i}'] = emp[2]  # 部署
    ws[f'D{i}'] = emp[3]  # 年齢
    ws[f'E{i}'] = emp[4]  # 入社年

# ファイルを保存
wb.save('社員名簿.xlsx')

print("✓ 社員名簿.xlsx を作成しました")
print(f"  シート名: {ws.title}")
print(f"  データ件数: {len(employees)}件")
```

**実行結果：**
```
✓ 社員名簿.xlsx を作成しました
  シート名: 社員一覧
  データ件数: 8件
```

### コード解説

```python
import openpyxl
```
openpyxlライブラリを読み込みます。`pip install`後でないとエラーになります。

```python
wb = openpyxl.Workbook()
```
新しいワークブック（Excelファイル）を作成します。
- GASでいう `SpreadsheetApp.create()` に相当
- この時点ではまだファイルは保存されていない（メモリ上にあるだけ）

```python
ws = wb.active
```
アクティブなシートを取得します。新規作成時は自動的に1つシートができています。
- GASでいう `ss.getActiveSheet()` に相当

```python
ws['A1'] = '社員ID'
```
A1セルに値を設定します。
- GASでいう `sheet.getRange('A1').setValue('社員ID')` に相当
- **openpyxlの方がシンプル！**

```python
for i, emp in enumerate(employees, start=2):
```
- `enumerate()`: リストをループしながらインデックス（番号）も取得
- `start=2`: インデックスを2から始める（1行目はヘッダーなので）

```python
wb.save('社員名簿.xlsx')
```
ファイルを保存します。
- **重要：これを忘れると保存されない！**
- GASは自動保存ですが、openpyxlは明示的に`save()`が必要

---

## Step 3：Excelファイルを読み込む

作成したExcelファイルを読み込んでみましょう。

```python
# ===================================================
# Step 3: Excelファイルを読み込む
# ===================================================

import openpyxl

# Excelファイルを開く
wb = openpyxl.load_workbook('社員名簿.xlsx')

# 基本情報を確認
print("=== ファイル情報 ===")
print(f"シート一覧: {wb.sheetnames}")
print(f"シート数: {len(wb.sheetnames)}")
print()

# シートを取得
ws = wb['社員一覧']

# シートの情報
print("=== シート情報 ===")
print(f"シート名: {ws.title}")
print(f"最終行: {ws.max_row}行")
print(f"最終列: {ws.max_column}列")
```

**実行結果：**
```
=== ファイル情報 ===
シート一覧: ['社員一覧']
シート数: 1

=== シート情報 ===
シート名: 社員一覧
最終行: 9行
最終列: 5列
```

### コード解説

```python
wb = openpyxl.load_workbook('社員名簿.xlsx')
```
既存のExcelファイルを開きます。
- GASでいう `SpreadsheetApp.openById()` に相当
- ファイルが存在しないとエラーになる

```python
wb.sheetnames
```
ワークブック内のすべてのシート名をリストで取得します。
- GASでいう `ss.getSheets().map(s => s.getName())` に相当

```python
ws = wb['社員一覧']
```
シート名を指定してシートを取得します。
- GASでいう `ss.getSheetByName('社員一覧')` に相当
- 存在しないシート名を指定するとエラー

```python
ws.max_row
ws.max_column
```
データが入っている最終行・最終列を取得します。
- GASでいう `sheet.getLastRow()` / `sheet.getLastColumn()` に相当

---

## Step 4：セルの値を読み取る

セルから値を取得する方法を学びます。

```python
# ===================================================
# Step 4: セルの値を読み取る
# ===================================================

import openpyxl

wb = openpyxl.load_workbook('社員名簿.xlsx')
ws = wb['社員一覧']

# ----- 方法1: A1形式で指定 -----
print("=== 方法1: A1形式 ===")
cell_a1 = ws['A1']
print(f"A1セルの値: {cell_a1.value}")
print(f"B2セルの値: {ws['B2'].value}")
print()

# ----- 方法2: 行番号・列番号で指定 -----
print("=== 方法2: 行番号・列番号（1から始まる） ===")
cell = ws.cell(row=1, column=1)
print(f"1行1列の値: {cell.value}")
cell2 = ws.cell(row=2, column=2)
print(f"2行2列の値: {cell2.value}")
print()

# ----- 方法3: 範囲を指定して複数セルを取得 -----
print("=== 方法3: 範囲指定 ===")
print("A1:B3の範囲:")
for row in ws['A1:B3']:
    for cell in row:
        print(f"  {cell.coordinate}: {cell.value}")
```

**実行結果：**
```
=== 方法1: A1形式 ===
A1セルの値: 社員ID
B2セルの値: 田中太郎

=== 方法2: 行番号・列番号（1から始まる） ===
1行1列の値: 社員ID
2行2列の値: 田中太郎

=== 方法3: 範囲指定 ===
A1:B3の範囲:
  A1: 社員ID
  B1: 名前
  A2: E001
  B2: 田中太郎
  A3: E002
  B3: 佐藤花子
```

### GASとの比較

| 操作 | GAS | openpyxl |
|------|-----|----------|
| A1セルの値を取得 | `sheet.getRange('A1').getValue()` | `ws['A1'].value` |
| 行列番号で取得 | `sheet.getRange(1, 1).getValue()` | `ws.cell(row=1, column=1).value` |
| 範囲を取得 | `sheet.getRange('A1:B3').getValues()` | `ws['A1:B3']`（ループが必要） |

**openpyxlの方がシンプル！** `.getRange().getValue()` が `['A1'].value` で済みます。

---

## Step 5：全データをループで読み取る

実務では、全データをループで処理することが多いです。

```python
# ===================================================
# Step 5: 全データをループで読み取る
# ===================================================

import openpyxl

wb = openpyxl.load_workbook('社員名簿.xlsx')
ws = wb['社員一覧']

# ----- 方法1: iter_rows() を使う（推奨） -----
print("=== 全データを読み取り ===")
print()

# ヘッダー行（1行目）
headers = []
for cell in ws[1]:  # 1行目を取得
    headers.append(cell.value)
print(f"ヘッダー: {headers}")
print()

# データ行（2行目以降）
print("【社員データ】")
for row in ws.iter_rows(min_row=2, values_only=True):
    emp_id, name, dept, age, year = row
    print(f"  {emp_id}: {name}（{dept}、{age}歳、{year}年入社）")
```

**実行結果：**
```
=== 全データを読み取り ===

ヘッダー: ['社員ID', '名前', '部署', '年齢', '入社年']

【社員データ】
  E001: 田中太郎（営業部、28歳、2020年入社）
  E002: 佐藤花子（開発部、32歳、2018年入社）
  E003: 鈴木一郎（総務部、25歳、2023年入社）
  E004: 高橋美咲（営業部、30歳、2019年入社）
  E005: 伊藤健太（開発部、27歳、2021年入社）
  E006: 渡辺由美（総務部、35歳、2015年入社）
  E007: 山本大輔（営業部、29歳、2020年入社）
  E008: 中村さくら（開発部、26歳、2022年入社）
```

### コード解説

```python
ws.iter_rows(min_row=2, values_only=True)
```
- `iter_rows()`: 行ごとにループする
- `min_row=2`: 2行目から開始（ヘッダーをスキップ）
- `values_only=True`: セルオブジェクトではなく、値だけを取得

```python
emp_id, name, dept, age, year = row
```
タプル（行データ）を変数に分解しています。
- `row` は `('E001', '田中太郎', '営業部', 28, 2020)` のようなタプル
- これを5つの変数に一度に代入

### GASとの比較

**GASの場合：**
```javascript
function readAllData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('社員一覧');
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(2, 1, lastRow - 1, 5).getValues();

  data.forEach(row => {
    const [empId, name, dept, age, year] = row;
    console.log(`${empId}: ${name}（${dept}、${age}歳、${year}年入社）`);
  });
}
```

**Pythonの場合：**
```python
for row in ws.iter_rows(min_row=2, values_only=True):
    emp_id, name, dept, age, year = row
    print(f"{emp_id}: {name}（{dept}、{age}歳、{year}年入社）")
```

行数はほぼ同じですが、Pythonの方が `getRange()` の指定が不要でシンプルです。

---

## Step 6：データをリストに格納する

読み取ったデータをリストに格納して、後で使えるようにします。

```python
# ===================================================
# Step 6: データをリストに格納する
# ===================================================

import openpyxl

wb = openpyxl.load_workbook('社員名簿.xlsx')
ws = wb['社員一覧']

# 全データをリストに格納
employees = []

for row in ws.iter_rows(min_row=2, values_only=True):
    emp = {
        '社員ID': row[0],
        '名前': row[1],
        '部署': row[2],
        '年齢': row[3],
        '入社年': row[4]
    }
    employees.append(emp)

# 確認
print(f"=== {len(employees)}件のデータを読み込みました ===")
print()

# 最初の3件を表示
print("【最初の3件】")
for emp in employees[:3]:
    print(emp)
print()

# 条件で抽出：営業部のメンバー
print("【営業部のメンバー】")
sales_members = [emp for emp in employees if emp['部署'] == '営業部']
for emp in sales_members:
    print(f"  {emp['名前']}（{emp['年齢']}歳）")
print()

# 集計：部署ごとの人数
print("【部署ごとの人数】")
dept_count = {}
for emp in employees:
    dept = emp['部署']
    dept_count[dept] = dept_count.get(dept, 0) + 1

for dept, count in dept_count.items():
    print(f"  {dept}: {count}人")
```

**実行結果：**
```
=== 8件のデータを読み込みました ===

【最初の3件】
{'社員ID': 'E001', '名前': '田中太郎', '部署': '営業部', '年齢': 28, '入社年': 2020}
{'社員ID': 'E002', '名前': '佐藤花子', '部署': '開発部', '年齢': 32, '入社年': 2018}
{'社員ID': 'E003', '名前': '鈴木一郎', '部署': '総務部', '年齢': 25, '入社年': 2023}

【営業部のメンバー】
  田中太郎（28歳）
  高橋美咲（30歳）
  山本大輔（29歳）

【部署ごとの人数】
  営業部: 3人
  開発部: 3人
  総務部: 2人
```

> **ポイント**
>
> openpyxlで読み込んだデータをリスト（辞書のリスト）に変換すると、
> その後の処理（抽出、集計、加工）がやりやすくなります。
>
> ただし、大量データの場合は次のセクション（3-2 pandas入門）で学ぶ
> pandasを使った方が圧倒的に効率的です。

---

## Step 7：Colabでファイルをアップロード/ダウンロードする

自分のExcelファイルをColabで処理する方法です。

```python
# ===================================================
# Step 7: ファイルのアップロードとダウンロード
# ===================================================

from google.colab import files

# ----- アップロード -----
print("Excelファイルをアップロードしてください...")
uploaded = files.upload()

# アップロードされたファイル名を取得
filename = list(uploaded.keys())[0]
print(f"✓ アップロード完了: {filename}")

# ファイルを開いて確認
import openpyxl
wb = openpyxl.load_workbook(filename)
print(f"  シート一覧: {wb.sheetnames}")
```

**実行すると：**
1. 「ファイルを選択」ボタンが表示される
2. PCからExcelファイルを選択
3. アップロードが完了するとファイル名が表示される

```python
# ----- ダウンロード -----
# 処理後のファイルをダウンロード
files.download('社員名簿.xlsx')
print("✓ ダウンロードを開始しました")
```

**実行すると：**
ブラウザのダウンロードが開始され、PCに保存されます。

---

## よくあるエラーと対処法

### エラー1: ファイルが見つからない

```
FileNotFoundError: [Errno 2] No such file or directory: 'sample.xlsx'
```

**原因：** 指定したファイルが存在しない

**対処法：**
1. ファイル名のスペルを確認（全角・半角、拡張子）
2. Colabの場合、ファイルをアップロードしたか確認
3. 現在のフォルダにあるファイル一覧を確認：
```python
import os
print(os.listdir('.'))
```

### エラー2: openpyxlがインストールされていない

```
ModuleNotFoundError: No module named 'openpyxl'
```

**対処法：**
```python
!pip install openpyxl
```

### エラー3: シートが見つからない

```
KeyError: 'Sheet1'
```

**原因：** 指定したシート名が存在しない

**対処法：**
```python
# まずシート名を確認
print(wb.sheetnames)
# 表示されたシート名を使う
ws = wb['正しいシート名']
```

### エラー4: 保存を忘れた

**症状：** コードは動いたのに、Excelファイルに変更が反映されていない

**原因：** `wb.save()` を呼び忘れている

**対処法：**
```python
# 変更後は必ず保存
wb.save('ファイル名.xlsx')
```

---

## このセクションのまとめ

### 学んだこと

- [ ] `!pip install openpyxl`: ライブラリのインストール
- [ ] `openpyxl.Workbook()`: 新規ワークブック作成
- [ ] `openpyxl.load_workbook()`: 既存ファイルを開く
- [ ] `wb.sheetnames`: シート一覧を取得
- [ ] `ws['A1'].value`: セルの値を取得
- [ ] `ws.cell(row=1, column=1)`: 行列番号でセルを取得
- [ ] `ws.iter_rows()`: 行をループで処理
- [ ] `wb.save()`: ファイルを保存（**忘れずに！**）

### GASとの違いのポイント

| 項目 | GAS | openpyxl |
|------|-----|----------|
| インストール | 不要 | `pip install` が必要 |
| ファイルを開く | `openById()` | `load_workbook()` |
| セルの値取得 | `.getRange().getValue()` | `['A1'].value` |
| 保存 | 自動 | `save()` が必要 |
| 実行環境 | Googleサーバー | Colab or ローカル |

---

## 次のステップ

openpyxlの基本操作を学びました。

openpyxlは1セルずつ操作するのに向いていますが、大量データの処理には向いていません。
次のセクション（3-2 pandas入門）では、大量データを高速に処理するpandasを学びます。

**openpyxlとpandasの使い分け：**
- セルの書式設定、結合など → openpyxl
- 大量データの読み込み、集計 → pandas
- 実務では両方を組み合わせることが多い
