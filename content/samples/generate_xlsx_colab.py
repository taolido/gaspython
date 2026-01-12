"""
サンプルExcelデータ生成スクリプト（Google Colab用）

【使い方】
1. Google Colabで新しいノートブックを開く
2. このコードをセルにコピペして実行
3. 生成されたxlsxファイルがダウンロードされる

※ Colabにはpandas, openpyxlがプリインストールされています
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Colabかどうかを判定
try:
    from google.colab import files
    IN_COLAB = True
    print("Google Colab環境を検出しました")
except ImportError:
    IN_COLAB = False
    print("ローカル環境で実行中（ダウンロードは自動で行われません）")

# 乱数シードを固定
np.random.seed(42)

print()
print("=" * 50)
print("  サンプルExcelデータ生成")
print("=" * 50)
print()

# マスターデータ
departments = ['営業部', '開発部', '総務部', 'マーケティング部']
products = ['商品A', '商品B', '商品C', '商品D', '商品E']
sales_reps = ['田中太郎', '鈴木花子', '佐藤一郎', '高橋美咲', '伊藤健太', '渡辺直美']

generated_files = []

# ===== 1. 売上データ（3ヶ月分） =====
print("1. 売上データを作成中...")

for month in [1, 2, 3]:
    n_rows = np.random.randint(150, 250)
    year = 2024
    days_in_month = 31 if month in [1, 3] else 29

    dates = [datetime(year, month, np.random.randint(1, days_in_month + 1)) for _ in range(n_rows)]

    data = {
        '日付': dates,
        '部署': np.random.choice(departments, n_rows, p=[0.4, 0.3, 0.15, 0.15]),
        '担当者': np.random.choice(sales_reps, n_rows),
        '商品': np.random.choice(products, n_rows),
        '数量': np.random.randint(1, 25, n_rows),
        '単価': np.random.choice([5000, 10000, 15000, 20000, 30000, 50000], n_rows)
    }

    df = pd.DataFrame(data)
    df['金額'] = df['数量'] * df['単価']
    df = df.sort_values('日付').reset_index(drop=True)

    filename = f'sales_data_2024{month:02d}.xlsx'
    df.to_excel(filename, index=False)
    generated_files.append(filename)
    print(f"   作成: {filename} ({len(df)}行)")

# ===== 2. 社員名簿 =====
print("\n2. 社員名簿を作成中...")

employees = [
    ('E001', '田中太郎', '営業部', '部長', '2015-04-01', 'tanaka@example.com'),
    ('E002', '鈴木花子', '営業部', '課長', '2017-04-01', 'suzuki@example.com'),
    ('E003', '佐藤一郎', '営業部', '主任', '2019-04-01', 'sato@example.com'),
    ('E004', '高橋美咲', '営業部', '一般', '2021-04-01', 'takahashi@example.com'),
    ('E005', '伊藤健太', '開発部', '部長', '2014-04-01', 'ito@example.com'),
    ('E006', '渡辺直美', '開発部', '課長', '2016-04-01', 'watanabe@example.com'),
    ('E007', '山本大輔', '開発部', '主任', '2018-04-01', 'yamamoto@example.com'),
    ('E008', '中村由美', '開発部', '一般', '2020-04-01', 'nakamura@example.com'),
    ('E009', '小林誠', '開発部', '一般', '2022-04-01', 'kobayashi@example.com'),
    ('E010', '加藤明日香', '総務部', '部長', '2013-04-01', 'kato@example.com'),
    ('E011', '吉田浩二', '総務部', '課長', '2016-04-01', 'yoshida@example.com'),
    ('E012', '山田恵子', '総務部', '一般', '2019-04-01', 'yamada@example.com'),
    ('E013', '松本健', 'マーケティング部', '部長', '2015-04-01', 'matsumoto@example.com'),
    ('E014', '井上舞', 'マーケティング部', '主任', '2018-04-01', 'inoue@example.com'),
    ('E015', '木村拓也', 'マーケティング部', '一般', '2021-04-01', 'kimura@example.com'),
]

df_employees = pd.DataFrame(employees, columns=['社員ID', '氏名', '部署', '役職', '入社日', 'メール'])
filename = 'employee_list.xlsx'
df_employees.to_excel(filename, index=False)
generated_files.append(filename)
print(f"   作成: {filename} ({len(df_employees)}行)")

# ===== 3. 商品マスター =====
print("\n3. 商品マスターを作成中...")

products_data = [
    ('P001', '商品A', 'カテゴリ1', 5000, 100, '主力商品'),
    ('P002', '商品B', 'カテゴリ1', 10000, 80, '高価格帯'),
    ('P003', '商品C', 'カテゴリ2', 15000, 50, 'プレミアム'),
    ('P004', '商品D', 'カテゴリ2', 20000, 30, '限定品'),
    ('P005', '商品E', 'カテゴリ3', 30000, 20, '最上位'),
    ('P006', '商品F', 'カテゴリ1', 3000, 150, 'エントリー'),
    ('P007', '商品G', 'カテゴリ3', 50000, 10, '法人向け'),
]

df_products = pd.DataFrame(products_data, columns=['商品ID', '商品名', 'カテゴリ', '単価', '在庫数', '備考'])
filename = 'product_master.xlsx'
df_products.to_excel(filename, index=False)
generated_files.append(filename)
print(f"   作成: {filename} ({len(df_products)}行)")

# ===== 4. 統合練習用サンプル（10ファイル） =====
print("\n4. 統合練習用サンプル（10ファイル）を作成中...")

os.makedirs('merge_sample', exist_ok=True)

for i in range(10):
    year = 2023
    month = i + 1
    n_rows = np.random.randint(30, 80)

    days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else (28 if month == 2 else 30)
    dates = [datetime(year, month, np.random.randint(1, days_in_month + 1)) for _ in range(n_rows)]

    data = {
        '日付': dates,
        '部署': np.random.choice(departments, n_rows),
        '商品': np.random.choice(products, n_rows),
        '金額': np.random.randint(10000, 100000, n_rows)
    }

    df = pd.DataFrame(data)
    df = df.sort_values('日付').reset_index(drop=True)

    filename = f'merge_sample/sales_{year}{month:02d}.xlsx'
    df.to_excel(filename, index=False)
    generated_files.append(filename)

print(f"   作成: merge_sample/ (10ファイル)")

# ===== 完了・ダウンロード =====
print()
print("=" * 50)
print("✅ サンプルExcelデータ生成完了！")
print("=" * 50)
print()

# Colabならダウンロード
if IN_COLAB:
    print("ファイルをダウンロード中...")
    print()

    # ZIPにまとめてダウンロード
    import shutil
    shutil.make_archive('sample_data', 'zip', '.', 'merge_sample')

    for f in generated_files:
        if not f.startswith('merge_sample/'):
            files.download(f)

    files.download('sample_data.zip')
    print()
    print("ダウンロード完了！")
    print("※ merge_sample/ は sample_data.zip に含まれています")
else:
    print("生成されたファイル:")
    for f in generated_files:
        print(f"  - {f}")
