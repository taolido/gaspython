#!/usr/bin/env python3
"""
サンプルCSVデータ生成スクリプト（標準ライブラリのみ）
"""

import csv
import random
import os
from datetime import datetime, timedelta

# 乱数シードを固定
random.seed(42)

# 出力ディレクトリ
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 50)
print("  サンプルCSVデータ生成")
print("=" * 50)
print()

# マスターデータ
departments = ['営業部', '開発部', '総務部', 'マーケティング部']
products = ['商品A', '商品B', '商品C', '商品D', '商品E']
sales_reps = ['田中太郎', '鈴木花子', '佐藤一郎', '高橋美咲', '伊藤健太', '渡辺直美']
prices = [5000, 10000, 15000, 20000, 30000, 50000]

# ===== 1. 売上データ（3ヶ月分） =====
print("1. 売上データを作成中...")

for month in [1, 2, 3]:
    n_rows = random.randint(150, 250)
    year = 2024
    days_in_month = 31 if month in [1, 3] else 29  # 2024年2月は29日

    rows = []
    for _ in range(n_rows):
        day = random.randint(1, days_in_month)
        date = f"{year}/{month:02d}/{day:02d}"
        dept = random.choices(departments, weights=[0.4, 0.3, 0.15, 0.15])[0]
        rep = random.choice(sales_reps)
        product = random.choice(products)
        qty = random.randint(1, 25)
        price = random.choice(prices)
        amount = qty * price
        rows.append([date, dept, rep, product, qty, price, amount])

    # 日付でソート
    rows.sort(key=lambda x: x[0])

    filename = f'{OUTPUT_DIR}/sales_data_2024{month:02d}.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['日付', '部署', '担当者', '商品', '数量', '単価', '金額'])
        writer.writerows(rows)

    print(f"   作成: sales_data_2024{month:02d}.csv ({n_rows}行)")

# ===== 2. 社員名簿 =====
print("\n2. 社員名簿を作成中...")

employees = [
    ['E001', '田中太郎', '営業部', '部長', '2015/04/01', 'tanaka@example.com'],
    ['E002', '鈴木花子', '営業部', '課長', '2017/04/01', 'suzuki@example.com'],
    ['E003', '佐藤一郎', '営業部', '主任', '2019/04/01', 'sato@example.com'],
    ['E004', '高橋美咲', '営業部', '一般', '2021/04/01', 'takahashi@example.com'],
    ['E005', '伊藤健太', '開発部', '部長', '2014/04/01', 'ito@example.com'],
    ['E006', '渡辺直美', '開発部', '課長', '2016/04/01', 'watanabe@example.com'],
    ['E007', '山本大輔', '開発部', '主任', '2018/04/01', 'yamamoto@example.com'],
    ['E008', '中村由美', '開発部', '一般', '2020/04/01', 'nakamura@example.com'],
    ['E009', '小林誠', '開発部', '一般', '2022/04/01', 'kobayashi@example.com'],
    ['E010', '加藤明日香', '総務部', '部長', '2013/04/01', 'kato@example.com'],
    ['E011', '吉田浩二', '総務部', '課長', '2016/04/01', 'yoshida@example.com'],
    ['E012', '山田恵子', '総務部', '一般', '2019/04/01', 'yamada@example.com'],
    ['E013', '松本健', 'マーケティング部', '部長', '2015/04/01', 'matsumoto@example.com'],
    ['E014', '井上舞', 'マーケティング部', '主任', '2018/04/01', 'inoue@example.com'],
    ['E015', '木村拓也', 'マーケティング部', '一般', '2021/04/01', 'kimura@example.com'],
]

filename = f'{OUTPUT_DIR}/employee_list.csv'
with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['社員ID', '氏名', '部署', '役職', '入社日', 'メール'])
    writer.writerows(employees)

print(f"   作成: employee_list.csv ({len(employees)}行)")

# ===== 3. 商品マスター =====
print("\n3. 商品マスターを作成中...")

products_data = [
    ['P001', '商品A', 'カテゴリ1', 5000, 100, '主力商品'],
    ['P002', '商品B', 'カテゴリ1', 10000, 80, '高価格帯'],
    ['P003', '商品C', 'カテゴリ2', 15000, 50, 'プレミアム'],
    ['P004', '商品D', 'カテゴリ2', 20000, 30, '限定品'],
    ['P005', '商品E', 'カテゴリ3', 30000, 20, '最上位'],
    ['P006', '商品F', 'カテゴリ1', 3000, 150, 'エントリー'],
    ['P007', '商品G', 'カテゴリ3', 50000, 10, '法人向け'],
]

filename = f'{OUTPUT_DIR}/product_master.csv'
with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['商品ID', '商品名', 'カテゴリ', '単価', '在庫数', '備考'])
    writer.writerows(products_data)

print(f"   作成: product_master.csv ({len(products_data)}行)")

# ===== 4. 統合練習用サンプル =====
print("\n4. 統合練習用サンプル（10ファイル）を作成中...")

merge_dir = f'{OUTPUT_DIR}/merge_sample'
os.makedirs(merge_dir, exist_ok=True)

for i in range(10):
    year = 2023
    month = i + 1
    n_rows = random.randint(30, 80)

    days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else (28 if month == 2 else 30)

    rows = []
    for _ in range(n_rows):
        day = random.randint(1, days_in_month)
        date = f"{year}/{month:02d}/{day:02d}"
        dept = random.choice(departments)
        product = random.choice(products)
        amount = random.randint(10000, 100000)
        rows.append([date, dept, product, amount])

    rows.sort(key=lambda x: x[0])

    filename = f'{merge_dir}/sales_{year}{month:02d}.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['日付', '部署', '商品', '金額'])
        writer.writerows(rows)

print(f"   作成: merge_sample/ (10ファイル)")

# ===== 完了 =====
print()
print("=" * 50)
print("✅ サンプルCSVデータ生成完了！")
print("=" * 50)
print()
print("Excelで使う場合:")
print("  CSVファイルをExcelで開き、.xlsx形式で保存してください")
print()
print("または、講座内のPythonコードでCSVを読み込めます:")
print("  df = pd.read_csv('sales_data_202401.csv')")
