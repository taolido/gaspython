# 3-5. 【実践】100枚のExcelを3秒で統合

## この節で学ぶこと

- 複数のExcelファイルを自動検出する
- 100ファイルを1つに統合する
- GASでは困難な「大量ファイル処理」をPythonで実現
- 実務で即使える統合ツールを作る

---

## GASの限界、Pythonの強み

### GASでこれをやろうとすると...

```javascript
// GAS: 複数Excelファイルを統合（理想のコード）
function mergeExcelFiles() {
  const folder = DriveApp.getFolderById('フォルダID');
  const files = folder.getFilesByType(MimeType.MICROSOFT_EXCEL);

  const allData = [];
  while (files.hasNext()) {
    const file = files.next();
    // ここで問題発生！
    // GASはExcelファイルを直接読めない
    // → スプレッドシートに変換が必要
    // → 変換に時間がかかる
    // → 6分のタイムアウトに引っかかる
  }
}
```

**GASの問題点:**
- Excelファイル（.xlsx）を直接読めない
- Google Driveへのアップロード → スプレッドシート変換が必要
- 変換に1ファイル数秒〜数十秒かかる
- 100ファイルなら6分のタイムアウトに確実に引っかかる

### Pythonなら3秒

```python
# Python: 100ファイルを3秒で統合
import pandas as pd
import glob

files = glob.glob('*.xlsx')
df = pd.concat([pd.read_excel(f) for f in files])
df.to_excel('統合.xlsx', index=False)
# 完了！
```

**これがGAS経験者がPythonを学ぶ理由の1つです。**

---

## Step 0: サンプルファイルを作成（100ファイル）

実際に100ファイルを作成して、統合ツールをテストします。

```python
# ===== Step 0: 100個のサンプルExcelファイルを作成 =====
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 出力フォルダ
output_dir = 'monthly_sales'
os.makedirs(output_dir, exist_ok=True)

np.random.seed(42)

# 100ファイル = 過去100ヶ月分（約8年分）を想定
departments = ['営業部', '開発部', '総務部', 'マーケ部']
products = ['商品A', '商品B', '商品C', '商品D', '商品E']

print("100ファイルを作成中...")
start_time = datetime.now()

for i in range(100):
    # 年月を計算（2016年1月〜2024年4月）
    year = 2016 + (i // 12)
    month = (i % 12) + 1

    # 各ファイル50〜150行のデータ
    n_rows = np.random.randint(50, 150)

    data = {
        '日付': [datetime(year, month, np.random.randint(1, 28)) for _ in range(n_rows)],
        '部署': np.random.choice(departments, n_rows),
        '商品': np.random.choice(products, n_rows),
        '数量': np.random.randint(1, 30, n_rows),
        '単価': np.random.choice([5000, 10000, 15000, 20000, 30000], n_rows)
    }

    df = pd.DataFrame(data)
    df['金額'] = df['数量'] * df['単価']

    filename = f'{output_dir}/sales_{year}{month:02d}.xlsx'
    df.to_excel(filename, index=False)

    # 進捗表示（10ファイルごと）
    if (i + 1) % 10 == 0:
        print(f"  {i + 1}/100 ファイル作成完了")

elapsed = (datetime.now() - start_time).total_seconds()
print(f"\n✅ 100ファイル作成完了！")
print(f"   フォルダ: {output_dir}/")
print(f"   作成時間: {elapsed:.1f}秒")

# ファイル一覧を確認
import glob
files = glob.glob(f'{output_dir}/*.xlsx')
print(f"   ファイル数: {len(files)}")
```

**実行結果：**
```
100ファイルを作成中...
  10/100 ファイル作成完了
  20/100 ファイル作成完了
  ...
  100/100 ファイル作成完了

✅ 100ファイル作成完了！
   フォルダ: monthly_sales/
   作成時間: 15.3秒
   ファイル数: 100
```

---

## Step 1: 100ファイルを3秒で統合

```python
# ===== Step 1: 100ファイルを統合（シンプル版） =====
import pandas as pd
import glob
import time

# 計測開始
start_time = time.time()

# ファイル一覧を取得
files = glob.glob('monthly_sales/*.xlsx')
print(f"処理対象: {len(files)}ファイル")

# 全ファイルを読み込んで結合
all_data = []
for f in files:
    df = pd.read_excel(f)
    all_data.append(df)

# 1つのDataFrameに統合
merged_df = pd.concat(all_data, ignore_index=True)

# 保存
merged_df.to_excel('sales_merged_all.xlsx', index=False)

# 計測終了
elapsed = time.time() - start_time

print(f"\n✅ 統合完了！")
print(f"   処理時間: {elapsed:.1f}秒")
print(f"   処理ファイル数: {len(files)}")
print(f"   合計行数: {len(merged_df):,}行")
print(f"   出力ファイル: sales_merged_all.xlsx")
```

**実行結果：**
```
処理対象: 100ファイル

✅ 統合完了！
   処理時間: 2.8秒
   処理ファイル数: 100
   合計行数: 9,847行
   出力ファイル: sales_merged_all.xlsx
```

**100ファイル、約1万行を3秒以下で統合。GASでは不可能な速度です。**

---

## Step 2: より実用的な統合ツール

実務で使える機能を追加した完成版です。

```python
# ===== Excel統合ツール（完成版） =====
# excel_merge_tool.py
#
# 機能:
# - フォルダ内のExcelファイルを自動検出
# - 1つのファイルに統合
# - ファイル名をソースとして記録
# - 処理時間を計測

import pandas as pd
import glob
import os
import time
from datetime import datetime

def merge_excel_files(input_folder, output_file=None):
    """
    フォルダ内のExcelファイルを統合する

    Parameters:
    -----------
    input_folder : str
        Excelファイルがあるフォルダパス
    output_file : str, optional
        出力ファイル名（省略時は自動生成）

    Returns:
    --------
    dict : 処理結果の情報
    """

    start_time = time.time()

    # ファイル一覧を取得
    pattern = os.path.join(input_folder, '*.xlsx')
    files = sorted(glob.glob(pattern))

    if not files:
        return {'error': f'Excelファイルが見つかりません: {input_folder}'}

    print(f"処理対象: {len(files)}ファイル")
    print("-" * 40)

    # 全ファイルを読み込み
    all_data = []
    total_rows = 0

    for i, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)

        try:
            df = pd.read_excel(filepath)

            # ソースファイル名を追加（どのファイルから来たか分かるように）
            df['_source_file'] = filename

            all_data.append(df)
            total_rows += len(df)

            # 進捗表示（20ファイルごと、または最後）
            if i % 20 == 0 or i == len(files):
                print(f"  読み込み: {i}/{len(files)} ({filename})")

        except Exception as e:
            print(f"  ⚠️ スキップ: {filename} - {e}")

    # 統合
    merged_df = pd.concat(all_data, ignore_index=True)

    # 日付列があればソート
    if '日付' in merged_df.columns:
        merged_df = merged_df.sort_values('日付').reset_index(drop=True)

    # 出力ファイル名
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'統合データ_{timestamp}.xlsx'

    # 保存
    merged_df.to_excel(output_file, index=False)

    elapsed = time.time() - start_time

    result = {
        'output_file': output_file,
        'file_count': len(files),
        'total_rows': len(merged_df),
        'elapsed_seconds': round(elapsed, 2)
    }

    return result


# ===== メイン処理 =====
if __name__ == "__main__":
    print("=" * 50)
    print("  Excel統合ツール")
    print("  〜 100枚のExcelを3秒で統合 〜")
    print("=" * 50)
    print()

    # 統合対象のフォルダを指定
    input_folder = 'monthly_sales'  # ここを変更

    if not os.path.exists(input_folder):
        print(f"❌ フォルダが見つかりません: {input_folder}")
        print("   monthly_sales フォルダを作成してExcelファイルを配置してください")
    else:
        result = merge_excel_files(input_folder)

        if 'error' in result:
            print(f"\n❌ {result['error']}")
        else:
            print()
            print("=" * 50)
            print("✅ 統合完了！")
            print("=" * 50)
            print(f"   出力ファイル: {result['output_file']}")
            print(f"   処理ファイル数: {result['file_count']}")
            print(f"   合計行数: {result['total_rows']:,}行")
            print(f"   処理時間: {result['elapsed_seconds']}秒")
            print()

            # GASとの比較コメント
            if result['file_count'] >= 10:
                print("💡 GASでこの処理をすると...")
                print(f"   ・{result['file_count']}ファイルの変換だけで数分")
                print("   ・6分のタイムアウトで失敗する可能性大")
                print(f"   → Pythonなら{result['elapsed_seconds']}秒で完了！")

    print()
    input("Enterキーで終了...")
```

**実行結果：**
```
==================================================
  Excel統合ツール
  〜 100枚のExcelを3秒で統合 〜
==================================================

処理対象: 100ファイル
----------------------------------------
  読み込み: 20/100 (sales_201708.xlsx)
  読み込み: 40/100 (sales_201904.xlsx)
  読み込み: 60/100 (sales_202012.xlsx)
  読み込み: 80/100 (sales_202208.xlsx)
  読み込み: 100/100 (sales_202404.xlsx)

==================================================
✅ 統合完了！
==================================================
   出力ファイル: 統合データ_20240115_143052.xlsx
   処理ファイル数: 100
   合計行数: 9,847行
   処理時間: 2.73秒

💡 GASでこの処理をすると...
   ・100ファイルの変換だけで数分
   ・6分のタイムアウトで失敗する可能性大
   → Pythonなら2.73秒で完了！

Enterキーで終了...
```

---

## Step 3: Colab上で使う場合

Google Colabでも同じコードが動きます。

```python
# Colab用: ファイルをアップロードして統合

from google.colab import files
import pandas as pd
import glob
import os
import time

# 1. ファイルをアップロード
print("Excelファイルをアップロードしてください（複数選択可）")
uploaded = files.upload()

print(f"\nアップロード完了: {len(uploaded)}ファイル")

# 2. 統合処理
start_time = time.time()

all_data = []
for filename in uploaded.keys():
    if filename.endswith('.xlsx'):
        df = pd.read_excel(filename)
        df['_source'] = filename
        all_data.append(df)
        print(f"  読み込み: {filename} ({len(df)}行)")

merged_df = pd.concat(all_data, ignore_index=True)

elapsed = time.time() - start_time

# 3. 結果を保存してダウンロード
output_file = '統合データ.xlsx'
merged_df.to_excel(output_file, index=False)

print(f"\n✅ 統合完了！")
print(f"   処理時間: {elapsed:.1f}秒")
print(f"   合計行数: {len(merged_df):,}行")

# ダウンロード
files.download(output_file)
```

---

## GAS vs Python: 大量ファイル処理の比較

```
┌─────────────────────────────────────────────────────────────┐
│  100ファイル統合の比較                                       │
├─────────────────────┬───────────────────┬───────────────────┤
│  項目                │  GAS              │  Python           │
├─────────────────────┼───────────────────┼───────────────────┤
│  Excelファイル読込  │  変換必要         │  直接読込         │
│  処理時間（推定）   │  タイムアウト     │  約3秒            │
│  タイムアウト       │  6分で強制終了    │  なし             │
│  大量ファイル       │  困難             │  得意             │
│  メモリ             │  制限あり         │  PC依存           │
│  コード量           │  複雑             │  シンプル         │
└─────────────────────┴───────────────────┴───────────────────┘
```

**「GASでは6分タイムアウト、Pythonなら3秒」**

これがGAS経験者がPythonを学ぶべき理由の1つです。

---

## 応用: フィルタリング付き統合

特定の条件でフィルタリングしながら統合することもできます。

```python
# 応用: 2023年のデータだけ統合
import pandas as pd
import glob

files = glob.glob('monthly_sales/sales_2023*.xlsx')  # 2023年だけ
print(f"2023年のファイル: {len(files)}件")

all_data = [pd.read_excel(f) for f in files]
df_2023 = pd.concat(all_data, ignore_index=True)

# さらに営業部だけに絞る
df_sales = df_2023[df_2023['部署'] == '営業部']

df_sales.to_excel('2023年_営業部.xlsx', index=False)
print(f"出力: 2023年_営業部.xlsx ({len(df_sales)}行)")
```

---

## この節のまとめ

- `glob.glob()` でファイル一覧を取得
- `pd.concat()` で複数DataFrameを統合
- 100ファイルでも約3秒で統合可能
- GASの6分タイムアウト問題を完全解決
- `_source_file` 列を追加すると元ファイルが分かる

**GASでは「できない」「時間がかかる」処理が、Pythonなら一瞬。**
**これがPythonを学ぶ価値です。**

**次の節では、Excel処理で困ったときのAIプロンプトテンプレートを紹介します。**
