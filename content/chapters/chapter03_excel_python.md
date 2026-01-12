# 第3章：Excel×Pythonで「目に見える成果」を出す

## このパートで学ぶこと

- openpyxlでExcelファイルを読み書きする
- pandasで大量データを一瞬で処理する
- GASでは難しい処理をPythonで実現する
- 実用的なExcel処理ツールを完成させる

---

## 3-1. openpyxl入門：Excelファイルを読み書き

### openpyxlとは

**openpyxl**は、PythonでExcelファイル（.xlsx）を操作するためのライブラリです。

GASでスプレッドシートを操作するのと同じ感覚で、Excelファイルを読み書きできます。

### Colabでのインストール

Google Colabには最初から入っていないので、インストールが必要です。

```python
# Colabでは「!」をつけてpipコマンドを実行
!pip install openpyxl
```

> **GAS経験者へ**
> GASは「インストール」という概念がありませんでしたね。Pythonでは外部ライブラリを使うときに`pip install`が必要です。Colabではセッションごとに実行が必要ですが、一度実行すれば同じセッション内では再実行不要です。

### Excelファイルの階層構造

GASのスプレッドシートと同じく、Excelにも階層構造があります。

```
Workbook（ファイル全体）= GASのSpreadsheet
    ↓
Worksheet（シート）= GASのSheet
    ↓
Cell（セル）= GASのRange
    ↓
値
```

### GASとの比較

| 操作 | GAS | Python (openpyxl) |
|------|-----|-------------------|
| ファイルを開く | `SpreadsheetApp.openById()` | `openpyxl.load_workbook()` |
| シートを取得 | `ss.getSheetByName()` | `wb['シート名']` |
| セルの値を取得 | `sheet.getRange().getValue()` | `ws['A1'].value` |
| セルに値を設定 | `sheet.getRange().setValue()` | `ws['A1'] = 値` |
| 保存 | 自動保存 | `wb.save()` が必要 |

### Colabへのファイルアップロード

Colabでローカルのファイルを使うには、アップロードが必要です。

```python
from google.colab import files

# ファイルアップロードのダイアログを表示
uploaded = files.upload()

# アップロードされたファイル名を確認
for filename in uploaded.keys():
    print(f"アップロードされたファイル: {filename}")
```

### 基本操作：ファイルを開いて読む

```python
import openpyxl

# Excelファイルを開く
wb = openpyxl.load_workbook('売上データ.xlsx')

# シート名の一覧を確認
print(wb.sheetnames)  # ['Sheet1', 'Sheet2', ...]

# シートを取得
ws = wb['Sheet1']
# または: ws = wb.active  # アクティブなシートを取得

# セルの値を取得
value = ws['A1'].value
print(value)

# 行番号・列番号で指定（1から始まる）
value2 = ws.cell(row=1, column=1).value
print(value2)
```

### 基本操作：値を書き込んで保存

```python
import openpyxl

# 新規ワークブックを作成
wb = openpyxl.Workbook()
ws = wb.active

# セルに値を設定
ws['A1'] = '名前'
ws['B1'] = '年齢'
ws['A2'] = '田中太郎'
ws['B2'] = 25

# 行番号・列番号で指定
ws.cell(row=3, column=1, value='佐藤花子')
ws.cell(row=3, column=2, value=30)

# ファイルを保存（これを忘れると保存されない！）
wb.save('新規ファイル.xlsx')

print("保存完了！")
```

> **重要：GASとの違い**
> GASはスプレッドシートへの変更が自動保存されますが、openpyxlでは**`wb.save()`を呼ばないと保存されません**。これを忘れると変更が消えてしまうので注意！

### 複数セルの読み書き

```python
import openpyxl

wb = openpyxl.load_workbook('売上データ.xlsx')
ws = wb['Sheet1']

# 範囲を指定して読み込み
for row in ws['A1:C5']:
    for cell in row:
        print(cell.value, end='\t')
    print()  # 改行

# 行をイテレート（全データを読む）
for row in ws.iter_rows(min_row=2, max_col=3, values_only=True):
    print(row)  # タプルで取得: ('田中', 25, '営業部')
```

### データ範囲の動的取得

```python
import openpyxl

wb = openpyxl.load_workbook('売上データ.xlsx')
ws = wb['Sheet1']

# 最終行・最終列を取得
last_row = ws.max_row
last_col = ws.max_column

print(f"データは {last_row} 行 {last_col} 列あります")

# 全データを取得
all_data = []
for row in ws.iter_rows(min_row=1, max_row=last_row,
                         max_col=last_col, values_only=True):
    all_data.append(list(row))

print(all_data)
```

### Colabからファイルをダウンロード

処理結果をローカルに保存するには：

```python
from google.colab import files

# ファイルを保存
wb.save('処理結果.xlsx')

# ダウンロード
files.download('処理結果.xlsx')
```

---

## 3-2. pandas入門：大量データを一瞬で処理

### pandasとは

**pandas**は、Pythonでデータ分析を行うための最強ライブラリです。

Excelの表形式データを、非常に高速かつ簡潔に処理できます。GASにはない、Pythonならではの武器です。

```python
# Colabにはpandasが最初から入っている
import pandas as pd
```

### なぜpandasを使うのか

| 観点 | openpyxlのみ | pandas |
|------|-------------|--------|
| 10万行の処理 | 数分かかる | 数秒 |
| 集計処理 | 自分でループを書く | 1行で完了 |
| コード量 | 多い | 少ない |
| メモリ効率 | 低い | 高い |

### DataFrameの基本

pandasの中心は**DataFrame**（データフレーム）です。Excelの表をそのままPythonで扱えるイメージです。

```python
import pandas as pd

# Excelファイルを読み込み → DataFrame
df = pd.read_excel('売上データ.xlsx')

# 最初の5行を表示
print(df.head())

# データの形状（行数, 列数）
print(df.shape)  # (100, 4) → 100行4列

# 列名の一覧
print(df.columns)
```

### DataFrameの構造

```
         日付      部署    商品名    金額
    0   2025/1/1  営業部   商品A   10000
    1   2025/1/2  開発部   商品B   20000
    2   2025/1/3  営業部   商品C   15000
    ↑
インデックス（行番号）        ↑ 列名（カラム）
```

### 列へのアクセス

```python
import pandas as pd

df = pd.read_excel('売上データ.xlsx')

# 1つの列を取得（Seriesになる）
departments = df['部署']
print(departments)

# 複数の列を取得（DataFrameになる）
subset = df[['日付', '金額']]
print(subset)
```

### 行のフィルタリング

GASでは`if`文でループして抽出していた処理が、1行で書けます。

```python
import pandas as pd

df = pd.read_excel('売上データ.xlsx')

# 条件でフィルタリング
sales_dept = df[df['部署'] == '営業部']
print(sales_dept)

# 金額が10000以上
high_sales = df[df['金額'] >= 10000]
print(high_sales)

# 複数条件（AND: &, OR: |）
filtered = df[(df['部署'] == '営業部') & (df['金額'] >= 10000)]
print(filtered)
```

### 集計処理

GASで何十行も書いていた集計が、1行で完了します。

```python
import pandas as pd

df = pd.read_excel('売上データ.xlsx')

# 合計
total = df['金額'].sum()
print(f"売上合計: {total}")

# 平均
average = df['金額'].mean()
print(f"平均: {average}")

# グループ別集計（これが最強！）
by_dept = df.groupby('部署')['金額'].sum()
print(by_dept)
# 部署
# 営業部    150000
# 開発部     80000
# 総務部     50000

# 複数の集計を同時に
summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
print(summary)
```

### GAS vs pandas：売上集計の比較

**GASの場合（20行以上）：**
```javascript
function aggregateSalesByDepartment() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("売上データ");
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(2, 1, lastRow - 1, 4).getValues();

  const salesByDept = {};
  data.forEach(row => {
    const department = row[1];
    const amount = row[3];
    if (salesByDept[department]) {
      salesByDept[department] += amount;
    } else {
      salesByDept[department] = amount;
    }
  });

  // 出力処理...
}
```

**pandasの場合（3行）：**
```python
import pandas as pd

df = pd.read_excel('売上データ.xlsx')
result = df.groupby('部署')['金額'].sum()
print(result)
```

### CSVの読み書き

```python
import pandas as pd

# CSVを読み込み
df = pd.read_csv('data.csv')

# Excelに保存
df.to_excel('output.xlsx', index=False)

# CSVに保存
df.to_csv('output.csv', index=False)
```

### 複数シートの読み込み

```python
import pandas as pd

# 特定のシートを読み込み
df = pd.read_excel('data.xlsx', sheet_name='Sheet2')

# 全シートを読み込み（辞書で取得）
all_sheets = pd.read_excel('data.xlsx', sheet_name=None)
for sheet_name, df in all_sheets.items():
    print(f"--- {sheet_name} ---")
    print(df.head())
```

---

## 3-3. GASの「6分制限」を超える処理

### GASの実行時間制限

GASには**6分の実行時間制限**があります。大量データを処理しようとすると、途中でタイムアウトしてしまいます。

```
GASの制限:
├── 実行時間: 最大6分（一般アカウント）
├── トリガー実行: 最大30分
└── 1日の実行時間: 合計90分
```

### Pythonには制限がない

ColabやローカルのPythonには、このような時間制限がありません。

| 処理内容 | GAS | Python |
|----------|-----|--------|
| 10万行のデータ処理 | タイムアウトの恐れ | 数秒で完了 |
| 複雑な計算処理 | 制限内で工夫が必要 | そのまま実行 |
| 大量ファイル処理 | 分割実行が必要 | 一括処理可能 |

### 実例：10万行の売上データ集計

```python
import pandas as pd
import time

# 処理時間を計測
start = time.time()

# 10万行のデータを読み込み
df = pd.read_excel('大量売上データ.xlsx')
print(f"データ件数: {len(df)}行")

# 部署別・月別の売上集計
df['月'] = pd.to_datetime(df['日付']).dt.month
result = df.groupby(['部署', '月'])['金額'].agg(['sum', 'mean', 'count'])

# 処理時間を表示
elapsed = time.time() - start
print(f"処理時間: {elapsed:.2f}秒")

print(result)
```

### Colabの注意点

ColabはGASと同じくクラウド環境ですが、異なる制限があります。

```
Colabの制限:
├── セッション: 最大12時間（無料版）
├── 連続実行: 90分でタイムアウト（無操作時）
└── GPU/TPU: 使用制限あり
```

> **ポイント**
> Colabは「開いている間は動く」環境です。ブラウザを閉じるとセッションが切れる可能性があります。長時間処理は第4章で学ぶローカル環境で行うのがベストです。

---

## 3-4. 【実践】売上集計システム

GAS講座で作った「売上集計システム」を、Pythonで作り直してみましょう。同じ機能がどれだけシンプルに書けるか体感してください。

### データ構造

**売上データ.xlsx:**
| 日付 | 部署 | 商品名 | 金額 |
|------|------|--------|------|
| 2025/1/1 | 営業部 | 商品A | 10000 |
| 2025/1/2 | 開発部 | 商品B | 20000 |
| 2025/1/3 | 営業部 | 商品C | 15000 |
| ... | ... | ... | ... |

### 完成コード

```python
import pandas as pd
from google.colab import files

# ===== 1. ファイルアップロード =====
print("売上データのExcelファイルをアップロードしてください")
uploaded = files.upload()
filename = list(uploaded.keys())[0]

# ===== 2. データ読み込み =====
df = pd.read_excel(filename)
print(f"\n読み込み完了: {len(df)}件のデータ")
print(df.head())

# ===== 3. 部署別売上集計 =====
print("\n===== 部署別売上集計 =====")
dept_sales = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
dept_sales.columns = ['売上合計', '平均単価', '件数']
dept_sales = dept_sales.sort_values('売上合計', ascending=False)
print(dept_sales)

# ===== 4. 月別売上集計 =====
print("\n===== 月別売上集計 =====")
df['月'] = pd.to_datetime(df['日付']).dt.month
monthly_sales = df.groupby('月')['金額'].sum()
print(monthly_sales)

# ===== 5. 結果をExcelに出力 =====
with pd.ExcelWriter('集計結果.xlsx') as writer:
    dept_sales.to_excel(writer, sheet_name='部署別集計')
    monthly_sales.to_excel(writer, sheet_name='月別集計')

print("\n集計結果.xlsx に保存しました")

# ===== 6. ダウンロード =====
files.download('集計結果.xlsx')
```

### コード解説

| 部分 | 説明 |
|------|------|
| `files.upload()` | Colabにファイルをアップロード |
| `pd.read_excel()` | Excelファイルを読み込み |
| `groupby().agg()` | グループ化して複数の集計を実行 |
| `sort_values()` | 並び替え |
| `pd.ExcelWriter()` | 複数シートへの書き込み |
| `files.download()` | 結果をダウンロード |

### GASとの比較

| 項目 | GAS | Python |
|------|-----|--------|
| コード行数 | 約40行 | 約25行 |
| 処理速度 | 数秒〜数分 | 1秒未満 |
| 複数シート出力 | 手動でシート作成 | `ExcelWriter`で簡単 |

---

## 3-5. 【実践】複数ファイル一括処理

複数のExcelファイルを一括で処理する、実務で頻出のパターンです。

### シナリオ

月次の売上ファイルが複数あり、それを1つのファイルに統合したい。

```
sales_2025_01.xlsx
sales_2025_02.xlsx
sales_2025_03.xlsx
    ↓ 統合
全期間売上.xlsx
```

### Colabでの複数ファイルアップロード

```python
from google.colab import files
import pandas as pd
import os

# 複数ファイルをアップロード
print("複数のExcelファイルをアップロードしてください")
uploaded = files.upload()

# アップロードされたファイル一覧
excel_files = [f for f in uploaded.keys() if f.endswith('.xlsx')]
print(f"\n{len(excel_files)}個のExcelファイルがアップロードされました")
for f in excel_files:
    print(f"  - {f}")
```

### 統合処理

```python
import pandas as pd
from google.colab import files

# ===== 1. ファイルアップロード =====
print("統合したいExcelファイルを複数選択してアップロードしてください")
uploaded = files.upload()
excel_files = [f for f in uploaded.keys() if f.endswith('.xlsx')]

# ===== 2. 全ファイルを読み込んで統合 =====
all_data = []

for filename in excel_files:
    df = pd.read_excel(filename)
    df['元ファイル'] = filename  # どのファイルから来たか記録
    all_data.append(df)
    print(f"  {filename}: {len(df)}行")

# 縦に結合
combined = pd.concat(all_data, ignore_index=True)
print(f"\n統合完了: 合計 {len(combined)}行")

# ===== 3. 統合データを確認 =====
print("\n--- 統合データのプレビュー ---")
print(combined.head(10))

# ===== 4. 保存してダウンロード =====
combined.to_excel('統合データ.xlsx', index=False)
files.download('統合データ.xlsx')
```

### フォルダ内の全ファイルを処理（ローカル環境向け）

第4章でローカル環境を構築した後は、フォルダ指定で一括処理できます。

```python
import pandas as pd
import glob

# フォルダ内の全Excelファイルを取得
excel_files = glob.glob('売上データ/*.xlsx')

all_data = []
for filepath in excel_files:
    df = pd.read_excel(filepath)
    all_data.append(df)

combined = pd.concat(all_data, ignore_index=True)
combined.to_excel('統合結果.xlsx', index=False)
```

---

## 3-6. 【AIプロンプト】Excel操作コードの生成

AIを活用して、Excel処理のコードを効率的に生成するテンプレートです。

### 基本テンプレート

```
【依頼】
PythonでExcelファイルを処理したいです。

【入力ファイル】
- ファイル名: [ファイル名.xlsx]
- シート構成: [シート名の一覧]
- 列構成: [列名のリスト]

【やりたいこと】
[具体的な処理内容]

【出力】
[期待する出力形式]

【環境】
Google Colab（pandasとopenpyxlが使えます）
```

### 実践例1：条件抽出

```
【依頼】
PythonでExcelファイルを処理したいです。

【入力ファイル】
- ファイル名: 売上データ.xlsx
- 列構成: 日付, 部署, 商品名, 金額

【やりたいこと】
金額が50000円以上のデータだけを抽出したい

【出力】
抽出結果を新しいExcelファイルに保存

【環境】
Google Colab（pandasが使えます）
```

### 実践例2：集計レポート

```
【依頼】
売上データから月次レポートを自動生成したいです。

【入力ファイル】
- ファイル名: 売上データ.xlsx
- 列構成: 日付, 部署, 商品名, 金額

【やりたいこと】
1. 部署別の売上合計
2. 月別の売上推移
3. 商品別の売上ランキング（上位10件）

【出力】
上記3つを別シートとして1つのExcelファイルに保存

【環境】
Google Colab
```

### 実践例3：複数ファイル統合

```
【依頼】
複数の月次売上ファイルを1つに統合したいです。

【入力ファイル】
- sales_2025_01.xlsx
- sales_2025_02.xlsx
- sales_2025_03.xlsx
（すべて同じ列構成: 日付, 部署, 商品名, 金額）

【やりたいこと】
1. 全ファイルを縦に結合
2. どのファイルから来たデータか分かる列を追加
3. 日付順にソート

【出力】
統合データ.xlsx として保存

【環境】
Google Colab
```

### AIへの質問テンプレート

**コードの意味を理解したいとき:**
```
以下のPythonコードを1行ずつ説明してください。
特に [わからない部分] が理解できません。

[コードを貼り付け]
```

**エラーが出たとき:**
```
以下のPythonコードを実行したらエラーが出ました。
原因と解決策を教えてください。

【コード】
[コードを貼り付け]

【エラーメッセージ】
[エラーメッセージを貼り付け]

【やりたかったこと】
[何をしようとしていたか]
```

---

## このパートのまとめ

このパートで学んだことを確認しましょう。

- [ ] openpyxlでExcelファイルを読み書きできる
- [ ] pandasでDataFrameを使ったデータ処理ができる
- [ ] groupbyで集計処理ができる
- [ ] 複数ファイルを統合できる
- [ ] ColabでExcelファイルのアップロード/ダウンロードができる
- [ ] AIにExcel処理のコード生成を依頼できる

### 作成したツール

1. **売上集計システム** - 部署別・月別の売上を自動集計
2. **複数ファイル統合ツール** - 複数のExcelファイルを1つに統合

### GASとの違いのポイント

| 項目 | GAS | Python |
|------|-----|--------|
| 環境 | ブラウザ（スプレッドシート） | Colab / ローカル |
| 対象ファイル | Googleスプレッドシート | Excel (.xlsx) |
| 処理速度 | 遅い（API呼び出し） | 速い（メモリ上で処理） |
| 時間制限 | 6分 | なし |
| 集計処理 | ループで自作 | pandasで1行 |
| 保存 | 自動 | `save()`が必要 |

---

## 練習問題

### 問題1：基本操作

Excelファイル「社員名簿.xlsx」を読み込み、以下を実行してください。
- 全データの行数と列数を表示
- 「部署」列のユニークな値を表示
- 「年齢」列の平均値を計算

### 問題2：フィルタリング

売上データから以下の条件でデータを抽出してください。
- 営業部のデータのみ
- 金額が30000円以上
- 上記2つの条件を両方満たすデータ

### 問題3：集計レポート

売上データを読み込み、以下のレポートを作成してください。
- 部署別の売上合計と件数
- 結果をExcelファイルに保存

<details>
<summary>解答例</summary>

```python
# 問題1
import pandas as pd

df = pd.read_excel('社員名簿.xlsx')
print(f"行数: {len(df)}, 列数: {len(df.columns)}")
print(f"部署一覧: {df['部署'].unique()}")
print(f"平均年齢: {df['年齢'].mean():.1f}歳")

# 問題2
df = pd.read_excel('売上データ.xlsx')
sales_dept = df[df['部署'] == '営業部']
high_sales = df[df['金額'] >= 30000]
both = df[(df['部署'] == '営業部') & (df['金額'] >= 30000)]

# 問題3
df = pd.read_excel('売上データ.xlsx')
report = df.groupby('部署')['金額'].agg(['sum', 'count'])
report.columns = ['売上合計', '件数']
report.to_excel('部署別レポート.xlsx')
```

</details>

---

## 次のパートへ

おめでとうございます！Pythonで「目に見える成果」を出せるようになりました。

GASでは難しかった大量データ処理や複雑な集計が、pandasを使えば驚くほど簡単に実現できることを体感できたと思います。

次のパートでは、いよいよ**ローカル環境**への移行を学びます。

- Colabを卒業して、自分のPCでPythonを動かす
- **venv**で環境を「壊さない」作法を身につける
- **exe化**してツールを配布可能にする

「壊さない」Python作法を身につけて、プロのPythonistaへの第一歩を踏み出しましょう！
