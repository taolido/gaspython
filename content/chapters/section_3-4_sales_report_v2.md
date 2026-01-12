# 3-4. 【実践】グラフ付き売上レポート自動生成

## この節で学ぶこと

- 売上データを読み込んで集計する
- Excelにグラフを自動挿入する
- 見栄えの良いレポートを自動生成する
- 経理部に渡せる品質のExcelを作る

---

## 完成イメージ

この節で作るレポート：

```
┌─────────────────────────────────────────────────────────────┐
│  売上レポート_2024年1月.xlsx                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  【Sheet1: サマリー】                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  2024年1月 売上レポート                              │   │
│  │                                                       │   │
│  │  総売上: ¥12,345,678                                 │   │
│  │  取引件数: 156件                                      │   │
│  │  平均単価: ¥79,139                                   │   │
│  │                                                       │   │
│  │  📊 部門別売上グラフ                                 │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │ 営業部 ████████████████ 52%                │    │   │
│  │  │ 開発部 ██████████ 33%                      │    │   │
│  │  │ 総務部 █████ 15%                           │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  【Sheet2: 詳細データ】                                      │
│  日付 | 部署 | 商品 | 金額 | ...                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**「経理部に毎月渡すレポート」を自動生成します。**

---

## Step 0: サンプル売上データを作成

まずは練習用のデータを作成します。

```python
# ===== Step 0: サンプル売上データを作成 =====
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 再現可能な乱数
np.random.seed(42)

# データ生成
n_rows = 200
departments = ['営業部', '開発部', '総務部']
products = ['商品A', '商品B', '商品C', '商品D']
sales_reps = ['田中', '鈴木', '佐藤', '高橋', '伊藤', '渡辺']

# 2024年1月の日付を生成
base_date = datetime(2024, 1, 1)
dates = [base_date + timedelta(days=np.random.randint(0, 31)) for _ in range(n_rows)]

data = {
    '日付': dates,
    '部署': np.random.choice(departments, n_rows, p=[0.5, 0.35, 0.15]),  # 営業部多め
    '担当者': np.random.choice(sales_reps, n_rows),
    '商品': np.random.choice(products, n_rows),
    '数量': np.random.randint(1, 20, n_rows),
    '単価': np.random.choice([10000, 15000, 20000, 30000, 50000], n_rows)
}

df = pd.DataFrame(data)
df['金額'] = df['数量'] * df['単価']

# 日付でソート
df = df.sort_values('日付').reset_index(drop=True)

# 保存
df.to_excel('sales_data_202401.xlsx', index=False)

print("【サンプルデータ作成完了】")
print(f"ファイル: sales_data_202401.xlsx")
print(f"行数: {len(df)}")
print(f"\n【データプレビュー】")
print(df.head(10))
print(f"\n【集計】")
print(f"総売上: ¥{df['金額'].sum():,}")
```

**実行結果：**
```
【サンプルデータ作成完了】
ファイル: sales_data_202401.xlsx
行数: 200

【データプレビュー】
         日付    部署 担当者   商品  数量    単価      金額
0  2024-01-01  営業部   高橋  商品C    11  30000   330000
1  2024-01-01  開発部   鈴木  商品A     8  20000   160000
2  2024-01-01  営業部   佐藤  商品B    15  15000   225000
...

【集計】
総売上: ¥52,830,000
```

---

## Step 1: データを読み込んで集計

```python
# ===== Step 1: データ読み込みと集計 =====
import pandas as pd

# データ読み込み
df = pd.read_excel('sales_data_202401.xlsx')

print("【基本統計】")
print(f"総売上: ¥{df['金額'].sum():,}")
print(f"取引件数: {len(df)}件")
print(f"平均単価: ¥{df['金額'].mean():,.0f}")

# 部門別集計
dept_summary = df.groupby('部署').agg({
    '金額': ['sum', 'count', 'mean']
}).round(0)
dept_summary.columns = ['売上合計', '件数', '平均単価']
dept_summary = dept_summary.sort_values('売上合計', ascending=False)

print("\n【部門別売上】")
print(dept_summary)

# 商品別集計
product_summary = df.groupby('商品').agg({
    '金額': 'sum',
    '数量': 'sum'
}).sort_values('金額', ascending=False)

print("\n【商品別売上】")
print(product_summary)

# 担当者別集計
rep_summary = df.groupby('担当者')['金額'].sum().sort_values(ascending=False)
print("\n【担当者別売上TOP3】")
print(rep_summary.head(3))
```

**実行結果：**
```
【基本統計】
総売上: ¥52,830,000
取引件数: 200件
平均単価: ¥264,150

【部門別売上】
        売上合計   件数     平均単価
部署
営業部  27345000    99   276212.0
開発部  18130000    72   251806.0
総務部   7355000    29   253621.0

【商品別売上】
       金額   数量
商品
商品D  16250000   85
商品C  14820000  102
商品A  11505000   88
商品B  10255000   92

【担当者別売上TOP3】
担当者
高橋    11780000
田中    10420000
鈴木     9085000
Name: 金額, dtype: int64
```

---

## Step 2: グラフ付きレポートを生成

openpyxlでExcelにグラフを挿入します。

```python
# ===== Step 2: グラフ付きレポート生成 =====
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

# データ読み込み
df = pd.read_excel('sales_data_202401.xlsx')

# 集計
total_sales = df['金額'].sum()
total_count = len(df)
avg_price = df['金額'].mean()

dept_summary = df.groupby('部署')['金額'].sum().sort_values(ascending=False)
product_summary = df.groupby('商品')['金額'].sum().sort_values(ascending=False)

# ===== Excelワークブック作成 =====
wb = Workbook()

# ----- Sheet1: サマリー -----
ws_summary = wb.active
ws_summary.title = "サマリー"

# タイトル
ws_summary['A1'] = "2024年1月 売上レポート"
ws_summary['A1'].font = Font(size=18, bold=True)
ws_summary.merge_cells('A1:E1')

# 基本統計
ws_summary['A3'] = "基本統計"
ws_summary['A3'].font = Font(size=14, bold=True)

stats = [
    ('総売上', f'¥{total_sales:,}'),
    ('取引件数', f'{total_count}件'),
    ('平均単価', f'¥{avg_price:,.0f}'),
]
for i, (label, value) in enumerate(stats, start=4):
    ws_summary[f'A{i}'] = label
    ws_summary[f'B{i}'] = value
    ws_summary[f'A{i}'].font = Font(bold=True)

# 部門別売上データ（グラフ用）
ws_summary['A8'] = "部門別売上"
ws_summary['A8'].font = Font(size=14, bold=True)

ws_summary['A9'] = "部署"
ws_summary['B9'] = "売上"
for i, (dept, sales) in enumerate(dept_summary.items(), start=10):
    ws_summary[f'A{i}'] = dept
    ws_summary[f'B{i}'] = sales

# 部門別棒グラフ
chart1 = BarChart()
chart1.type = "col"
chart1.title = "部門別売上"
chart1.y_axis.title = "売上（円）"
chart1.x_axis.title = "部門"

data = Reference(ws_summary, min_col=2, min_row=9, max_row=12)
cats = Reference(ws_summary, min_col=1, min_row=10, max_row=12)
chart1.add_data(data, titles_from_data=True)
chart1.set_categories(cats)
chart1.shape = 4
chart1.width = 12
chart1.height = 8

ws_summary.add_chart(chart1, "D3")

# 商品別売上データ
ws_summary['A15'] = "商品別売上"
ws_summary['A15'].font = Font(size=14, bold=True)

ws_summary['A16'] = "商品"
ws_summary['B16'] = "売上"
for i, (product, sales) in enumerate(product_summary.items(), start=17):
    ws_summary[f'A{i}'] = product
    ws_summary[f'B{i}'] = sales

# 商品別円グラフ
chart2 = PieChart()
chart2.title = "商品別売上構成"

data = Reference(ws_summary, min_col=2, min_row=16, max_row=20)
cats = Reference(ws_summary, min_col=1, min_row=17, max_row=20)
chart2.add_data(data, titles_from_data=True)
chart2.set_categories(cats)
chart2.width = 10
chart2.height = 8

# データラベル表示
chart2.dataLabels = DataLabelList()
chart2.dataLabels.showPercent = True
chart2.dataLabels.showVal = False
chart2.dataLabels.showCatName = True

ws_summary.add_chart(chart2, "D15")

# ----- Sheet2: 詳細データ -----
ws_detail = wb.create_sheet(title="詳細データ")

# DataFrameをシートに書き込み
for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), start=1):
    for c_idx, value in enumerate(row, start=1):
        cell = ws_detail.cell(row=r_idx, column=c_idx, value=value)
        if r_idx == 1:  # ヘッダー行
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.font = Font(bold=True, color="FFFFFF")

# 列幅調整
ws_detail.column_dimensions['A'].width = 12
ws_detail.column_dimensions['B'].width = 10
ws_detail.column_dimensions['C'].width = 10
ws_detail.column_dimensions['D'].width = 10
ws_detail.column_dimensions['E'].width = 8
ws_detail.column_dimensions['F'].width = 10
ws_detail.column_dimensions['G'].width = 12

# ----- 保存 -----
output_file = '売上レポート_2024年1月.xlsx'
wb.save(output_file)

print(f"レポートを生成しました: {output_file}")
print(f"\n【レポート構成】")
print(f"  Sheet1: サマリー（基本統計 + グラフ2つ）")
print(f"  Sheet2: 詳細データ（{len(df)}行）")
```

**実行結果：**
```
レポートを生成しました: 売上レポート_2024年1月.xlsx

【レポート構成】
  Sheet1: サマリー（基本統計 + グラフ2つ）
  Sheet2: 詳細データ（200行）
```

---

## Step 3: 完成コード（コピペで使える）

ここまでの処理を1つのスクリプトにまとめます。

```python
# ===== 売上レポート自動生成ツール =====
# sales_report_generator.py
#
# 使い方:
# 1. sales_data_YYYYMM.xlsx を同じフォルダに置く
# 2. このスクリプトを実行
# 3. 「売上レポート_YYYY年MM月.xlsx」が生成される

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import glob
from datetime import datetime

def generate_sales_report(input_file):
    """売上データからグラフ付きレポートを生成"""

    # ===== 1. データ読み込み =====
    print(f"読み込み中: {input_file}")
    df = pd.read_excel(input_file)

    # ファイル名から年月を取得
    # 例: sales_data_202401.xlsx → 2024年1月
    basename = os.path.basename(input_file)
    if 'sales_data_' in basename:
        ym = basename.replace('sales_data_', '').replace('.xlsx', '')
        year = ym[:4]
        month = ym[4:6]
        title = f"{year}年{int(month)}月 売上レポート"
    else:
        title = "売上レポート"
        year = datetime.now().year
        month = datetime.now().month

    # ===== 2. 集計 =====
    total_sales = df['金額'].sum()
    total_count = len(df)
    avg_price = df['金額'].mean()

    dept_summary = df.groupby('部署')['金額'].sum().sort_values(ascending=False)
    product_summary = df.groupby('商品')['金額'].sum().sort_values(ascending=False)

    # ===== 3. レポート生成 =====
    wb = Workbook()

    # ----- Sheet1: サマリー -----
    ws = wb.active
    ws.title = "サマリー"

    # タイトル
    ws['A1'] = title
    ws['A1'].font = Font(size=18, bold=True)
    ws.merge_cells('A1:E1')

    # 基本統計
    ws['A3'] = "基本統計"
    ws['A3'].font = Font(size=14, bold=True)

    ws['A4'] = "総売上"
    ws['B4'] = f'¥{total_sales:,}'
    ws['A5'] = "取引件数"
    ws['B5'] = f'{total_count}件'
    ws['A6'] = "平均単価"
    ws['B6'] = f'¥{avg_price:,.0f}'

    for i in range(4, 7):
        ws[f'A{i}'].font = Font(bold=True)

    # 部門別売上
    ws['A8'] = "部門別売上"
    ws['A8'].font = Font(size=14, bold=True)
    ws['A9'] = "部署"
    ws['B9'] = "売上"

    for i, (dept, sales) in enumerate(dept_summary.items(), start=10):
        ws[f'A{i}'] = dept
        ws[f'B{i}'] = sales

    # 棒グラフ
    chart1 = BarChart()
    chart1.type = "col"
    chart1.title = "部門別売上"
    data = Reference(ws, min_col=2, min_row=9, max_row=9+len(dept_summary))
    cats = Reference(ws, min_col=1, min_row=10, max_row=9+len(dept_summary))
    chart1.add_data(data, titles_from_data=True)
    chart1.set_categories(cats)
    chart1.width = 12
    chart1.height = 8
    ws.add_chart(chart1, "D3")

    # 商品別売上
    start_row = 10 + len(dept_summary) + 2
    ws[f'A{start_row}'] = "商品別売上"
    ws[f'A{start_row}'].font = Font(size=14, bold=True)
    ws[f'A{start_row+1}'] = "商品"
    ws[f'B{start_row+1}'] = "売上"

    for i, (product, sales) in enumerate(product_summary.items(), start=start_row+2):
        ws[f'A{i}'] = product
        ws[f'B{i}'] = sales

    # 円グラフ
    chart2 = PieChart()
    chart2.title = "商品別売上構成"
    data = Reference(ws, min_col=2, min_row=start_row+1, max_row=start_row+1+len(product_summary))
    cats = Reference(ws, min_col=1, min_row=start_row+2, max_row=start_row+1+len(product_summary))
    chart2.add_data(data, titles_from_data=True)
    chart2.set_categories(cats)
    chart2.width = 10
    chart2.height = 8
    chart2.dataLabels = DataLabelList()
    chart2.dataLabels.showPercent = True
    chart2.dataLabels.showCatName = True
    ws.add_chart(chart2, "D15")

    # ----- Sheet2: 詳細データ -----
    ws_detail = wb.create_sheet(title="詳細データ")

    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), start=1):
        for c_idx, value in enumerate(row, start=1):
            cell = ws_detail.cell(row=r_idx, column=c_idx, value=value)
            if r_idx == 1:
                cell.fill = PatternFill(start_color="4472C4", fill_type="solid")
                cell.font = Font(bold=True, color="FFFFFF")

    # 列幅調整
    for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        ws_detail.column_dimensions[col].width = 12

    # ===== 4. 保存 =====
    output_file = f'売上レポート_{year}年{int(month)}月.xlsx'
    wb.save(output_file)

    return output_file, total_sales, total_count

# ===== メイン処理 =====
if __name__ == "__main__":
    print("=" * 50)
    print("  売上レポート自動生成ツール")
    print("=" * 50)

    # 売上データファイルを検索
    files = glob.glob('sales_data_*.xlsx')

    if not files:
        print("\n❌ エラー: sales_data_*.xlsx が見つかりません")
        print("   sales_data_YYYYMM.xlsx 形式のファイルを配置してください")
    else:
        print(f"\n処理対象ファイル: {len(files)}件")
        for f in files:
            output, sales, count = generate_sales_report(f)
            print(f"\n✅ レポート生成完了")
            print(f"   入力: {f}")
            print(f"   出力: {output}")
            print(f"   総売上: ¥{sales:,}")
            print(f"   件数: {count}件")

    print("\n" + "=" * 50)
    input("Enterキーで終了...")
```

---

## GASとの比較

```javascript
// GAS: スプレッドシートにグラフを追加（簡易版）
function createChart() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getRange('A1:B10');

  const chart = sheet.newChart()
    .setChartType(Charts.ChartType.BAR)
    .addRange(range)
    .setPosition(1, 4, 0, 0)
    .build();

  sheet.insertChart(chart);
}
// ※ Excelファイルへの出力は不可
```

```python
# Python: Excelにグラフを追加
from openpyxl.chart import BarChart, Reference

chart = BarChart()
chart.title = "売上グラフ"
data = Reference(ws, min_col=2, min_row=1, max_row=10)
chart.add_data(data)
ws.add_chart(chart, "D1")
wb.save('output.xlsx')
# → Excelファイルとして保存可能
```

**Pythonの優位点:**
- Excelファイル（.xlsx）に直接グラフを埋め込める
- ファイルをそのまま配布可能
- スプレッドシートへの変換不要

---

## よくあるエラーと対処法

### エラー1: openpyxl.chart がインポートできない

```
ModuleNotFoundError: No module named 'openpyxl.chart'
```

**対処法:** openpyxlが正しくインストールされているか確認

```
pip install openpyxl --upgrade
```

### エラー2: グラフが表示されない

```
ExcelでファイルをいたがグラフがEmpty
```

**対処法:** データ範囲の指定を確認

```python
# 間違い: データがない範囲を指定
data = Reference(ws, min_col=2, min_row=1, max_row=1)  # 1行だけ

# 正しい: データがある範囲を指定
data = Reference(ws, min_col=2, min_row=1, max_row=10)  # 複数行
```

---

## この節のまとめ

- `openpyxl.chart` でExcelにグラフを埋め込める
- `BarChart`（棒グラフ）、`PieChart`（円グラフ）が使える
- `Reference` でデータ範囲を指定
- pandasで集計 → openpyxlでレポート化のパターンが強力
- 経理部に渡せる品質のExcelレポートを自動生成できた

**次の節では、100枚のExcelファイルを3秒で統合するツールを作ります！**
