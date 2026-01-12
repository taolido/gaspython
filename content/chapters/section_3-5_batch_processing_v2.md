# 3-5. 【実践】複数ファイル一括処理

## この節で学ぶこと

- 複数のExcelファイルを自動検出する
- ファイルを1つに統合する
- 各ファイルに同じ処理を適用する
- フォルダ構造を活用した処理

---

## Step 0: なぜ複数ファイル処理が重要か

実務では、こんな状況がよくあります：

```
月次売上フォルダ/
├── sales_2024_01.xlsx
├── sales_2024_02.xlsx
├── sales_2024_03.xlsx
├── ...
└── sales_2024_12.xlsx

→ これを1つのファイルに統合して、年間集計したい！
```

### GASの場合の問題点

GASでこれをやろうとすると：
- Googleドライブのファイル一覧を取得するコードが必要
- 各ファイルを開いて読み込むのに時間がかかる
- 12ファイル処理で6分制限に引っかかる可能性

Pythonなら、数行のコードで一瞬です。

---

## Step 1: サンプルファイルを作成する

まずは練習用に、複数のサンプルファイルを作成しましょう。

```python
# ===== Step 1: 3ヶ月分のサンプル売上ファイルを作成 =====
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

months = ['01', '02', '03']
departments = ['営業部', '開発部', '総務部']
products = ['商品A', '商品B', '商品C']

for month in months:
    # 月ごとにデータを生成
    n_rows = 100  # 各ファイル100行

    # その月の日付を生成
    year = 2024
    month_int = int(month)

    # 月の日数を取得
    if month_int in [1, 3, 5, 7, 8, 10, 12]:
        days_in_month = 31
    elif month_int in [4, 6, 9, 11]:
        days_in_month = 30
    else:
        days_in_month = 29  # 2024年はうるう年

    dates = [datetime(year, month_int, np.random.randint(1, days_in_month + 1))
             for _ in range(n_rows)]

    data = {
        '日付': dates,
        '部署': np.random.choice(departments, n_rows),
        '商品名': np.random.choice(products, n_rows),
        '金額': np.random.randint(5000, 50000, n_rows)
    }

    df = pd.DataFrame(data)
    filename = f'sales_2024_{month}.xlsx'
    df.to_excel(filename, index=False)
    print(f"作成: {filename} ({len(df)}行)")

print("\n3ファイルの作成が完了しました！")
```

**実行結果：**
```
作成: sales_2024_01.xlsx (100行)
作成: sales_2024_02.xlsx (100行)
作成: sales_2024_03.xlsx (100行)

3ファイルの作成が完了しました！
```

### コード解説

```python
for month in months:
    ...
    df.to_excel(filename, index=False)
```
- `for`ループで各月のファイルを順番に作成
- `index=False` でDataFrameの行番号を出力しない

```python
filename = f'sales_2024_{month}.xlsx'
```
- f文字列で動的にファイル名を生成
- `month` が '01' なら `sales_2024_01.xlsx` になる

---

## Step 2: ファイル一覧を取得する

作成したファイルの一覧を取得してみましょう。

### Colab環境の場合

```python
# ===== Step 2: Colabでファイル一覧を取得 =====
import os

# 現在のディレクトリのファイル一覧
all_files = os.listdir('.')
print("現在のディレクトリ内のファイル:")
for f in all_files:
    print(f"  {f}")

# Excelファイルのみ抽出
excel_files = [f for f in all_files if f.endswith('.xlsx')]
print(f"\nExcelファイル ({len(excel_files)}個):")
for f in sorted(excel_files):
    print(f"  {f}")
```

**実行結果：**
```
現在のディレクトリ内のファイル:
  .config
  sample_data
  sales_2024_01.xlsx
  sales_2024_02.xlsx
  sales_2024_03.xlsx

Excelファイル (3個):
  sales_2024_01.xlsx
  sales_2024_02.xlsx
  sales_2024_03.xlsx
```

### パターンマッチングでファイルを取得

特定のパターンに一致するファイルだけを取得する方法です。

```python
# ===== パターンマッチングでファイル取得 =====
import glob

# sales_2024_*.xlsx に一致するファイルを取得
sales_files = glob.glob('sales_2024_*.xlsx')
print(f"sales_2024_*.xlsx に一致するファイル:")
for f in sorted(sales_files):
    print(f"  {f}")

# 他のパターン例
# glob.glob('*.xlsx')        → すべてのExcelファイル
# glob.glob('data/*.xlsx')   → dataフォルダ内のExcelファイル
# glob.glob('**/*.xlsx', recursive=True)  → サブフォルダも含めて検索
```

**実行結果：**
```
sales_2024_*.xlsx に一致するファイル:
  sales_2024_01.xlsx
  sales_2024_02.xlsx
  sales_2024_03.xlsx
```

### コード解説

```python
import glob
sales_files = glob.glob('sales_2024_*.xlsx')
```
- `glob.glob()` はワイルドカード（`*`）を使ってファイルを検索
- `*` は「任意の文字列」を意味する
- `sales_2024_*.xlsx` は「sales_2024_で始まり.xlsxで終わるファイル」

```python
[f for f in all_files if f.endswith('.xlsx')]
```
- リスト内包表記でフィルタリング
- `f.endswith('.xlsx')` は「.xlsxで終わるか」をチェック

---

## Step 3: 複数ファイルを統合する

取得したファイルを1つのDataFrameに統合しましょう。

```python
# ===== Step 3: 複数ファイルを1つに統合 =====
import pandas as pd
import glob

# ファイル一覧を取得
files = sorted(glob.glob('sales_2024_*.xlsx'))
print(f"統合対象: {len(files)}ファイル")

# 各ファイルを読み込んでリストに追加
all_dataframes = []

for filepath in files:
    # ファイルを読み込み
    df = pd.read_excel(filepath)

    # どのファイルから来たかを記録（後で確認用）
    df['元ファイル'] = filepath

    # リストに追加
    all_dataframes.append(df)

    print(f"  読込: {filepath} ({len(df)}行)")

# 縦に結合
combined = pd.concat(all_dataframes, ignore_index=True)

print(f"\n統合完了: 合計 {len(combined)}行")
print(f"\n最初の5行:")
print(combined.head())
print(f"\n最後の5行:")
print(combined.tail())
```

**実行結果：**
```
統合対象: 3ファイル
  読込: sales_2024_01.xlsx (100行)
  読込: sales_2024_02.xlsx (100行)
  読込: sales_2024_03.xlsx (100行)

統合完了: 合計 300行

最初の5行:
         日付   部署 商品名     金額           元ファイル
0 2024-01-15  営業部  商品A  23456  sales_2024_01.xlsx
1 2024-01-08  開発部  商品C  34567  sales_2024_01.xlsx
2 2024-01-22  総務部  商品B  12345  sales_2024_01.xlsx
3 2024-01-03  営業部  商品A  45678  sales_2024_01.xlsx
4 2024-01-29  開発部  商品B  28901  sales_2024_01.xlsx

最後の5行:
           日付   部署 商品名     金額           元ファイル
295 2024-03-18  営業部  商品C  31234  sales_2024_03.xlsx
296 2024-03-05  総務部  商品A  19876  sales_2024_03.xlsx
297 2024-03-27  開発部  商品B  42345  sales_2024_03.xlsx
298 2024-03-11  営業部  商品C  26789  sales_2024_03.xlsx
299 2024-03-21  総務部  商品A  38901  sales_2024_03.xlsx
```

### コード解説

```python
all_dataframes = []
for filepath in files:
    df = pd.read_excel(filepath)
    all_dataframes.append(df)
```
- 空のリストを作成
- 各ファイルを読み込んでDataFrameをリストに追加
- これは「リストにDataFrameを溜めていく」パターン

```python
combined = pd.concat(all_dataframes, ignore_index=True)
```
- `pd.concat()` でリスト内のDataFrameを縦に結合
- `ignore_index=True` で行番号を0から振り直す

```python
df['元ファイル'] = filepath
```
- 新しい列を追加
- どのファイルから来たデータかを記録（デバッグや確認に便利）

### 図解：pd.concatの動作

```
sales_2024_01.xlsx        sales_2024_02.xlsx        sales_2024_03.xlsx
┌────────────────┐        ┌────────────────┐        ┌────────────────┐
│  日付 │ 部署  │        │  日付 │ 部署  │        │  日付 │ 部署  │
├───────┼───────┤        ├───────┼───────┤        ├───────┼───────┤
│ 1/15  │ 営業部│        │ 2/10  │ 開発部│        │ 3/05  │ 総務部│
│ 1/08  │ 開発部│        │ 2/18  │ 営業部│        │ 3/12  │ 営業部│
│ ...   │ ...  │        │ ...   │ ...  │        │ ...   │ ...  │
└────────────────┘        └────────────────┘        └────────────────┘
        │                         │                         │
        └────────────────────────┬────────────────────────┘
                                 │
                         pd.concat()
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  日付 │ 部署  │元ファイル│
                    ├───────┼───────┼─────────┤
                    │ 1/15  │ 営業部│ 01.xlsx │
                    │ 1/08  │ 開発部│ 01.xlsx │
                    │ ...   │ ...  │ ...     │
                    │ 2/10  │ 開発部│ 02.xlsx │
                    │ 2/18  │ 営業部│ 02.xlsx │
                    │ ...   │ ...  │ ...     │
                    │ 3/05  │ 総務部│ 03.xlsx │
                    │ 3/12  │ 営業部│ 03.xlsx │
                    │ ...   │ ...  │ ...     │
                    └────────────────────────┘
                           統合後のDataFrame
```

---

## Step 4: 統合データを集計・保存する

統合したデータを集計して、結果を保存しましょう。

```python
# ===== Step 4: 統合データを集計・保存 =====
import pandas as pd

# 月を抽出
combined['月'] = pd.to_datetime(combined['日付']).dt.month

# ----- 集計1: 月別売上 -----
monthly_sales = combined.groupby('月')['金額'].agg(['sum', 'mean', 'count'])
monthly_sales.columns = ['売上合計', '平均単価', '件数']
print("【月別売上】")
print(monthly_sales)

# ----- 集計2: 部署別売上 -----
dept_sales = combined.groupby('部署')['金額'].sum().sort_values(ascending=False)
print("\n【部署別売上】")
print(dept_sales)

# ----- 集計3: 部署×月のクロス集計 -----
cross_table = combined.pivot_table(
    values='金額',
    index='部署',
    columns='月',
    aggfunc='sum',
    fill_value=0
)
print("\n【部署×月クロス集計】")
print(cross_table)

# ----- 結果を保存 -----
with pd.ExcelWriter('統合集計結果.xlsx') as writer:
    combined.to_excel(writer, sheet_name='統合データ', index=False)
    monthly_sales.to_excel(writer, sheet_name='月別集計')
    dept_sales.to_frame('売上').to_excel(writer, sheet_name='部署別集計')
    cross_table.to_excel(writer, sheet_name='クロス集計')

print("\n→ '統合集計結果.xlsx' に保存しました")

# Colabでダウンロード
try:
    from google.colab import files
    files.download('統合集計結果.xlsx')
except:
    pass
```

**実行結果：**
```
【月別売上】
      売上合計     平均単価  件数
月
1    2734567   27345.67  100
2    2612345   26123.45  100
3    2856789   28567.89  100

【部署別売上】
部署
営業部      3012345
開発部      2789012
総務部      2401344
Name: 金額, dtype: int64

【部署×月クロス集計】
月            1         2         3
部署
営業部   987654   1012345   1012346
開発部   912345    867890   1008777
総務部   834568    732110    834666

→ '統合集計結果.xlsx' に保存しました
```

---

## Step 5: 各ファイルに同じ処理を適用する

統合ではなく、各ファイルに同じ処理を行いたい場合もあります。

例：「各月の売上ファイルに、部署別集計シートを追加したい」

```python
# ===== Step 5: 各ファイルに同じ処理を適用 =====
import pandas as pd
import glob

files = sorted(glob.glob('sales_2024_*.xlsx'))

for filepath in files:
    print(f"\n処理中: {filepath}")

    # 1. ファイルを読み込み
    df = pd.read_excel(filepath)
    print(f"  データ件数: {len(df)}行")

    # 2. 部署別集計を計算
    dept_summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
    dept_summary.columns = ['売上合計', '平均単価', '件数']

    # 3. 商品別集計を計算
    product_summary = df.groupby('商品名')['金額'].agg(['sum', 'count'])
    product_summary.columns = ['売上合計', '件数']

    # 4. 新しいファイル名で保存（元データ + 集計シート）
    output_filename = filepath.replace('.xlsx', '_集計付.xlsx')

    with pd.ExcelWriter(output_filename) as writer:
        df.to_excel(writer, sheet_name='元データ', index=False)
        dept_summary.to_excel(writer, sheet_name='部署別集計')
        product_summary.to_excel(writer, sheet_name='商品別集計')

    print(f"  → 保存: {output_filename}")

print("\n全ファイルの処理が完了しました！")
```

**実行結果：**
```
処理中: sales_2024_01.xlsx
  データ件数: 100行
  → 保存: sales_2024_01_集計付.xlsx

処理中: sales_2024_02.xlsx
  データ件数: 100行
  → 保存: sales_2024_02_集計付.xlsx

処理中: sales_2024_03.xlsx
  データ件数: 100行
  → 保存: sales_2024_03_集計付.xlsx

全ファイルの処理が完了しました！
```

### コード解説

```python
output_filename = filepath.replace('.xlsx', '_集計付.xlsx')
```
- 文字列の置換で新しいファイル名を生成
- `sales_2024_01.xlsx` → `sales_2024_01_集計付.xlsx`

```python
with pd.ExcelWriter(output_filename) as writer:
    df.to_excel(writer, sheet_name='元データ', index=False)
    dept_summary.to_excel(writer, sheet_name='部署別集計')
```
- `ExcelWriter` を使うと複数シートを持つExcelファイルを作成できる
- `with` 文で使うと、処理後に自動でファイルが閉じられる

---

## Step 6: Colabで複数ファイルをアップロードして処理

Colabでは、複数ファイルを一度にアップロードして処理できます。

```python
# ===== Step 6: Colabで複数ファイルをアップロード =====
from google.colab import files
import pandas as pd

# 複数ファイルをアップロード
print("処理したいExcelファイルを選択してください（複数選択可）")
uploaded = files.upload()

# アップロードされたExcelファイルを取得
excel_files = [f for f in uploaded.keys() if f.endswith('.xlsx')]
print(f"\n{len(excel_files)}個のExcelファイルがアップロードされました")

# 統合処理
all_data = []
for filename in excel_files:
    df = pd.read_excel(filename)
    df['元ファイル'] = filename
    all_data.append(df)
    print(f"  読込: {filename} ({len(df)}行)")

# 結合
if len(all_data) > 0:
    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n統合完了: 合計 {len(combined)}行")

    # 保存してダウンロード
    combined.to_excel('アップロードファイル統合.xlsx', index=False)
    files.download('アップロードファイル統合.xlsx')
else:
    print("Excelファイルがアップロードされていません")
```

---

## Step 7: 完全版 - 複数ファイル一括処理ツール

学んだことを組み合わせて、汎用的なツールを作りましょう。

```python
# ===== 複数ファイル一括処理ツール（完全版） =====
import pandas as pd
import glob
import os
from datetime import datetime

def batch_process_excel_files(file_pattern, output_folder='output'):
    """
    指定パターンのExcelファイルを一括処理する

    Parameters:
    -----------
    file_pattern : str
        処理対象のファイルパターン（例: 'sales_*.xlsx'）
    output_folder : str
        出力先フォルダ名（デフォルト: 'output'）

    Returns:
    --------
    pd.DataFrame
        統合されたデータ
    """

    print("="*60)
    print("複数ファイル一括処理ツール")
    print("="*60)

    # 出力フォルダを作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"\n出力フォルダを作成: {output_folder}/")

    # ファイル一覧を取得
    files = sorted(glob.glob(file_pattern))
    if len(files) == 0:
        print(f"エラー: '{file_pattern}' に一致するファイルがありません")
        return None

    print(f"\n処理対象: {len(files)}ファイル")
    for f in files:
        print(f"  - {f}")

    # ===== 処理開始 =====
    all_data = []
    file_summaries = []

    for filepath in files:
        print(f"\n処理中: {filepath}")

        # ファイルを読み込み
        df = pd.read_excel(filepath)
        print(f"  → {len(df)}行のデータ")

        # メタデータを追加
        df['元ファイル'] = os.path.basename(filepath)

        # ファイルごとのサマリーを記録
        summary = {
            'ファイル名': os.path.basename(filepath),
            '行数': len(df),
            '列数': len(df.columns) - 1,  # 元ファイル列を除く
        }

        # 金額列があれば集計
        if '金額' in df.columns:
            summary['売上合計'] = df['金額'].sum()
            summary['平均単価'] = df['金額'].mean()

        file_summaries.append(summary)
        all_data.append(df)

    # ===== 統合 =====
    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n統合完了: 合計 {len(combined)}行")

    # ===== 集計処理 =====
    print("\n集計処理中...")

    # ファイル別サマリー
    summary_df = pd.DataFrame(file_summaries)

    # 部署別集計（部署列がある場合）
    dept_summary = None
    if '部署' in combined.columns and '金額' in combined.columns:
        dept_summary = combined.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
        dept_summary.columns = ['売上合計', '平均単価', '件数']

    # 月別集計（日付列がある場合）
    monthly_summary = None
    if '日付' in combined.columns and '金額' in combined.columns:
        combined['月'] = pd.to_datetime(combined['日付']).dt.month
        monthly_summary = combined.groupby('月')['金額'].agg(['sum', 'mean', 'count'])
        monthly_summary.columns = ['売上合計', '平均単価', '件数']

    # ===== 結果を保存 =====
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'{output_folder}/統合結果_{timestamp}.xlsx'

    with pd.ExcelWriter(output_file) as writer:
        # 統合データ
        combined.to_excel(writer, sheet_name='統合データ', index=False)

        # ファイル別サマリー
        summary_df.to_excel(writer, sheet_name='ファイル別サマリー', index=False)

        # 部署別集計
        if dept_summary is not None:
            dept_summary.to_excel(writer, sheet_name='部署別集計')

        # 月別集計
        if monthly_summary is not None:
            monthly_summary.to_excel(writer, sheet_name='月別集計')

    print(f"\n→ 保存完了: {output_file}")

    # ===== レポート出力 =====
    print("\n" + "="*60)
    print("処理結果サマリー")
    print("="*60)
    print(f"\n処理ファイル数: {len(files)}")
    print(f"統合後データ行数: {len(combined)}")

    if '金額' in combined.columns:
        print(f"売上合計: ¥{combined['金額'].sum():,.0f}")

    print(f"\n出力ファイル: {output_file}")

    # Colabならダウンロード
    try:
        from google.colab import files
        files.download(output_file)
        print("→ ダウンロードが開始されました")
    except:
        pass

    return combined


# ===== ツールを実行 =====
# サンプルファイルを処理
result = batch_process_excel_files('sales_2024_*.xlsx')
```

**実行結果：**
```
============================================================
複数ファイル一括処理ツール
============================================================

出力フォルダを作成: output/

処理対象: 3ファイル
  - sales_2024_01.xlsx
  - sales_2024_02.xlsx
  - sales_2024_03.xlsx

処理中: sales_2024_01.xlsx
  → 100行のデータ

処理中: sales_2024_02.xlsx
  → 100行のデータ

処理中: sales_2024_03.xlsx
  → 100行のデータ

統合完了: 合計 300行

集計処理中...

→ 保存完了: output/統合結果_20240115_143052.xlsx

============================================================
処理結果サマリー
============================================================

処理ファイル数: 3
統合後データ行数: 300
売上合計: ¥8,203,701

出力ファイル: output/統合結果_20240115_143052.xlsx
→ ダウンロードが開始されました
```

### コード解説

```python
def batch_process_excel_files(file_pattern, output_folder='output'):
```
- 関数として定義することで、再利用可能に
- `output_folder='output'` はデフォルト引数（指定しなければ 'output' が使われる）

```python
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
```
- フォルダが存在しなければ作成
- `os.makedirs()` は親フォルダも含めて作成できる

```python
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
```
- 現在時刻をファイル名に使う
- `%Y%m%d_%H%M%S` → `20240115_143052` のような形式

---

## GASとの対比

### GASで同じことをやろうとすると...

```javascript
// GAS: Googleドライブのファイルを一括処理（長くて複雑）
function processMultipleFiles() {
  const folderId = '1abc...';  // フォルダID（手動で取得が必要）
  const folder = DriveApp.getFolderById(folderId);
  const files = folder.getFilesByType(MimeType.MICROSOFT_EXCEL);

  const allData = [];

  while (files.hasNext()) {
    const file = files.next();
    const blob = file.getBlob();

    // ExcelファイルをGoogleスプレッドシートに変換（遅い！）
    const tempSS = Drive.Files.insert({
      title: 'temp_' + file.getName(),
      mimeType: MimeType.GOOGLE_SHEETS
    }, blob);

    const ss = SpreadsheetApp.openById(tempSS.id);
    const sheet = ss.getSheets()[0];
    const data = sheet.getDataRange().getValues();

    // データを追加
    for (let i = 1; i < data.length; i++) {  // 遅い！
      allData.push(data[i]);
    }

    // 一時ファイルを削除
    Drive.Files.remove(tempSS.id);
  }

  // 結果を出力...（さらにコードが続く）
}
```

**GASの問題点：**
- Excelを直接読めない（Googleスプレッドシートに変換が必要）
- ファイル数が多いと6分制限に引っかかる
- 変換処理が遅い
- コードが複雑

### Pythonなら...

```python
# Python: シンプルで高速
import pandas as pd
import glob

files = glob.glob('*.xlsx')
combined = pd.concat([pd.read_excel(f) for f in files])
combined.to_excel('result.xlsx')
```

**たった3行**で完了。

---

## GASとの対比まとめ

```
┌────────────────────────────────────────────────────────────┐
│           複数ファイル処理: GAS vs Python                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  【ファイル検出】                                          │
│    GAS    : DriveApp.getFiles() でフォルダID指定          │
│    Python : glob.glob('*.xlsx') でパターンマッチ          │
│                                                            │
│  【Excel読み込み】                                         │
│    GAS    : スプレッドシートに変換が必要（遅い）          │
│    Python : pd.read_excel() で直接読み込み（高速）        │
│                                                            │
│  【統合処理】                                              │
│    GAS    : ループで配列に追加（遅い）                    │
│    Python : pd.concat() で一発結合（高速）                │
│                                                            │
│  【10ファイル処理】                                        │
│    GAS    : 数分〜タイムアウト                            │
│    Python : 数秒                                           │
│                                                            │
│  【コード量】                                              │
│    GAS    : 30〜50行                                       │
│    Python : 3〜10行                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## エラーと対処法

### よくあるエラー

**エラー1: ファイルが見つからない**
```
FileNotFoundError: [Errno 2] No such file or directory
```
**対処法:**
```python
import os
print(os.getcwd())  # 現在のディレクトリを確認
print(os.listdir('.'))  # ファイル一覧を確認
```

**エラー2: 列名が一致しない**
```
ValueError: columns do not match
```
**原因:** 統合しようとしたファイルの列構成が異なる
**対処法:**
```python
# 共通の列だけで統合
common_cols = ['日付', '部署', '金額']  # 共通列を指定
combined = pd.concat([pd.read_excel(f)[common_cols] for f in files])
```

**エラー3: 文字化け**
```
UnicodeDecodeError または 文字化け表示
```
**対処法:**
```python
# エンコーディングを指定
df = pd.read_excel(filepath, engine='openpyxl')
# CSVの場合
df = pd.read_csv(filepath, encoding='shift-jis')  # または 'cp932'
```

---

## この節のまとめ

- `glob.glob()` でパターンマッチングによるファイル検索ができる
- `pd.concat()` で複数のDataFrameを縦に結合できる
- 各ファイルにループ処理で同じ操作を適用できる
- GASと比べて圧倒的にシンプルで高速

**次の節では、「AIプロンプトテンプレート」を学びます。ここまで学んだExcel処理を、AIの力を借りてさらに効率化する方法です。**
