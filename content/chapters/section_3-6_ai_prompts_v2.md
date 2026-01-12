# 3-6. AIプロンプトテンプレート（Excel操作編）

## この節で学ぶこと

- AIにExcel処理コードを生成してもらう方法
- 効果的なプロンプトの書き方
- エラーを解決してもらう方法
- コードの意味を理解するための質問法

---

## なぜAIを活用するのか

この章で学んだpandasやopenpyxlの文法は、最初はなかなか覚えられません。

でも大丈夫です。**AIに質問すれば、あなたの代わりにコードを書いてくれます。**

重要なのは：
1. **やりたいことを正確に伝える力**
2. **AIの出力を検証・修正する力**
3. **エラーが出たら質問する力**

この節では、Excel処理に特化したプロンプトテンプレートを紹介します。

---

## テンプレート1: Excel処理コードの生成

### 基本構造

```
【依頼】
PythonでExcelファイルを処理するコードを書いてください。

【入力ファイル】
- ファイル名: ○○○.xlsx
- シート名: ○○○（または「最初のシート」）
- 列構成:
  - A列: ○○○（例: 日付、形式: YYYY/MM/DD）
  - B列: ○○○（例: 部署名、文字列）
  - C列: ○○○（例: 金額、数値）
  - ...

【やりたいこと】
[具体的な処理内容を箇条書きで]

【出力】
[期待する出力形式]

【環境】
Google Colab（pandasとopenpyxlが利用可能）

【追加条件】
- コードにはコメントを入れてください
- エラー処理も含めてください
```

---

### 実践例1: 条件フィルタリング

**プロンプト:**
```
【依頼】
PythonでExcelファイルを処理するコードを書いてください。

【入力ファイル】
- ファイル名: 売上データ.xlsx
- 列構成:
  - A列: 日付（YYYY/MM/DD形式）
  - B列: 部署（営業部、開発部、総務部のいずれか）
  - C列: 商品名（文字列）
  - D列: 金額（数値、円単位）

【やりたいこと】
金額が50,000円以上のデータだけを抽出したい

【出力】
抽出結果を「高額売上.xlsx」という新しいファイルに保存

【環境】
Google Colab（pandasが利用可能）

【追加条件】
- 抽出前後のデータ件数を表示してください
- コードにはコメントを入れてください
```

**AIの回答例:**
```python
import pandas as pd
from google.colab import files

# ===== 1. ファイルをアップロード =====
print("売上データ.xlsxをアップロードしてください")
uploaded = files.upload()

# ===== 2. データを読み込み =====
df = pd.read_excel('売上データ.xlsx')
print(f"読み込みデータ: {len(df)}件")

# ===== 3. 金額が50,000円以上のデータを抽出 =====
df_filtered = df[df['金額'] >= 50000]
print(f"抽出後データ: {len(df_filtered)}件")
print(f"→ {len(df) - len(df_filtered)}件を除外しました")

# ===== 4. 抽出結果を確認 =====
print("\n【抽出結果プレビュー】")
print(df_filtered.head(10))

# ===== 5. 新しいファイルに保存 =====
df_filtered.to_excel('高額売上.xlsx', index=False)
print("\n'高額売上.xlsx'に保存しました")

# ===== 6. ダウンロード =====
files.download('高額売上.xlsx')
```

**このコードを使う手順:**
1. Colabに上記コードをコピペ
2. 実行すると「売上データ.xlsx」のアップロードを求められる
3. ファイルを選択してアップロード
4. 処理が実行され、結果がダウンロードされる

---

### 実践例2: 複数条件での集計

**プロンプト:**
```
【依頼】
PythonでExcelファイルを処理するコードを書いてください。

【入力ファイル】
- ファイル名: 売上データ.xlsx
- 列構成:
  - 日付（YYYY/MM/DD形式）
  - 部署（営業部、開発部、総務部）
  - 商品名
  - 金額

【やりたいこと】
以下の3種類の集計を行いたい:
1. 部署ごとの売上合計と平均と件数
2. 月ごとの売上推移
3. 部署×月のクロス集計表（ピボットテーブル）

【出力】
3種類の集計結果を、それぞれ別シートとして1つのExcelファイルに保存
ファイル名は「売上集計レポート.xlsx」

【環境】
Google Colab
```

**AIの回答例:**
```python
import pandas as pd
from google.colab import files

# ===== 1. ファイルアップロード =====
print("売上データ.xlsxをアップロードしてください")
uploaded = files.upload()

# ===== 2. データ読み込み =====
df = pd.read_excel('売上データ.xlsx')
print(f"読み込み: {len(df)}件のデータ")

# 日付列を変換して月を抽出
df['日付'] = pd.to_datetime(df['日付'])
df['月'] = df['日付'].dt.month

# ===== 3. 集計1: 部署別集計 =====
dept_summary = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
dept_summary.columns = ['売上合計', '平均単価', '件数']
dept_summary = dept_summary.sort_values('売上合計', ascending=False)

print("\n【部署別集計】")
print(dept_summary)

# ===== 4. 集計2: 月別売上 =====
monthly_sales = df.groupby('月')['金額'].sum()
monthly_sales = monthly_sales.to_frame('売上合計')

print("\n【月別売上】")
print(monthly_sales)

# ===== 5. 集計3: 部署×月クロス集計 =====
cross_table = df.pivot_table(
    values='金額',
    index='部署',
    columns='月',
    aggfunc='sum',
    fill_value=0
)

print("\n【部署×月クロス集計】")
print(cross_table)

# ===== 6. 結果を保存 =====
with pd.ExcelWriter('売上集計レポート.xlsx') as writer:
    dept_summary.to_excel(writer, sheet_name='部署別集計')
    monthly_sales.to_excel(writer, sheet_name='月別売上')
    cross_table.to_excel(writer, sheet_name='部署×月クロス集計')

print("\n'売上集計レポート.xlsx'に保存しました")
files.download('売上集計レポート.xlsx')
```

---

### 実践例3: 複数ファイル統合

**プロンプト:**
```
【依頼】
PythonでExcelファイルを処理するコードを書いてください。

【入力ファイル】
以下の3つのファイル（すべて同じ列構成）:
- sales_jan.xlsx
- sales_feb.xlsx
- sales_mar.xlsx

列構成: 日付、部署、商品名、金額

【やりたいこと】
1. 3つのファイルを1つに統合する
2. どのファイルから来たデータか分かるように「月」列を追加
3. 日付順にソートする

【出力】
統合データを「Q1売上統合.xlsx」として保存

【環境】
Google Colab（複数ファイルを一度にアップロードする）
```

**AIの回答例:**
```python
import pandas as pd
from google.colab import files

# ===== 1. 複数ファイルをアップロード =====
print("3つのファイル(sales_jan.xlsx, sales_feb.xlsx, sales_mar.xlsx)を")
print("一度に選択してアップロードしてください")
uploaded = files.upload()

# ===== 2. ファイルを読み込んで統合 =====
# ファイル名と月の対応
file_month_map = {
    'sales_jan.xlsx': '1月',
    'sales_feb.xlsx': '2月',
    'sales_mar.xlsx': '3月'
}

all_data = []

for filename, month_name in file_month_map.items():
    if filename in uploaded:
        df = pd.read_excel(filename)
        df['月'] = month_name  # 月列を追加
        all_data.append(df)
        print(f"読込: {filename} ({len(df)}行)")
    else:
        print(f"警告: {filename} が見つかりません")

# ===== 3. データを結合 =====
if len(all_data) > 0:
    combined = pd.concat(all_data, ignore_index=True)

    # 日付順にソート
    combined['日付'] = pd.to_datetime(combined['日付'])
    combined = combined.sort_values('日付')

    print(f"\n統合完了: 合計 {len(combined)}行")

    # ===== 4. 結果を確認 =====
    print("\n【統合データプレビュー】")
    print(combined.head(10))

    # ===== 5. 保存してダウンロード =====
    combined.to_excel('Q1売上統合.xlsx', index=False)
    print("\n'Q1売上統合.xlsx'に保存しました")
    files.download('Q1売上統合.xlsx')
else:
    print("エラー: 読み込めるファイルがありませんでした")
```

---

## テンプレート2: エラー解決

コードを実行してエラーが出たら、以下のテンプレートで質問しましょう。

### 基本構造

```
【状況】
以下のPythonコードを実行したらエラーが出ました。
原因と解決策を教えてください。

【コード】
```python
[エラーが出たコードをそのまま貼り付け]
```

【エラーメッセージ】
```
[エラーメッセージをそのまま貼り付け]
```

【やりたかったこと】
[何をしようとしていたか]

【環境】
Google Colab / Python 3.x
```

---

### 実践例: KeyError

**プロンプト:**
```
【状況】
以下のPythonコードを実行したらエラーが出ました。
原因と解決策を教えてください。

【コード】
```python
import pandas as pd

df = pd.read_excel('売上データ.xlsx')
result = df.groupby('部署')['売上'].sum()
print(result)
```

【エラーメッセージ】
```
KeyError: '売上'
```

【やりたかったこと】
部署ごとの売上合計を計算したい

【環境】
Google Colab
```

**AIの回答例:**

このエラーは、DataFrameに「売上」という名前の列が存在しないことが原因です。

**原因の確認方法:**
```python
# まず、実際の列名を確認しましょう
print(df.columns.tolist())
```

**考えられる原因と対処法:**

1. **列名が異なる場合**
   ```python
   # 実際の列名を確認して修正
   # 例: 列名が「金額」だった場合
   result = df.groupby('部署')['金額'].sum()
   ```

2. **列名に空白が含まれている場合**
   ```python
   # 列名に前後の空白がある場合
   result = df.groupby('部署')['売上 '].sum()  # 後ろに空白
   # または
   df.columns = df.columns.str.strip()  # 全列の空白を除去
   result = df.groupby('部署')['売上'].sum()
   ```

3. **列名が日本語でうまく読み込めていない場合**
   ```python
   # データの最初の数行を確認
   print(df.head())
   ```

**推奨される修正コード:**
```python
import pandas as pd

df = pd.read_excel('売上データ.xlsx')

# 列名を確認
print("列名:", df.columns.tolist())

# 列名を確認してから正しい列名を使用
# 以下は列名が「金額」だった場合の例
result = df.groupby('部署')['金額'].sum()
print(result)
```

---

### 実践例: FileNotFoundError

**プロンプト:**
```
【状況】
以下のPythonコードを実行したらエラーが出ました。

【コード】
```python
import pandas as pd
df = pd.read_excel('売上データ.xlsx')
```

【エラーメッセージ】
```
FileNotFoundError: [Errno 2] No such file or directory: '売上データ.xlsx'
```

【やりたかったこと】
Excelファイルを読み込みたい

【環境】
Google Colab
```

**AIの回答例:**

このエラーは、指定したファイルが見つからないことを意味します。

**Colabではファイルを先にアップロードする必要があります。**

**解決策:**
```python
import pandas as pd
from google.colab import files

# 1. ファイルをアップロード
print("売上データ.xlsxをアップロードしてください")
uploaded = files.upload()

# 2. アップロードされたファイルを確認
print("アップロードされたファイル:", list(uploaded.keys()))

# 3. ファイルを読み込み
df = pd.read_excel('売上データ.xlsx')
print(df.head())
```

**補足:**
- Colabのセッションが切れるとアップロードしたファイルは消えます
- 毎回アップロードが必要です
- 永続的に使いたい場合はGoogleドライブを使います:
  ```python
  from google.colab import drive
  drive.mount('/content/drive')
  df = pd.read_excel('/content/drive/MyDrive/売上データ.xlsx')
  ```

---

## テンプレート3: コードの理解

AIが生成したコードや、ネットで見つけたコードの意味がわからないときに使います。

### 基本構造

```
【依頼】
以下のPythonコードを1行ずつ説明してください。
特に [わからない部分] の意味が理解できません。

【コード】
```python
[理解したいコードを貼り付け]
```

【私のレベル】
- GASは使えます
- Pythonは初心者です
- pandasは今学習中です
```

---

### 実践例: groupbyの理解

**プロンプト:**
```
【依頼】
以下のPythonコードを1行ずつ説明してください。
特に `.agg(['sum', 'mean', 'count'])` の意味が理解できません。

【コード】
```python
result = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
result.columns = ['売上合計', '平均単価', '件数']
```

【私のレベル】
- GASは使えます
- Pythonは初心者です
```

**AIの回答例:**

このコードは、部署ごとに金額を集計しています。1行ずつ説明します。

**1行目の分解:**
```python
result = df.groupby('部署')['金額'].agg(['sum', 'mean', 'count'])
```

| 部分 | 意味 | GASで言うと |
|------|------|------------|
| `df` | 元のデータ | スプレッドシートのデータ |
| `.groupby('部署')` | 部署でグループ分け | UNIQUE関数で部署一覧を取得するイメージ |
| `['金額']` | 金額列を選択 | 集計対象の列を指定 |
| `.agg([...])` | 複数の集計を実行 | 複数のSUM, AVERAGEを一度に |
| `'sum'` | 合計を計算 | SUM関数 |
| `'mean'` | 平均を計算 | AVERAGE関数 |
| `'count'` | 件数を計算 | COUNT関数 |

**イメージ図:**
```
元データ:                          集計後:
┌────────┬───────┐               ┌────────┬────────┬──────┬──────┐
│  部署  │ 金額  │               │  部署  │  sum   │ mean │count │
├────────┼───────┤               ├────────┼────────┼──────┼──────┤
│ 営業部 │ 10000 │  ─┐           │ 営業部 │ 40000 │ 10000│   4  │
│ 営業部 │ 20000 │   ├→ 合計     │ 開発部 │ 25000 │ 12500│   2  │
│ 営業部 │ 5000  │   │           └────────┴────────┴──────┴──────┘
│ 営業部 │ 5000  │  ─┘
│ 開発部 │ 15000 │  ─┐
│ 開発部 │ 10000 │  ─┘→ 合計
└────────┴───────┘
```

**2行目:**
```python
result.columns = ['売上合計', '平均単価', '件数']
```
- 集計結果の列名を日本語に変更しています
- `sum` → `売上合計`、`mean` → `平均単価`、`count` → `件数`

**GASで同じことをすると:**
```javascript
// GASだと部署ごとにループして集計が必要
const depts = [...new Set(data.map(row => row[1]))];
depts.forEach(dept => {
  const deptData = data.filter(row => row[1] === dept);
  const sum = deptData.reduce((a, b) => a + b[3], 0);
  const mean = sum / deptData.length;
  const count = deptData.length;
  // ...
});
```

Pythonなら1行で同じことができます。

---

## テンプレート4: 改善・最適化

動くコードができたけど、もっと良くしたい場合に使います。

### 基本構造

```
【依頼】
以下のPythonコードを改善してください。

【現在のコード】
```python
[現在のコードを貼り付け]
```

【改善したい点】
- [具体的な改善ポイント]
- [例: 処理を高速化したい]
- [例: コードを短くしたい]
- [例: エラー処理を追加したい]

【制約】
- [例: 初心者にも読みやすいコードにしてほしい]
- [例: 外部ライブラリは追加したくない]
```

---

### 実践例: コードの短縮

**プロンプト:**
```
【依頼】
以下のPythonコードを改善してください。

【現在のコード】
```python
import pandas as pd

df = pd.read_excel('data.xlsx')

sales_dept = df[df['部署'] == '営業部']
sales_sum = sales_dept['金額'].sum()

dev_dept = df[df['部署'] == '開発部']
dev_sum = dev_dept['金額'].sum()

admin_dept = df[df['部署'] == '総務部']
admin_sum = admin_dept['金額'].sum()

print(f"営業部: {sales_sum}")
print(f"開発部: {dev_sum}")
print(f"総務部: {admin_sum}")
```

【改善したい点】
- 同じような処理を繰り返しているので、もっと短く書きたい
- 部署が増えても対応できるようにしたい

【制約】
- 初心者にも読みやすいコードにしてほしい
```

**AIの回答例:**

`groupby`を使うと、全部署を一度に集計できます。

**改善後のコード:**
```python
import pandas as pd

df = pd.read_excel('data.xlsx')

# 全部署の売上合計を一度に計算
dept_sales = df.groupby('部署')['金額'].sum()

# 結果を表示
print("【部署別売上】")
print(dept_sales)
```

**さらに見やすくするなら:**
```python
import pandas as pd

df = pd.read_excel('data.xlsx')

# 部署別に売上を集計
dept_sales = df.groupby('部署')['金額'].sum()

# 売上の多い順にソート
dept_sales = dept_sales.sort_values(ascending=False)

# 見やすく表示
print("【部署別売上】")
for dept, sales in dept_sales.items():
    print(f"  {dept}: ¥{sales:,}")

# 合計も表示
print(f"  --------")
print(f"  合計: ¥{dept_sales.sum():,}")
```

**改善のポイント:**
- 3回のフィルタリング → 1回の`groupby`で完了
- 部署が増えても、コードの変更は不要
- コード行数: 15行 → 5行

---

## よくあるプロンプトの失敗例

### 失敗例1: 曖昧なプロンプト

**悪い例:**
```
Excelを処理するコードを書いて
```

**なぜダメか:**
- どんなExcelファイルかわからない
- 何をしたいのかわからない
- 出力形式もわからない

**良い例:**
```
【入力ファイル】売上データ.xlsx（列: 日付, 部署, 金額）
【やりたいこと】部署ごとの売上合計を計算
【出力】結果を新しいExcelファイルに保存
```

---

### 失敗例2: 環境を伝えない

**悪い例:**
```
pandasでファイルを読み込むコードを書いて
```

**なぜダメか:**
- ローカル環境とColabでは、ファイルの扱いが異なる
- Colabでは`files.upload()`が必要

**良い例:**
```
【環境】Google Colab
pandasでExcelファイルをアップロードして読み込むコードを書いて
```

---

### 失敗例3: エラーメッセージを省略する

**悪い例:**
```
コードを実行したらエラーが出ました。直してください。

[コード]
df = pd.read_excel('data.xlsx')
```

**なぜダメか:**
- どんなエラーか分からないと、原因を特定できない

**良い例:**
```
【エラーメッセージ】
FileNotFoundError: [Errno 2] No such file or directory: 'data.xlsx'

【コード】
df = pd.read_excel('data.xlsx')

【環境】Google Colab
```

---

## プロンプト集：コピペで使えるテンプレート

### 1. ファイル読み込み
```
【依頼】
Google Colabで「○○○.xlsx」を読み込むコードを書いてください。
ファイルアップロードの処理も含めてください。
```

### 2. 条件フィルタリング
```
【依頼】
pandasで以下の条件でデータを抽出するコードを書いてください。
- 入力: ○○○.xlsx
- 条件: ○○○列が○○○以上
- 出力: 抽出結果を新しいExcelファイルに保存
```

### 3. グループ別集計
```
【依頼】
pandasで○○○列ごとに○○○列を集計するコードを書いてください。
- 入力: ○○○.xlsx
- 集計: 合計、平均、件数
- 出力: 集計結果をExcelファイルに保存
```

### 4. 複数ファイル統合
```
【依頼】
複数のExcelファイルを1つに統合するコードを書いてください。
- 対象ファイル: ○○○_01.xlsx, ○○○_02.xlsx, ○○○_03.xlsx
- すべて同じ列構成（列: ○○○, ○○○, ○○○）
- 環境: Google Colab
```

### 5. エラー解決
```
【状況】
以下のコードでエラーが出ました。原因と解決策を教えてください。

【コード】
```python
[コードを貼り付け]
```

【エラー】
```
[エラーメッセージを貼り付け]
```

【環境】Google Colab
```

### 6. コード理解
```
【依頼】
以下のコードの意味を1行ずつ説明してください。
GASは使えますが、Pythonは初心者です。

```python
[コードを貼り付け]
```
```

---

## AIへの質問のコツ

### 1. 具体的に書く
```
悪い: データを処理したい
良い: 売上データ.xlsxの部署列でグループ化して、金額列の合計を計算したい
```

### 2. 段階的に質問する
```
1回目: 「部署別の売上合計を計算するコードを書いて」
2回目: 「さらに月別の集計も追加して」
3回目: 「結果をグラフにする方法も教えて」
```

### 3. 自分のレベルを伝える
```
私のレベル:
- GASは使えます
- Pythonは今週始めたばかりです
- pandasは初めて使います

初心者にも分かるように説明してください。
```

### 4. 動いたら「なぜ動くか」を聞く
```
このコードは動きましたが、以下の部分がなぜ動くのか理解できません:
- `df[df['金額'] >= 50000]` ← なぜこれでフィルタリングできるのか
- `groupby('部署')` ← 内部でどんな処理が行われているのか
```

---

## この節のまとめ

- AIに依頼するときは「入力・やりたいこと・出力・環境」を明記する
- エラーが出たら、エラーメッセージをそのままコピペして質問する
- コードの意味がわからなければ、遠慮なく質問する
- 曖昧なプロンプトは、曖昧な回答しか返ってこない

**AIは最強の学習パートナーです。どんどん質問して、Python力を高めていきましょう！**

---

## 次の章へ

おめでとうございます！第3章「Excel×Python」を完了しました。

この章で学んだこと：
- openpyxlでExcelファイルを操作する
- pandasで大量データを高速処理する
- GASの6分制限を超える処理をPythonで実現する
- 複数ファイルを一括処理する
- AIを活用してコードを生成・改善する

**次の第4章では、いよいよローカル環境を構築します。**

- Colabを卒業して、自分のPCでPythonを動かす
- **venv**で環境を「壊さない」作法を身につける
- 作ったツールを**exe化**して配布する

「環境を壊さない」Python作法を学んで、本格的なPythonistaへの道を歩み始めましょう！
