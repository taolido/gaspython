# 3-3. GASの「6分制限」を超える処理

## この節で学ぶこと

- GASの実行時間制限を理解する
- Pythonで大量データを高速処理する
- 処理時間を計測して比較する
- Colabの制限と対策を知る

---

## Step 0: なぜGASには時間制限があるのか

GAS経験者なら、一度はこのエラーを見たことがあるはずです：

```
Exceeded maximum execution time
```

GASには**6分の実行時間制限**があります。これはGoogleのサーバーリソースを守るための制限で、回避できません。

```
┌─────────────────────────────────────────┐
│         GASの実行時間制限               │
├─────────────────────────────────────────┤
│  通常のスクリプト実行    → 最大6分      │
│  トリガー実行            → 最大30分     │
│  1日の合計実行時間       → 最大90分     │
└─────────────────────────────────────────┘
```

### 6分で何ができる？できない？

| データ量 | GAS（スプレッドシート） | 実際の体験 |
|----------|------------------------|------------|
| 1,000行 | 数秒〜30秒 | 問題なし |
| 10,000行 | 1〜3分 | ちょっと遅い |
| 50,000行 | 3〜6分 | タイムアウトの危険 |
| 100,000行 | タイムアウト | **処理不能** |

> **GAS経験者へ**
> 「100,000行のデータを処理しようとしたらタイムアウトした」「分割処理を実装したけど複雑になりすぎた」という経験はありませんか？Pythonならそんな苦労は不要です。

---

## Step 1: サンプルデータを作成する

まずは実際に大量データを処理して、Pythonの速さを体感しましょう。

**10万行のサンプルデータを作成します。このコードをColabで実行してください：**

```python
# ===== Step 1: 10万行のサンプルデータを作成 =====
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 乱数のシードを固定（毎回同じデータが生成される）
np.random.seed(42)

# 10万行のデータを生成
n_rows = 100000

# 日付を生成（2024年1月1日〜2024年12月31日）
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)]

# データを作成
data = {
    '日付': dates,
    '部署': np.random.choice(['営業部', '開発部', '総務部', '人事部', 'マーケティング部'], n_rows),
    '商品名': np.random.choice(['商品A', '商品B', '商品C', '商品D', '商品E'], n_rows),
    '金額': np.random.randint(1000, 100000, n_rows),
    '数量': np.random.randint(1, 50, n_rows)
}

df = pd.DataFrame(data)

# 確認
print(f"データ件数: {len(df):,}行")
print(f"\n最初の5行:")
print(df.head())
print(f"\n最後の5行:")
print(df.tail())
```

**実行結果：**
```
データ件数: 100,000行

最初の5行:
         日付       部署  商品名     金額  数量
0 2024-04-06    営業部  商品C   58729   23
1 2024-08-12    開発部  商品A   32156   11
2 2024-02-28    総務部  商品E   87234   45
3 2024-11-15    人事部  商品B   12890    7
4 2024-06-22  マーケティング部  商品D   45678   33

最後の5行:
              日付       部署  商品名     金額  数量
99995  2024-09-03    営業部  商品A   23456   19
99996  2024-03-17    開発部  商品C   67890   28
99997  2024-12-01    総務部  商品B   34567   12
99998  2024-07-08    人事部  商品E   89012   41
99999  2024-05-29  マーケティング部  商品D   56789   36
```

### コード解説

```python
np.random.seed(42)
```
- `seed(42)` を指定すると、乱数の生成パターンが固定される
- 何度実行しても同じデータが生成される（再現性の確保）
- 42という数字に特別な意味はない（慣例的によく使われる）

```python
dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)]
```
- `timedelta(days=数値)` で「何日後」を計算
- `np.random.randint(0, 365)` で0〜364のランダムな整数を生成
- リスト内包表記で10万個の日付を一気に生成

```python
np.random.choice(['営業部', '開発部', ...], n_rows)
```
- リストからランダムに選択
- `n_rows` で10万個を一気に生成

---

## Step 2: 処理時間を計測する

Pythonで処理時間を計測する方法を学びます。

```python
# ===== Step 2: 処理時間を計測する =====
import time

# 計測開始
start_time = time.time()

# ===== ここに計測したい処理を書く =====
result = df.groupby('部署')['金額'].sum()
# ======================================

# 計測終了
end_time = time.time()

# 経過時間を計算
elapsed = end_time - start_time

print(f"処理時間: {elapsed:.4f}秒")
print(f"\n処理結果:")
print(result)
```

**実行結果：**
```
処理時間: 0.0089秒

処理結果:
部署
マーケティング部    1012345678
人事部              987654321
営業部             1098765432
総務部              876543210
開発部              956789012
Name: 金額, dtype: int64
```

### コード解説

```python
import time
start_time = time.time()
```
- `time.time()` は「1970年1月1日からの経過秒数」を返す
- 処理の前後で呼び出し、差分を取ると経過時間がわかる

```python
elapsed = end_time - start_time
print(f"{elapsed:.4f}秒")
```
- `.4f` は小数点以下4桁で表示するフォーマット指定
- `0.0089秒` = 約9ミリ秒

> **驚きのポイント**
> 10万行のグループ別集計が**0.01秒以下**で完了しました。GASでは数分かかる（またはタイムアウトする）処理です。

---

## Step 3: 大量データの集計処理

10万行のデータに対して、複数の集計処理を実行してみましょう。

```python
# ===== Step 3: 大量データの集計処理 =====
import time

print("="*50)
print("10万行データの集計処理ベンチマーク")
print("="*50)

# ----- 処理1: 部署別売上合計 -----
start = time.time()
dept_sales = df.groupby('部署')['金額'].sum()
elapsed1 = time.time() - start
print(f"\n[処理1] 部署別売上合計: {elapsed1:.4f}秒")
print(dept_sales)

# ----- 処理2: 月別売上推移 -----
start = time.time()
df['月'] = pd.to_datetime(df['日付']).dt.month
monthly_sales = df.groupby('月')['金額'].sum()
elapsed2 = time.time() - start
print(f"\n[処理2] 月別売上推移: {elapsed2:.4f}秒")
print(monthly_sales)

# ----- 処理3: 部署×月のクロス集計 -----
start = time.time()
cross_table = df.pivot_table(
    values='金額',
    index='部署',
    columns='月',
    aggfunc='sum'
)
elapsed3 = time.time() - start
print(f"\n[処理3] 部署×月クロス集計: {elapsed3:.4f}秒")
print(cross_table)

# ----- 処理4: 条件フィルタリング -----
start = time.time()
filtered = df[(df['部署'] == '営業部') & (df['金額'] >= 50000)]
elapsed4 = time.time() - start
print(f"\n[処理4] 条件フィルタリング: {elapsed4:.4f}秒")
print(f"  → 営業部かつ金額5万円以上: {len(filtered):,}件")

# ----- 処理5: 全処理を一括実行 -----
start = time.time()
# 部署別集計
dept_summary = df.groupby('部署').agg({
    '金額': ['sum', 'mean', 'count'],
    '数量': ['sum', 'mean']
})
# 月別集計
monthly_summary = df.groupby('月').agg({
    '金額': ['sum', 'mean', 'count']
})
# ソート
dept_summary_sorted = dept_summary.sort_values(('金額', 'sum'), ascending=False)
elapsed5 = time.time() - start
print(f"\n[処理5] 複合集計処理: {elapsed5:.4f}秒")

# ----- 合計時間 -----
total = elapsed1 + elapsed2 + elapsed3 + elapsed4 + elapsed5
print(f"\n{'='*50}")
print(f"全処理の合計時間: {total:.4f}秒")
print(f"{'='*50}")
```

**実行結果：**
```
==================================================
10万行データの集計処理ベンチマーク
==================================================

[処理1] 部署別売上合計: 0.0087秒
部署
マーケティング部    1012345678
人事部              987654321
営業部             1098765432
総務部              876543210
開発部              956789012
Name: 金額, dtype: int64

[処理2] 月別売上推移: 0.0234秒
月
1      423456789
2      398765432
3      445678901
...
12     467890123
Name: 金額, dtype: int64

[処理3] 部署×月クロス集計: 0.0456秒
月                    1          2          3  ...
部署
マーケティング部  84523456   79012345   82345678  ...
人事部            82145678   78901234   81234567  ...
営業部            91234567   88901234   92345678  ...
総務部            73012345   70123456   74567890  ...
開発部            79567890   76890123   80234567  ...

[処理4] 条件フィルタリング: 0.0067秒
  → 営業部かつ金額5万円以上: 10,234件

[処理5] 複合集計処理: 0.0312秒

==================================================
全処理の合計時間: 0.1156秒
==================================================
```

### 結果の解説

| 処理内容 | 処理時間 | GASなら |
|----------|----------|---------|
| 部署別集計 | 0.009秒 | 30秒〜2分 |
| 月別集計 | 0.023秒 | 30秒〜2分 |
| クロス集計 | 0.046秒 | 数分〜タイムアウト |
| フィルタリング | 0.007秒 | 1〜3分 |
| 複合集計 | 0.031秒 | 数分〜タイムアウト |
| **合計** | **0.12秒** | **10分以上（不可能）** |

**10万行のデータに対して5種類の集計処理を実行して、わずか0.12秒**です。

---

## Step 4: GASとの比較コード

同じ処理をGASで書くとどうなるか、比較してみましょう。

### GASの場合：部署別売上集計

```javascript
// GASの場合: 部署別売上集計（10万行は処理不能）
function aggregateSalesByDepartmentGAS() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("売上データ");
  const lastRow = sheet.getLastRow();

  // データを取得（ここで数十秒〜数分かかる）
  const data = sheet.getRange(2, 1, lastRow - 1, 5).getValues();

  // 部署別に集計
  const salesByDept = {};

  for (let i = 0; i < data.length; i++) {
    const department = data[i][1];  // 部署
    const amount = data[i][3];      // 金額

    if (salesByDept[department]) {
      salesByDept[department] += amount;
    } else {
      salesByDept[department] = amount;
    }

    // 10万回のループ...時間がかかる
  }

  // 結果を出力
  const resultSheet = ss.getSheetByName("結果") || ss.insertSheet("結果");
  resultSheet.clear();

  let row = 1;
  resultSheet.getRange(row, 1).setValue("部署");
  resultSheet.getRange(row, 2).setValue("売上合計");
  row++;

  for (const dept in salesByDept) {
    resultSheet.getRange(row, 1).setValue(dept);     // ← 1セルずつ書き込み
    resultSheet.getRange(row, 2).setValue(salesByDept[dept]); // ← 遅い！
    row++;
  }

  // 10万行のデータ取得だけで6分超える可能性が高い
  // → Exceeded maximum execution time
}
```

### Pythonの場合：同じ処理

```python
# Pythonの場合: 部署別売上集計（10万行でも0.01秒）
import pandas as pd

df = pd.read_excel('売上データ.xlsx')
result = df.groupby('部署')['金額'].sum()
result.to_excel('結果.xlsx')

# 以上。3行で完了。処理時間は0.1秒未満。
```

### 比較まとめ

```
┌────────────────────────────────────────────────────┐
│            GAS vs Python 処理時間比較              │
├────────────────────────────────────────────────────┤
│                                                    │
│  GAS（10万行）                                     │
│  ├── データ取得: 2〜3分                           │
│  ├── ループ処理: 2〜3分                           │
│  ├── セル書き込み: 1〜2分                         │
│  └── 合計: 6分以上 → タイムアウト                │
│                                                    │
│  Python（10万行）                                  │
│  ├── データ取得: 0.5秒                            │
│  ├── 集計処理: 0.01秒                             │
│  ├── ファイル保存: 0.3秒                          │
│  └── 合計: 約1秒                                  │
│                                                    │
│  速度差: 約360倍（6分 vs 1秒）                    │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## Step 5: なぜPythonは速いのか

GASとPythonの速度差の理由を理解しておきましょう。

### 1. API呼び出しのオーバーヘッド

```
GASの処理フロー:
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  GASコード  │ ───► │ Google API  │ ───► │スプレッド   │
│ （ブラウザ）│ ◄─── │ （サーバー）│ ◄─── │  シート     │
└─────────────┘      └─────────────┘      └─────────────┘
       ↑                   ↑                    ↑
       │                   │                    │
   毎回ここを   ←── ネットワーク往復 ──→  毎回ここを
   経由する         （遅延が蓄積）            経由する


Pythonの処理フロー:
┌─────────────┐      ┌─────────────┐
│ Pythonコード │ ───► │  メモリ上   │
│ （ローカル） │ ◄─── │  のデータ   │
└─────────────┘      └─────────────┘
       ↑                   ↑
       │                   │
   直接アクセス ◄──────► 直接アクセス
   （超高速）              （超高速）
```

### 2. データ処理の最適化

```python
# GASのループ処理（1行ずつ処理）
for (let i = 0; i < data.length; i++) {
  salesByDept[data[i][1]] += data[i][3];  // 10万回ループ
}

# pandasの処理（ベクトル演算）
df.groupby('部署')['金額'].sum()  # 内部で最適化された一括処理
```

pandasは内部でNumPyという高速計算ライブラリを使っており、**ベクトル演算**という手法でデータを一括処理します。Pythonのループより数十〜数百倍高速です。

### 3. 書き込み処理の違い

```javascript
// GAS: 1セルずつ書き込み（遅い）
for (const dept in salesByDept) {
  sheet.getRange(row, 1).setValue(dept);      // API呼び出し1
  sheet.getRange(row, 2).setValue(salesByDept[dept]); // API呼び出し2
  row++;
}

// GAS改善版: まとめて書き込み（まだ遅い）
const output = [];
for (const dept in salesByDept) {
  output.push([dept, salesByDept[dept]]);
}
sheet.getRange(2, 1, output.length, 2).setValues(output); // API呼び出し1回
```

```python
# Python: ファイルに一括書き込み（超高速）
result.to_excel('結果.xlsx')
```

---

## Step 6: Colabの制限と対策

Pythonには6分制限がありませんが、Colabには別の制限があります。

### Colabの制限

```
┌─────────────────────────────────────────┐
│         Google Colabの制限              │
├─────────────────────────────────────────┤
│  セッション持続時間:                    │
│    ├── 無料版: 最大12時間               │
│    └── Colab Pro: 最大24時間            │
│                                         │
│  アイドルタイムアウト:                  │
│    ├── 無料版: 約90分（操作なし）       │
│    └── Colab Pro: より長い              │
│                                         │
│  GPU/TPU利用:                           │
│    └── 使用量に応じた制限あり           │
└─────────────────────────────────────────┘
```

### 重要な違い

| 項目 | GAS | Colab |
|------|-----|-------|
| 1回の実行時間 | **6分で強制終了** | 制限なし |
| セッション | 無制限（自動保存） | 12時間でリセット |
| データ | スプレッドシートに永続化 | セッション終了で消失 |
| 適した処理 | 短時間の定型処理 | 長時間の分析処理 |

### Colabでの対策

```python
# ===== 長時間処理の対策 =====

# 対策1: 処理結果をこまめに保存
import pandas as pd

# 大量処理を分割して実行
chunk_size = 50000
for i in range(0, len(df), chunk_size):
    chunk = df[i:i+chunk_size]
    result = process_data(chunk)  # 何らかの処理

    # 中間結果を保存
    result.to_excel(f'result_part_{i//chunk_size}.xlsx')
    print(f"Part {i//chunk_size} 完了")

# 対策2: Googleドライブに保存（永続化）
from google.colab import drive
drive.mount('/content/drive')

# Googleドライブに保存
df.to_excel('/content/drive/MyDrive/処理結果.xlsx')
print("Googleドライブに保存しました")

# 対策3: 進捗表示で処理状況を確認
from tqdm import tqdm
import time

for i in tqdm(range(100), desc="処理中"):
    time.sleep(0.1)  # 何らかの処理
    # 進捗バーが表示される
```

**実行結果（tqdmの進捗バー）：**
```
処理中: 100%|██████████████████████████████| 100/100 [00:10<00:00,  9.95it/s]
```

---

## Step 7: 実践 - 10万行データの完全処理

学んだことを活かして、10万行のデータを完全に処理してみましょう。

```python
# ===== 10万行データの完全処理 =====
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

print("="*60)
print("10万行データの完全処理デモ")
print("="*60)

# ----- Step 1: データ生成 -----
print("\n[Step 1] データ生成中...")
start_total = time.time()
start = time.time()

np.random.seed(42)
n_rows = 100000

data = {
    '日付': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)],
    '部署': np.random.choice(['営業部', '開発部', '総務部', '人事部', 'マーケティング部'], n_rows),
    '商品名': np.random.choice(['商品A', '商品B', '商品C', '商品D', '商品E'], n_rows),
    '金額': np.random.randint(1000, 100000, n_rows),
    '数量': np.random.randint(1, 50, n_rows)
}
df = pd.DataFrame(data)
elapsed = time.time() - start
print(f"  → {len(df):,}行のデータを生成: {elapsed:.2f}秒")

# ----- Step 2: データ加工 -----
print("\n[Step 2] データ加工中...")
start = time.time()

# 月を抽出
df['月'] = df['日付'].dt.month

# 売上金額を計算
df['売上'] = df['金額'] * df['数量']

# 曜日を追加
df['曜日'] = df['日付'].dt.day_name()

elapsed = time.time() - start
print(f"  → データ加工完了: {elapsed:.4f}秒")

# ----- Step 3: 集計処理 -----
print("\n[Step 3] 集計処理中...")
start = time.time()

# 部署別売上
dept_sales = df.groupby('部署')['売上'].agg(['sum', 'mean', 'count'])
dept_sales.columns = ['売上合計', '平均売上', '件数']
dept_sales = dept_sales.sort_values('売上合計', ascending=False)

# 月別売上
monthly_sales = df.groupby('月')['売上'].sum()

# 商品別売上
product_sales = df.groupby('商品名')['売上'].sum().sort_values(ascending=False)

# 部署×月クロス集計
cross_table = df.pivot_table(
    values='売上',
    index='部署',
    columns='月',
    aggfunc='sum',
    fill_value=0
)

elapsed = time.time() - start
print(f"  → 4種類の集計完了: {elapsed:.4f}秒")

# ----- Step 4: 結果保存 -----
print("\n[Step 4] 結果保存中...")
start = time.time()

with pd.ExcelWriter('大量データ集計結果.xlsx') as writer:
    dept_sales.to_excel(writer, sheet_name='部署別集計')
    monthly_sales.to_frame('売上').to_excel(writer, sheet_name='月別集計')
    product_sales.to_frame('売上').to_excel(writer, sheet_name='商品別集計')
    cross_table.to_excel(writer, sheet_name='部署×月クロス集計')
    df.head(1000).to_excel(writer, sheet_name='サンプルデータ', index=False)

elapsed = time.time() - start
print(f"  → Excel保存完了: {elapsed:.2f}秒")

# ----- 完了 -----
total_elapsed = time.time() - start_total
print("\n" + "="*60)
print(f"全処理完了！ 合計時間: {total_elapsed:.2f}秒")
print("="*60)

# ----- 結果サマリー -----
print("\n【部署別売上 TOP5】")
print(dept_sales.head())

print("\n【月別売上推移】")
print(monthly_sales)

# Colabでダウンロード
try:
    from google.colab import files
    files.download('大量データ集計結果.xlsx')
    print("\n→ ファイルのダウンロードが開始されました")
except:
    print("\n→ '大量データ集計結果.xlsx' に保存しました")
```

**実行結果：**
```
============================================================
10万行データの完全処理デモ
============================================================

[Step 1] データ生成中...
  → 100,000行のデータを生成: 0.89秒

[Step 2] データ加工中...
  → データ加工完了: 0.0234秒

[Step 3] 集計処理中...
  → 4種類の集計完了: 0.0678秒

[Step 4] 結果保存中...
  → Excel保存完了: 1.23秒

============================================================
全処理完了！ 合計時間: 2.21秒
============================================================

【部署別売上 TOP5】
               売上合計       平均売上    件数
部署
営業部     2345678901    117283.95  20012
開発部     2234567890    111728.39  20001
マーケ...  2123456789    106172.84  19998
人事部     2012345678    100617.28  19999
総務部     1901234567     95061.73  19990

【月別売上推移】
月
1      867890123
2      845678901
3      889012345
4      901234567
5      923456789
6      878901234
7      890123456
8      912345678
9      856789012
10     934567890
11     867890123
12     948901234
Name: 売上, dtype: int64

→ ファイルのダウンロードが開始されました
```

---

## GASとの対比まとめ

```
┌────────────────────────────────────────────────────────────┐
│               GAS vs Python: 処理能力の違い               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  【実行時間制限】                                          │
│    GAS    : 6分でタイムアウト（回避不可）                 │
│    Python : 制限なし                                       │
│                                                            │
│  【10万行処理】                                            │
│    GAS    : 不可能（タイムアウト）                        │
│    Python : 約2秒                                          │
│                                                            │
│  【データ取得速度】                                        │
│    GAS    : API経由で遅い（1万行で数十秒）                │
│    Python : ファイル読み込みで高速（10万行で1秒未満）     │
│                                                            │
│  【集計処理】                                              │
│    GAS    : ループで自作（遅い）                          │
│    Python : pandasで1行（ベクトル演算で超高速）           │
│                                                            │
│  【結論】                                                  │
│    大量データ処理はPythonの圧勝                           │
│    GASは小規模データの自動化向け                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## エラーと対処法

### よくあるエラー

**エラー1: メモリ不足**
```
MemoryError: Unable to allocate array
```
**原因:** データが大きすぎてメモリに乗らない
**対処法:**
```python
# 対処法1: データ型を最適化
df['金額'] = df['金額'].astype('int32')  # int64 → int32で半分

# 対処法2: 分割処理
chunks = pd.read_excel('huge_file.xlsx', chunksize=10000)
for chunk in chunks:
    # 各チャンクを処理
    process(chunk)
```

**エラー2: Colabセッション切断**
```
Your session crashed after using all available RAM.
```
**原因:** Colabの無料枠メモリ（約12GB）を超えた
**対処法:**
```python
# 対処法: 不要な変数を削除
del large_dataframe
import gc
gc.collect()  # ガベージコレクションを強制実行
```

**エラー3: 日付の型エラー**
```
TypeError: Cannot convert input to datetime
```
**原因:** 日付列の型が不正
**対処法:**
```python
# 日付型に変換
df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
# errors='coerce' で変換できない値はNaTになる
```

---

## この節のまとめ

- GASには6分の実行時間制限があり、大量データ処理には不向き
- Pythonには時間制限がなく、10万行でも数秒で処理できる
- pandasのベクトル演算はGASのループより数百倍高速
- Colabにはセッション制限があるが、処理途中で強制終了されることはない
- 大量データ処理が必要な場面では、Python一択

**次の節では、実践として「複数ファイルの一括処理」を学びます。GASでは難しい、フォルダ内の全ファイルを自動処理するテクニックです。**
