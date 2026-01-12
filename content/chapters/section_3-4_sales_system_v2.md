# 3-4. 【実践】売上集計システム

GAS講座で作った「売上集計システム」を、Pythonで作り直します。
**このセクションのコードはすべてColabでコピペして動きます。**

---

## このセクションのゴール

- Excelファイルから売上データを読み込む
- 部署別・月別の売上を集計する
- 結果を新しいExcelファイルに出力する

所要時間：約30分

---

## Step 0：サンプルデータを作る

まず、練習用の売上データを作ります。以下のコードをColabで実行してください。

```python
# ===================================================
# Step 0: サンプルデータの作成
# Colabで実行すると「売上データ.xlsx」が作られます
# ===================================================

import pandas as pd
import random
from datetime import datetime, timedelta

# 再現性のために乱数シードを固定
random.seed(42)

# データを生成
data = []
departments = ['営業部', '開発部', '総務部', 'マーケティング部']
products = ['商品A', '商品B', '商品C', '商品D', '商品E']

# 2025年1月1日から100件のデータを生成
start_date = datetime(2025, 1, 1)

for i in range(100):
    date = start_date + timedelta(days=random.randint(0, 89))  # 1-3月のランダムな日付
    department = random.choice(departments)
    product = random.choice(products)
    amount = random.randint(1, 10) * 10000  # 1万〜10万円

    data.append({
        '日付': date.strftime('%Y/%m/%d'),
        '部署': department,
        '商品名': product,
        '金額': amount
    })

# DataFrameを作成
df = pd.DataFrame(data)

# 日付順にソート
df = df.sort_values('日付').reset_index(drop=True)

# Excelファイルとして保存
df.to_excel('売上データ.xlsx', index=False)

# 確認：最初の10行を表示
print("=== 売上データ.xlsx を作成しました ===")
print(f"データ件数: {len(df)}件")
print()
print("【データのプレビュー（最初の10行）】")
print(df.head(10).to_string(index=False))
```

**実行結果：**
```
=== 売上データ.xlsx を作成しました ===
データ件数: 100件

【データのプレビュー（最初の10行）】
       日付           部署 商品名    金額
2025/01/01       開発部  商品C  50000
2025/01/02       営業部  商品A  30000
2025/01/02 マーケティング部  商品E  80000
2025/01/03       総務部  商品B  20000
2025/01/04       営業部  商品D  60000
2025/01/05       開発部  商品A  40000
2025/01/06       営業部  商品C  90000
2025/01/07       総務部  商品E  10000
2025/01/08 マーケティング部  商品B  70000
2025/01/09       開発部  商品D  30000
```

> **ここで何をしているか：**
> - `random.seed(42)`: 乱数を固定して、誰が実行しても同じデータが生成されるようにする
> - `timedelta(days=...)`: 日付を1日ずつずらすためのPythonの機能
> - `df.to_excel()`: DataFrameをExcelファイルとして保存

---

## Step 1：データを読み込む

作成したExcelファイルを読み込みます。

```python
# ===================================================
# Step 1: Excelファイルを読み込む
# ===================================================

import pandas as pd

# Excelファイルを読み込む
df = pd.read_excel('売上データ.xlsx')

# 読み込んだデータの情報を確認
print("=== データ読み込み完了 ===")
print(f"行数: {len(df)}行")
print(f"列数: {len(df.columns)}列")
print(f"列名: {list(df.columns)}")
print()

# データ型を確認
print("【各列のデータ型】")
print(df.dtypes)
print()

# 最初の5行を表示
print("【最初の5行】")
print(df.head())
```

**実行結果：**
```
=== データ読み込み完了 ===
行数: 100行
列数: 4列
列名: ['日付', '部署', '商品名', '金額']

【各列のデータ型】
日付      object
部署      object
商品名    object
金額       int64
dtype: object

【最初の5行】
         日付           部署 商品名    金額
0  2025/01/01       開発部  商品C  50000
1  2025/01/02       営業部  商品A  30000
2  2025/01/02 マーケティング部  商品E  80000
3  2025/01/03       総務部  商品B  20000
4  2025/01/04       営業部  商品D  60000
```

### コード解説（1行ずつ）

```python
import pandas as pd
```
pandasライブラリを読み込みます。`pd`という短い名前で使えるようにしています。
これはPythonの慣習で、ほぼすべてのコードで`pd`が使われます。

```python
df = pd.read_excel('売上データ.xlsx')
```
- `pd.read_excel()`: Excelファイルを読み込む関数
- `'売上データ.xlsx'`: 読み込むファイル名（同じフォルダにある前提）
- `df`: 読み込んだデータを入れる変数。`df`はDataFrameの略で、これも慣習

```python
print(f"行数: {len(df)}行")
```
- `len(df)`: DataFrameの行数を取得
- `f"..."`: f文字列。`{}`の中に変数を埋め込める（GASのテンプレートリテラルと同じ）

```python
print(df.dtypes)
```
- `df.dtypes`: 各列のデータ型を表示
- `object`: 文字列（Pythonでは文字列を`object`と表示する）
- `int64`: 64ビット整数

### よくあるエラーと対処法

**エラー1: ファイルが見つからない**
```
FileNotFoundError: [Errno 2] No such file or directory: '売上データ.xlsx'
```

**原因**: ファイル名が間違っている、またはStep 0を実行していない

**対処法**:
1. Step 0を先に実行してファイルを作成する
2. ファイル名のスペルを確認する（全角・半角に注意）

**エラー2: openpyxlがない**
```
ImportError: Missing optional dependency 'openpyxl'.
```

**対処法**: 以下を実行してからやり直す
```python
!pip install openpyxl
```

---

## Step 2：部署別の売上を集計する

ここがPythonの真骨頂です。GASでは20行以上かかる処理が、たった1行で書けます。

```python
# ===================================================
# Step 2: 部署別売上を集計する
# ===================================================

# 部署別の売上合計を計算（たった1行！）
sales_by_dept = df.groupby('部署')['金額'].sum()

print("=== 部署別売上合計 ===")
print(sales_by_dept)
print()
print(f"全社合計: {sales_by_dept.sum():,}円")
```

**実行結果：**
```
=== 部署別売上合計 ===
部署
マーケティング部    1230000
営業部            1450000
総務部             980000
開発部            1340000
Name: 金額, dtype: int64

全社合計: 5,000,000円
```

### この1行を分解して理解する

```python
sales_by_dept = df.groupby('部署')['金額'].sum()
```

この1行は、実は3つの処理を連結しています：

```python
# 分解するとこうなる：

# 1. 部署でグループ化
grouped = df.groupby('部署')
print(type(grouped))  # <class 'pandas.core.groupby.generic.DataFrameGroupBy'>

# 2. 金額列だけを取り出す
amount_grouped = grouped['金額']
print(type(amount_grouped))  # <class 'pandas.core.groupby.generic.SeriesGroupBy'>

# 3. 各グループの合計を計算
result = amount_grouped.sum()
print(type(result))  # <class 'pandas.core.series.Series'>
```

**図解：**
```
元データ（df）
┌────────┬────────┬────────┐
│  部署  │ 商品名 │  金額  │
├────────┼────────┼────────┤
│ 営業部 │ 商品A  │ 30000  │
│ 開発部 │ 商品C  │ 50000  │
│ 営業部 │ 商品D  │ 60000  │
│ 総務部 │ 商品B  │ 20000  │
│ 開発部 │ 商品A  │ 40000  │
└────────┴────────┴────────┘
          ↓
    groupby('部署')
          ↓
┌─────────────────────────┐
│ 営業部: [30000, 60000]   │
│ 開発部: [50000, 40000]   │
│ 総務部: [20000]          │
└─────────────────────────┘
          ↓
       .sum()
          ↓
┌─────────────────────────┐
│ 営業部:  90000           │
│ 開発部:  90000           │
│ 総務部:  20000           │
└─────────────────────────┘
```

### GASで同じ処理を書くと…

```javascript
// GASの場合（20行以上必要）
function aggregateSalesByDepartment() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("売上データ");

  // データを取得
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(2, 1, lastRow - 1, 4).getValues();

  // 部署別に集計するオブジェクト
  const salesByDept = {};

  // ループして集計
  data.forEach(row => {
    const department = row[1];  // B列: 部署
    const amount = row[3];      // D列: 金額

    if (salesByDept[department]) {
      salesByDept[department] += amount;
    } else {
      salesByDept[department] = amount;
    }
  });

  // 結果を表示
  for (const dept in salesByDept) {
    console.log(`${dept}: ${salesByDept[dept]}円`);
  }
}
```

**比較：**
| 項目 | GAS | Python (pandas) |
|------|-----|-----------------|
| コード行数 | 約20行 | 1行 |
| 処理内容 | ループで1行ずつ処理 | 内部で最適化された処理 |
| 速度（1万行） | 数秒 | 0.01秒以下 |
| 速度（10万行） | タイムアウトの恐れ | 0.1秒程度 |

---

## Step 3：より詳細な集計

複数の集計を同時に行います。

```python
# ===================================================
# Step 3: 複数の集計を同時に行う
# ===================================================

# 部署別の売上合計・平均・件数を一度に計算
dept_summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])

# 列名を日本語に変更
dept_summary.columns = ['売上合計', '平均単価', '件数']

# 売上合計の降順でソート
dept_summary = dept_summary.sort_values('売上合計', ascending=False)

# 金額をカンマ区切りで見やすく表示
print("=== 部署別売上サマリー ===")
print(dept_summary.to_string())
```

**実行結果：**
```
=== 部署別売上サマリー ===
                売上合計     平均単価  件数
部署
営業部          1450000  53703.70   27
開発部          1340000  51538.46   26
マーケティング部  1230000  51250.00   24
総務部           980000  42608.70   23
```

### コード解説

```python
.agg(['sum', 'mean', 'count'])
```
- `agg`: aggregate（集計）の略
- 複数の集計関数をリストで渡すと、全部まとめて計算してくれる
- `sum`: 合計、`mean`: 平均、`count`: 件数

```python
dept_summary.columns = ['売上合計', '平均単価', '件数']
```
- `.columns`: DataFrameの列名を取得/設定
- リストで新しい列名を渡すと、順番に置き換わる

```python
.sort_values('売上合計', ascending=False)
```
- `sort_values()`: 指定した列で並び替え
- `ascending=False`: 降順（大きい順）。`True`なら昇順（小さい順）

---

## Step 4：月別集計を追加

日付から月を抽出して、月別の集計も行います。

```python
# ===================================================
# Step 4: 月別売上を集計する
# ===================================================

# 日付列を日付型に変換
df['日付'] = pd.to_datetime(df['日付'])

# 日付から「月」を抽出して新しい列を作成
df['月'] = df['日付'].dt.month

# 確認：月の列が追加されたか
print("【月の列を追加した結果】")
print(df.head())
print()

# 月別の売上合計
monthly_sales = df.groupby('月')['金額'].sum()

print("=== 月別売上合計 ===")
for month, amount in monthly_sales.items():
    print(f"{month}月: {amount:,}円")

print(f"\n合計: {monthly_sales.sum():,}円")
```

**実行結果：**
```
【月の列を追加した結果】
        日付           部署 商品名    金額  月
0 2025-01-01       開発部  商品C  50000   1
1 2025-01-02       営業部  商品A  30000   1
2 2025-01-02 マーケティング部  商品E  80000   1
3 2025-01-03       総務部  商品B  20000   1
4 2025-01-04       営業部  商品D  60000   1

=== 月別売上合計 ===
1月: 1,850,000円
2月: 1,620,000円
3月: 1,530,000円

合計: 5,000,000円
```

### コード解説

```python
df['日付'] = pd.to_datetime(df['日付'])
```
- `pd.to_datetime()`: 文字列を日付型に変換
- 元の「2025/01/01」という文字列が、日付として扱えるようになる
- 日付型にすると、年・月・日を個別に取り出せる

```python
df['月'] = df['日付'].dt.month
```
- `.dt`: 日付型の列に対して日付操作をするためのアクセサ
- `.dt.month`: 日付から月だけを取り出す（1〜12の数値）
- 他にも `.dt.year`（年）、`.dt.day`（日）、`.dt.weekday`（曜日）などがある

### よくあるエラーと対処法

**エラー: dt アクセサが使えない**
```
AttributeError: Can only use .dt accessor with datetimelike values
```

**原因**: 日付列がまだ文字列のまま

**対処法**: 先に`pd.to_datetime()`で変換する
```python
df['日付'] = pd.to_datetime(df['日付'])  # これを先に実行
df['月'] = df['日付'].dt.month  # その後でdt.monthが使える
```

---

## Step 5：結果をExcelに出力する

集計結果を新しいExcelファイルに保存します。複数の集計結果を別々のシートに保存します。

```python
# ===================================================
# Step 5: 結果をExcelファイルに出力する
# ===================================================

# 出力用に集計結果を再作成
dept_summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
dept_summary.columns = ['売上合計', '平均単価', '件数']
dept_summary = dept_summary.sort_values('売上合計', ascending=False)

monthly_sales = df.groupby('月')['金額'].sum()
monthly_sales = monthly_sales.reset_index()  # インデックスを列に戻す
monthly_sales.columns = ['月', '売上合計']

# ExcelWriterを使って複数シートに書き込む
with pd.ExcelWriter('集計結果.xlsx') as writer:
    dept_summary.to_excel(writer, sheet_name='部署別集計')
    monthly_sales.to_excel(writer, sheet_name='月別集計', index=False)

print("=== 集計結果.xlsx に保存しました ===")
print()
print("【ファイルの中身】")
print("シート1: 部署別集計")
print(dept_summary.to_string())
print()
print("シート2: 月別集計")
print(monthly_sales.to_string(index=False))
```

**実行結果：**
```
=== 集計結果.xlsx に保存しました ===

【ファイルの中身】
シート1: 部署別集計
                売上合計     平均単価  件数
部署
営業部          1450000  53703.70   27
開発部          1340000  51538.46   26
マーケティング部  1230000  51250.00   24
総務部           980000  42608.70   23

シート2: 月別集計
 月   売上合計
  1  1850000
  2  1620000
  3  1530000
```

### コード解説

```python
with pd.ExcelWriter('集計結果.xlsx') as writer:
```
- `pd.ExcelWriter()`: Excelファイルに書き込むためのオブジェクトを作成
- `with ... as writer:`: 書き込み後に自動でファイルを閉じる（お作法）

```python
dept_summary.to_excel(writer, sheet_name='部署別集計')
```
- `.to_excel()`: DataFrameをExcelに書き込む
- `writer`: 書き込み先のExcelWriterオブジェクト
- `sheet_name`: シート名を指定

```python
monthly_sales.to_excel(writer, sheet_name='月別集計', index=False)
```
- `index=False`: 行番号（インデックス）を出力しない
- Trueにすると、0, 1, 2...という行番号も書き込まれる

---

## Step 6：ファイルをダウンロードする（Colab用）

Colabで作成したファイルをPCにダウンロードします。

```python
# ===================================================
# Step 6: ファイルをダウンロードする（Colab専用）
# ===================================================

from google.colab import files

# 作成したファイルをダウンロード
files.download('集計結果.xlsx')

print("ダウンロードが開始されました。")
print("ブラウザのダウンロードフォルダを確認してください。")
```

**実行結果：**
ブラウザのダウンロードが開始され、「集計結果.xlsx」がPCに保存されます。

> **注意**: この`files.download()`はGoogle Colab専用の機能です。
> ローカル環境（第4章で学ぶ）では不要です。ファイルはそのままPCに保存されます。

---

## 完成コード（まとめ）

これまでのステップをまとめた完成版です。**このコードをColab**にコピペすれば、最初から最後まで動きます。

```python
# ===================================================
# 売上集計システム - 完成版
# Colabにコピペしてそのまま実行できます
# ===================================================

import pandas as pd
import random
from datetime import datetime, timedelta

# ----- Step 0: サンプルデータ作成 -----
random.seed(42)
data = []
departments = ['営業部', '開発部', '総務部', 'マーケティング部']
products = ['商品A', '商品B', '商品C', '商品D', '商品E']
start_date = datetime(2025, 1, 1)

for i in range(100):
    date = start_date + timedelta(days=random.randint(0, 89))
    data.append({
        '日付': date.strftime('%Y/%m/%d'),
        '部署': random.choice(departments),
        '商品名': random.choice(products),
        '金額': random.randint(1, 10) * 10000
    })

df = pd.DataFrame(data).sort_values('日付').reset_index(drop=True)
df.to_excel('売上データ.xlsx', index=False)
print(f"✓ サンプルデータ作成完了: {len(df)}件")

# ----- Step 1: データ読み込み -----
df = pd.read_excel('売上データ.xlsx')
print(f"✓ データ読み込み完了: {len(df)}件")

# ----- Step 2-3: 部署別集計 -----
dept_summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
dept_summary.columns = ['売上合計', '平均単価', '件数']
dept_summary = dept_summary.sort_values('売上合計', ascending=False)

print("\n=== 部署別売上サマリー ===")
print(dept_summary.to_string())

# ----- Step 4: 月別集計 -----
df['日付'] = pd.to_datetime(df['日付'])
df['月'] = df['日付'].dt.month
monthly_sales = df.groupby('月')['金額'].sum().reset_index()
monthly_sales.columns = ['月', '売上合計']

print("\n=== 月別売上 ===")
for _, row in monthly_sales.iterrows():
    print(f"{int(row['月'])}月: {row['売上合計']:,.0f}円")

# ----- Step 5: Excel出力 -----
with pd.ExcelWriter('集計結果.xlsx') as writer:
    dept_summary.to_excel(writer, sheet_name='部署別集計')
    monthly_sales.to_excel(writer, sheet_name='月別集計', index=False)

print("\n✓ 集計結果.xlsx に保存しました")

# ----- Step 6: ダウンロード（Colab用） -----
from google.colab import files
files.download('集計結果.xlsx')
print("✓ ダウンロード開始")
```

**実行結果：**
```
✓ サンプルデータ作成完了: 100件
✓ データ読み込み完了: 100件

=== 部署別売上サマリー ===
                売上合計     平均単価  件数
部署
営業部          1450000  53703.70   27
開発部          1340000  51538.46   26
マーケティング部  1230000  51250.00   24
総務部           980000  42608.70   23

=== 月別売上 ===
1月: 1,850,000円
2月: 1,620,000円
3月: 1,530,000円

✓ 集計結果.xlsx に保存しました
✓ ダウンロード開始
```

---

## 自分のデータで試す場合

サンプルデータではなく、自分のExcelファイルを使いたい場合：

```python
# ===================================================
# 自分のExcelファイルを使う場合
# ===================================================

import pandas as pd
from google.colab import files

# ----- ファイルをアップロード -----
print("Excelファイルをアップロードしてください")
uploaded = files.upload()

# アップロードされたファイル名を取得
filename = list(uploaded.keys())[0]
print(f"アップロードされたファイル: {filename}")

# ----- データ読み込み -----
df = pd.read_excel(filename)

# 列名を確認
print(f"\n【列名の確認】")
print(list(df.columns))

# ↓↓↓ 以下、自分のデータの列名に合わせて修正 ↓↓↓
# 例: 列名が「部門」「売上金額」の場合
# dept_summary = df.groupby('部門')['売上金額'].sum()
```

> **ポイント**: 自分のデータを使うときは、列名を確認してコードを修正してください。
> 「部署」→「部門」、「金額」→「売上金額」など、データによって列名が異なります。

---

## このセクションのまとめ

### 学んだこと

- [ ] `pd.read_excel()`: Excelファイルを読み込む
- [ ] `df.groupby()`: データをグループ化する
- [ ] `.agg()`: 複数の集計を同時に行う
- [ ] `.sort_values()`: データを並び替える
- [ ] `pd.to_datetime()`: 文字列を日付型に変換
- [ ] `.dt.month`: 日付から月を取り出す
- [ ] `pd.ExcelWriter()`: 複数シートのExcelを作成
- [ ] `files.download()`: Colabからファイルをダウンロード

### GASとの違い

| 項目 | GAS | Python |
|------|-----|--------|
| 集計処理 | ループで自作（20行） | `.groupby().sum()`（1行） |
| 複数集計 | 別々にループを書く | `.agg()`で一度に |
| 日付処理 | 手動でパース | `.dt`アクセサで簡単 |
| 複数シート出力 | シートを作成→書き込み | `ExcelWriter`で一括 |
| 処理速度 | 遅い | 高速 |

---

## 練習問題

### 問題1
商品名別の売上合計を計算してください。

### 問題2
部署×月のクロス集計表を作ってください。
（ヒント: `pd.pivot_table()`を使います）

### 問題3
売上金額が50,000円以上のデータだけを抽出して、新しいExcelファイルに保存してください。

<details>
<summary>解答を見る</summary>

```python
# 問題1: 商品名別の売上合計
product_sales = df.groupby('商品名')['金額'].sum()
print(product_sales.sort_values(ascending=False))

# 問題2: 部署×月のクロス集計
pivot = pd.pivot_table(df, values='金額', index='部署', columns='月', aggfunc='sum')
print(pivot)

# 問題3: 50,000円以上を抽出
high_sales = df[df['金額'] >= 50000]
high_sales.to_excel('高額売上.xlsx', index=False)
print(f"抽出件数: {len(high_sales)}件")
files.download('高額売上.xlsx')
```

</details>
