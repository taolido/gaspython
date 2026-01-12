# 3-2. pandas入門：大量データを一瞬で処理

Pythonでデータ分析を行う最強ライブラリ「pandas」を学びます。
**このセクションのコードはすべてColabでコピペして動きます。**

---

## このセクションのゴール

- pandasのDataFrameを理解する
- Excelファイルを読み込んで操作する
- データの抽出・集計を1行で書く
- GASでは何十行もかかる処理を数行で実現する

所要時間：約30分

---

## pandasとは

**pandas**（パンダス）は、Pythonでデータ分析を行うための最強ライブラリです。

「Excel作業をPythonで自動化したい」なら、pandasは必須スキルです。

### なぜpandasを使うのか

| 比較項目 | openpyxl | pandas |
|---------|----------|--------|
| 10万行の読み込み | 数分かかる | 数秒 |
| 部署別集計 | 自分でループを書く | 1行で完了 |
| 条件でデータ抽出 | if文でループ | 1行で完了 |
| 複数ファイル結合 | 複雑なコード | 3行で完了 |

**結論：Excelデータを扱うなら、pandasを使わない理由がない。**

---

## Step 1：サンプルデータを作る

まず、練習用のデータを作成します。

```python
# ===================================================
# Step 1: サンプルデータを作る
# このコードを実行すると「売上データ.xlsx」が作られます
# ===================================================

import pandas as pd
import random
from datetime import datetime, timedelta

# 再現性のために乱数シードを固定（誰が実行しても同じデータになる）
random.seed(42)

# データを生成
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
        '数量': random.randint(1, 10),
        '単価': random.choice([10000, 20000, 30000, 50000]),
        '金額': 0  # 後で計算
    })

# DataFrameを作成
df = pd.DataFrame(data)

# 金額を計算（数量 × 単価）
df['金額'] = df['数量'] * df['単価']

# 日付順にソート
df = df.sort_values('日付').reset_index(drop=True)

# Excelファイルとして保存
df.to_excel('売上データ.xlsx', index=False)

print("✓ 売上データ.xlsx を作成しました")
print(f"  データ件数: {len(df)}件")
print()
print("【最初の5行】")
print(df.head().to_string(index=False))
```

**実行結果：**
```
✓ 売上データ.xlsx を作成しました
  データ件数: 100件

【最初の5行】
       日付           部署 商品名  数量   単価     金額
2025/01/01       開発部  商品C    8  30000  240000
2025/01/02       営業部  商品A    3  10000   30000
2025/01/02 マーケティング部  商品E    5  50000  250000
2025/01/03       総務部  商品B    2  20000   40000
2025/01/04       営業部  商品D    7  30000  210000
```

---

## Step 2：Excelファイルを読み込む

pandasでExcelファイルを読み込みます。

```python
# ===================================================
# Step 2: Excelファイルを読み込む
# ===================================================

import pandas as pd

# Excelファイルを読み込む
df = pd.read_excel('売上データ.xlsx')

# 基本情報を確認
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
print()

# 最後の3行を表示
print("【最後の3行】")
print(df.tail(3))
```

**実行結果：**
```
=== データ読み込み完了 ===
行数: 100行
列数: 6列
列名: ['日付', '部署', '商品名', '数量', '単価', '金額']

【各列のデータ型】
日付      object
部署      object
商品名    object
数量       int64
単価       int64
金額       int64
dtype: object

【最初の5行】
         日付           部署 商品名  数量   単価     金額
0  2025/01/01       開発部  商品C    8  30000  240000
1  2025/01/02       営業部  商品A    3  10000   30000
2  2025/01/02 マーケティング部  商品E    5  50000  250000
3  2025/01/03       総務部  商品B    2  20000   40000
4  2025/01/04       営業部  商品D    7  30000  210000

【最後の3行】
          日付           部署 商品名  数量   単価     金額
97  2025/03/28       開発部  商品B    6  20000  120000
98  2025/03/29       営業部  商品C    4  30000  120000
99  2025/03/30       総務部  商品A    9  10000   90000
```

### コード解説

```python
import pandas as pd
```
pandasライブラリを読み込みます。慣習的に `pd` という名前で使います。
Colabには最初から入っているので、`pip install` は不要です。

```python
df = pd.read_excel('売上データ.xlsx')
```
- `pd.read_excel()`: Excelファイルを読み込んでDataFrameに変換
- `df`: DataFrame（データフレーム）を入れる変数。慣習的に`df`を使う

```python
df.head()
```
最初の5行を表示。`df.head(10)`で10行表示。

```python
df.tail(3)
```
最後の3行を表示。

---

## Step 3：DataFrameの構造を理解する

DataFrameはExcelの表そのものです。

```
DataFrame（df）の構造：

         日付      部署   商品名   数量    単価      金額
    ┌─────────────────────────────────────────────────┐
  0 │ 2025/01/01  開発部   商品C     8   30000   240000 │
  1 │ 2025/01/02  営業部   商品A     3   10000    30000 │
  2 │ 2025/01/02  マーケ   商品E     5   50000   250000 │
  3 │ 2025/01/03  総務部   商品B     2   20000    40000 │
    └─────────────────────────────────────────────────┘
  ↑                              ↑
インデックス（行番号）          カラム（列名）
```

### 列へのアクセス

```python
# ===================================================
# 列（カラム）へのアクセス
# ===================================================

import pandas as pd
df = pd.read_excel('売上データ.xlsx')

# ----- 1つの列を取得 -----
print("=== 1つの列を取得 ===")
departments = df['部署']
print(type(departments))  # <class 'pandas.core.series.Series'>
print(departments.head())
print()

# ----- 複数の列を取得 -----
print("=== 複数の列を取得 ===")
subset = df[['日付', '部署', '金額']]  # リストで列名を指定
print(type(subset))  # <class 'pandas.core.frame.DataFrame'>
print(subset.head())
```

**実行結果：**
```
=== 1つの列を取得 ===
<class 'pandas.core.series.Series'>
0         開発部
1         営業部
2    マーケティング部
3         総務部
4         営業部
Name: 部署, dtype: object

=== 複数の列を取得 ===
<class 'pandas.core.frame.DataFrame'>
         日付           部署     金額
0  2025/01/01       開発部  240000
1  2025/01/02       営業部   30000
2  2025/01/02 マーケティング部  250000
3  2025/01/03       総務部   40000
4  2025/01/04       営業部  210000
```

**重要：**
- 1列を取得 → `df['列名']` → **Series**（1次元データ）
- 複数列を取得 → `df[['列1', '列2']]` → **DataFrame**（2次元データ）

---

## Step 4：データを抽出（フィルタリング）する

条件に合うデータだけを取り出します。**これがpandasの真骨頂！**

```python
# ===================================================
# Step 4: データを抽出（フィルタリング）する
# ===================================================

import pandas as pd
df = pd.read_excel('売上データ.xlsx')

# ----- 条件1: 営業部のデータだけ抽出 -----
print("=== 営業部のデータ ===")
sales_dept = df[df['部署'] == '営業部']
print(f"件数: {len(sales_dept)}件")
print(sales_dept.head())
print()

# ----- 条件2: 金額が10万円以上 -----
print("=== 金額10万円以上 ===")
high_sales = df[df['金額'] >= 100000]
print(f"件数: {len(high_sales)}件")
print(high_sales.head())
print()

# ----- 条件3: 複数条件（AND） -----
print("=== 営業部 かつ 金額10万円以上 ===")
filtered = df[(df['部署'] == '営業部') & (df['金額'] >= 100000)]
print(f"件数: {len(filtered)}件")
print(filtered.head())
print()

# ----- 条件4: 複数条件（OR） -----
print("=== 営業部 または 開発部 ===")
two_depts = df[(df['部署'] == '営業部') | (df['部署'] == '開発部')]
print(f"件数: {len(two_depts)}件")
```

**実行結果：**
```
=== 営業部のデータ ===
件数: 27件
         日付   部署 商品名  数量   単価     金額
1  2025/01/02  営業部  商品A    3  10000   30000
4  2025/01/04  営業部  商品D    7  30000  210000
...

=== 金額10万円以上 ===
件数: 58件
         日付           部署 商品名  数量   単価     金額
0  2025/01/01       開発部  商品C    8  30000  240000
2  2025/01/02 マーケティング部  商品E    5  50000  250000
...

=== 営業部 かつ 金額10万円以上 ===
件数: 15件

=== 営業部 または 開発部 ===
件数: 53件
```

### コード解説（重要！）

```python
df[df['部署'] == '営業部']
```

これを分解すると：

```python
# Step 1: 条件式を評価 → True/Falseのリストができる
condition = df['部署'] == '営業部'
print(condition)
# 0    False  (開発部)
# 1     True  (営業部)
# 2    False  (マーケティング部)
# 3    False  (総務部)
# 4     True  (営業部)
# ...

# Step 2: Trueの行だけを取り出す
result = df[condition]
```

**複数条件のルール：**
- AND（かつ）: `&` を使い、各条件を `()` で囲む
- OR（または）: `|` を使い、各条件を `()` で囲む

```python
# 正しい書き方
df[(df['部署'] == '営業部') & (df['金額'] >= 100000)]

# 間違い（エラーになる）
df[df['部署'] == '営業部' & df['金額'] >= 100000]  # ()がない
df[df['部署'] == '営業部' and df['金額'] >= 100000]  # andは使えない
```

### GASとの比較

**GASで営業部のデータを抽出する場合（15行以上）：**

```javascript
function filterSalesDept() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('売上データ');
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(2, 1, lastRow - 1, 6).getValues();

  const salesDept = [];
  data.forEach(row => {
    if (row[1] === '営業部') {  // B列が部署
      salesDept.push(row);
    }
  });

  console.log(`営業部のデータ: ${salesDept.length}件`);
  salesDept.forEach(row => console.log(row));
}
```

**pandasの場合（1行）：**

```python
sales_dept = df[df['部署'] == '営業部']
```

---

## Step 5：データを集計する

集計処理がpandasの最強ポイントです。

```python
# ===================================================
# Step 5: データを集計する
# ===================================================

import pandas as pd
df = pd.read_excel('売上データ.xlsx')

# ----- 基本的な集計 -----
print("=== 金額の基本統計 ===")
print(f"合計: {df['金額'].sum():,}円")
print(f"平均: {df['金額'].mean():,.0f}円")
print(f"最大: {df['金額'].max():,}円")
print(f"最小: {df['金額'].min():,}円")
print(f"件数: {df['金額'].count()}件")
print()

# ----- グループ別集計（これが最強！） -----
print("=== 部署別売上合計 ===")
by_dept = df.groupby('部署')['金額'].sum()
print(by_dept)
print()

# ----- 複数の集計を同時に -----
print("=== 部署別サマリー ===")
summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
summary.columns = ['売上合計', '平均単価', '件数']
print(summary)
```

**実行結果：**
```
=== 金額の基本統計 ===
合計: 13,350,000円
平均: 133,500円
最大: 500,000円
最小: 10,000円
件数: 100件

=== 部署別売上合計 ===
部署
マーケティング部    3200000
営業部            3650000
総務部            2900000
開発部            3600000
Name: 金額, dtype: int64

=== 部署別サマリー ===
                売上合計      平均単価  件数
部署
マーケティング部   3200000  133333.33   24
営業部           3650000  135185.19   27
総務部           2900000  126086.96   23
開発部           3600000  138461.54   26
```

### groupbyを図解で理解する

```
元データ（df）
┌──────┬──────┬────────┐
│ 部署 │ 商品 │  金額  │
├──────┼──────┼────────┤
│営業部│商品A │  30000 │
│開発部│商品C │ 240000 │
│営業部│商品D │ 210000 │
│総務部│商品B │  40000 │
│開発部│商品A │ 150000 │
└──────┴──────┴────────┘
          ↓
   groupby('部署')
          ↓
┌─────────────────────────────┐
│ 営業部グループ: [30000, 210000] │
│ 開発部グループ: [240000, 150000]│
│ 総務部グループ: [40000]        │
└─────────────────────────────┘
          ↓
       .sum()
          ↓
┌─────────────────────────────┐
│ 営業部: 240000               │
│ 開発部: 390000               │
│ 総務部:  40000               │
└─────────────────────────────┘
```

### GASで同じ集計をすると…

```javascript
// GASの場合：約25行
function aggregateByDept() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('売上データ');
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(2, 1, lastRow - 1, 6).getValues();

  const salesByDept = {};

  data.forEach(row => {
    const dept = row[1];
    const amount = row[5];

    if (salesByDept[dept]) {
      salesByDept[dept].sum += amount;
      salesByDept[dept].count++;
    } else {
      salesByDept[dept] = { sum: amount, count: 1 };
    }
  });

  for (const dept in salesByDept) {
    const avg = salesByDept[dept].sum / salesByDept[dept].count;
    console.log(`${dept}: 合計${salesByDept[dept].sum}円, 平均${avg}円`);
  }
}
```

```python
# pandasの場合：1行
summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
```

**25行 → 1行。** これがpandasの威力です。

---

## Step 6：並び替えとランキング

```python
# ===================================================
# Step 6: 並び替えとランキング
# ===================================================

import pandas as pd
df = pd.read_excel('売上データ.xlsx')

# ----- 金額で降順ソート -----
print("=== 売上金額TOP10 ===")
top10 = df.sort_values('金額', ascending=False).head(10)
print(top10[['日付', '部署', '商品名', '金額']].to_string(index=False))
print()

# ----- 商品別売上ランキング -----
print("=== 商品別売上ランキング ===")
product_sales = df.groupby('商品名')['金額'].sum()
product_ranking = product_sales.sort_values(ascending=False)
print(product_ranking)
print()

# ----- 部署×商品のクロス集計 -----
print("=== 部署×商品のクロス集計 ===")
pivot = pd.pivot_table(df, values='金額', index='部署', columns='商品名', aggfunc='sum', fill_value=0)
print(pivot)
```

**実行結果：**
```
=== 売上金額TOP10 ===
       日付           部署 商品名     金額
2025/01/15       開発部  商品E  500000
2025/02/20 マーケティング部  商品E  450000
2025/03/05       営業部  商品E  400000
...

=== 商品別売上ランキング ===
商品名
商品E    3650000
商品C    3200000
商品D    2800000
商品B    2100000
商品A    1600000
Name: 金額, dtype: int64

=== 部署×商品のクロス集計 ===
商品名         商品A    商品B    商品C    商品D    商品E
部署
マーケティング部  300000  480000  720000  560000  1140000
営業部          520000  420000  800000  910000  1000000
総務部          380000  600000  640000  530000   750000
開発部          400000  600000  1040000  800000   760000
```

### コード解説

```python
df.sort_values('金額', ascending=False)
```
- `sort_values()`: 指定した列で並び替え
- `ascending=False`: 降順（大きい順）。Trueで昇順

```python
pd.pivot_table(df, values='金額', index='部署', columns='商品名', aggfunc='sum')
```
- `pivot_table()`: クロス集計表を作成
- `values`: 集計する値の列
- `index`: 縦軸
- `columns`: 横軸
- `aggfunc`: 集計方法（'sum', 'mean', 'count'など）

---

## Step 7：結果をExcelに保存する

```python
# ===================================================
# Step 7: 結果をExcelに保存する
# ===================================================

import pandas as pd
df = pd.read_excel('売上データ.xlsx')

# 各種集計を準備
dept_summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
dept_summary.columns = ['売上合計', '平均単価', '件数']

product_ranking = df.groupby('商品名')['金額'].sum().sort_values(ascending=False)
product_ranking = product_ranking.reset_index()
product_ranking.columns = ['商品名', '売上合計']

# 複数シートに保存
with pd.ExcelWriter('分析結果.xlsx') as writer:
    dept_summary.to_excel(writer, sheet_name='部署別集計')
    product_ranking.to_excel(writer, sheet_name='商品別ランキング', index=False)
    df.to_excel(writer, sheet_name='元データ', index=False)

print("✓ 分析結果.xlsx に保存しました")
print("  - シート1: 部署別集計")
print("  - シート2: 商品別ランキング")
print("  - シート3: 元データ")

# Colabでダウンロード
from google.colab import files
files.download('分析結果.xlsx')
```

**実行結果：**
```
✓ 分析結果.xlsx に保存しました
  - シート1: 部署別集計
  - シート2: 商品別ランキング
  - シート3: 元データ
```

---

## pandasでよく使うメソッド一覧

| メソッド | 説明 | 使用例 |
|---------|------|--------|
| `read_excel()` | Excel読み込み | `pd.read_excel('file.xlsx')` |
| `read_csv()` | CSV読み込み | `pd.read_csv('file.csv')` |
| `head()` | 先頭n行 | `df.head(10)` |
| `tail()` | 末尾n行 | `df.tail(5)` |
| `shape` | 行数・列数 | `df.shape` → `(100, 6)` |
| `columns` | 列名一覧 | `df.columns` |
| `dtypes` | データ型 | `df.dtypes` |
| `describe()` | 基本統計 | `df.describe()` |
| `groupby()` | グループ化 | `df.groupby('列名')` |
| `agg()` | 複数集計 | `.agg(['sum', 'mean'])` |
| `sort_values()` | 並び替え | `df.sort_values('列名')` |
| `to_excel()` | Excel保存 | `df.to_excel('file.xlsx')` |

---

## よくあるエラーと対処法

### エラー1: 列名が見つからない

```
KeyError: '部署名'
```

**原因：** 列名のタイプミス、または全角・半角の違い

**対処法：**
```python
# 列名を確認
print(df.columns.tolist())
# ['日付', '部署', '商品名', '数量', '単価', '金額']
# → '部署名'ではなく'部署'だった
```

### エラー2: 複数条件でエラー

```
ValueError: The truth value of a Series is ambiguous
```

**原因：** `and` や `or` を使っている

**対処法：**
```python
# 間違い
df[df['部署'] == '営業部' and df['金額'] >= 100000]

# 正解（& を使い、各条件を () で囲む）
df[(df['部署'] == '営業部') & (df['金額'] >= 100000)]
```

### エラー3: openpyxlがない

```
ImportError: Missing optional dependency 'openpyxl'
```

**対処法：**
```python
!pip install openpyxl
```

---

## このセクションのまとめ

### 学んだこと

- [ ] `pd.read_excel()`: Excelファイルの読み込み
- [ ] `df['列名']`: 列へのアクセス
- [ ] `df[条件]`: 条件によるフィルタリング
- [ ] `&` と `|`: 複数条件の組み合わせ
- [ ] `.sum()`, `.mean()`, `.count()`: 基本集計
- [ ] `.groupby()`: グループ別集計
- [ ] `.agg()`: 複数の集計を同時に実行
- [ ] `.sort_values()`: 並び替え
- [ ] `pd.pivot_table()`: クロス集計
- [ ] `.to_excel()`: Excel保存

### GASとの比較

| 処理 | GAS | pandas |
|------|-----|--------|
| 条件抽出 | if文でループ（10行以上） | 1行 |
| 部署別集計 | オブジェクトで手動集計（20行以上） | 1行 |
| 並び替え | sort()でループ | 1行 |
| クロス集計 | 自力で実装（30行以上） | 1行 |

---

## 次のステップ

pandasの基本を学びました。

次のセクション（3-3）では、**GASの6分制限を超える大量データ処理**を体験します。
10万行のデータをpandasで処理し、GASとの速度差を実感してください。
