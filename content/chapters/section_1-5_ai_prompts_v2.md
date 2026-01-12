# 1-5. AIプロンプトテンプレート（基礎文法編）

## この節で学ぶこと

- AIを「プログラミング家庭教師」として活用する方法
- GASからPythonへの変換をAIに依頼する方法
- エラーが出たときの質問の仕方
- コードの意味を理解するための質問の仕方

---

## なぜAIを活用するのか

プログラミング学習で最も効率的な方法は「わからないことをすぐに聞ける環境」を作ることです。

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  従来の学習方法:                                             │
│                                                              │
│  エラーが出る → 検索 → 難しい記事ばかり → 理解できない     │
│              → 時間だけが過ぎる → 挫折                      │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  AIを使った学習方法:                                         │
│                                                              │
│  エラーが出る → AIに質問 → 自分のコードに対する回答       │
│              → すぐ解決 → 学習が進む                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

AIは24時間対応の「プログラミング家庭教師」です。遠慮なく活用しましょう。

---

## テンプレート1: GASコードをPythonに変換

GASで書いたコードをPythonに変換してもらうテンプレートです。

### 基本構造

```
【依頼】
以下のGAS（JavaScript）コードをPythonに変換してください。

【GASコード】
```javascript
[ここにGASコードを貼り付け]
```

【追加の要望】
- 変換後のコードにはコメントを入れてください
- GASとの違いを説明してください
- Google Colabで実行できるようにしてください
```

### 実践例

**プロンプト:**
```
【依頼】
以下のGAS（JavaScript）コードをPythonに変換してください。

【GASコード】
```javascript
function processData() {
  const data = [
    {name: "田中", age: 25, department: "営業部"},
    {name: "佐藤", age: 30, department: "開発部"},
    {name: "鈴木", age: 35, department: "営業部"}
  ];

  const salesDept = data.filter(person => person.department === "営業部");
  const names = salesDept.map(person => person.name);

  console.log(`営業部のメンバー: ${names.join(", ")}`);
}
```

【追加の要望】
- 変換後のコードにはコメントを入れてください
- GASとの違いを説明してください
```

**AIの回答例:**

以下がPythonに変換したコードです：

```python
# データの定義（GASのオブジェクト配列 → Pythonの辞書リスト）
data = [
    {"name": "田中", "age": 25, "department": "営業部"},
    {"name": "佐藤", "age": 30, "department": "開発部"},
    {"name": "鈴木", "age": 35, "department": "営業部"}
]

# 営業部のメンバーをフィルタリング
# GASの filter() → Pythonのリスト内包表記
sales_dept = [person for person in data if person["department"] == "営業部"]

# 名前だけを抽出
# GASの map() → Pythonのリスト内包表記
names = [person["name"] for person in sales_dept]

# 結果を表示
# GASの console.log() → Pythonの print()
# GASの join() → Pythonも join() だが書き方が異なる
print(f"営業部のメンバー: {', '.join(names)}")
```

**実行結果：**
```
営業部のメンバー: 田中, 鈴木
```

**GASとの主な違い：**

| 項目 | GAS | Python |
|------|-----|--------|
| オブジェクト定義 | `{name: "田中"}` | `{"name": "田中"}` |
| filter | `.filter(x => 条件)` | `[x for x in data if 条件]` |
| map | `.map(x => 式)` | `[式 for x in data]` |
| join | `array.join(", ")` | `", ".join(array)` |

---

## テンプレート2: エラーを解決してもらう

エラーが出たときに、AIに解決を依頼するテンプレートです。

### 基本構造

```
【状況】
Pythonで以下のエラーが出ました。原因と解決策を教えてください。

【エラーメッセージ】
```
[エラーメッセージをそのままコピペ]
```

【実行したコード】
```python
[コードを貼り付け]
```

【やりたかったこと】
[何をしようとしていたかを説明]

【環境】
Google Colab
```

### 実践例1: NameError

**プロンプト:**
```
【状況】
Pythonで以下のエラーが出ました。原因と解決策を教えてください。

【エラーメッセージ】
```
NameError: name 'prnt' is not defined
```

【実行したコード】
```python
message = "Hello World"
prnt(message)
```

【やりたかったこと】
メッセージを表示したかった

【環境】
Google Colab
```

**AIの回答例:**

**原因：**
`prnt` という関数は存在しません。`print` のスペルミスです。

**解決策：**
```python
message = "Hello World"
print(message)  # prnt → print に修正
```

**実行結果：**
```
Hello World
```

**補足：**
NameError は「その名前（変数や関数）が見つからない」というエラーです。よくある原因は：
- スペルミス
- 変数を定義する前に使おうとした
- importを忘れた

---

### 実践例2: IndentationError

**プロンプト:**
```
【状況】
Pythonで以下のエラーが出ました。原因と解決策を教えてください。

【エラーメッセージ】
```
IndentationError: expected an indented block after 'if' statement on line 1
```

【実行したコード】
```python
if score >= 60:
print("合格")
```

【やりたかったこと】
60点以上なら「合格」と表示したい

【環境】
Google Colab
```

**AIの回答例:**

**原因：**
Pythonでは `if` の後のブロックをインデント（字下げ）で示す必要があります。GASでは `{}` でブロックを示しますが、Pythonはインデントが文法的に意味を持ちます。

**解決策：**
```python
if score >= 60:
    print("合格")  # 4スペースでインデント
```

**実行前に変数を定義：**
```python
score = 75

if score >= 60:
    print("合格")
```

**実行結果：**
```
合格
```

**GASとの違い：**
```javascript
// GAS: {} でブロックを示す
if (score >= 60) {
    console.log("合格");
}
```

```python
# Python: インデントでブロックを示す
if score >= 60:
    print("合格")
```

---

### 実践例3: TypeError

**プロンプト:**
```
【状況】
Pythonで以下のエラーが出ました。原因と解決策を教えてください。

【エラーメッセージ】
```
TypeError: can only concatenate str (not "int") to str
```

【実行したコード】
```python
age = 25
message = "年齢は" + age + "歳です"
print(message)
```

【やりたかったこと】
年齢を含むメッセージを作成したい

【環境】
Google Colab
```

**AIの回答例:**

**原因：**
Pythonでは文字列（str）と数値（int）を `+` で直接連結できません。GASでは自動的に型変換されますが、Pythonは厳格です。

**解決策（3つの方法）：**

```python
age = 25

# 方法1: str()で型変換
message = "年齢は" + str(age) + "歳です"
print(message)

# 方法2: f文字列を使う（推奨）
message = f"年齢は{age}歳です"
print(message)

# 方法3: format()メソッドを使う
message = "年齢は{}歳です".format(age)
print(message)
```

**実行結果：**
```
年齢は25歳です
年齢は25歳です
年齢は25歳です
```

**推奨：** f文字列（方法2）が最も読みやすく、現代的な書き方です。

---

## テンプレート3: コードの意味を理解する

AIが生成したコードや、ネットで見つけたコードの意味を理解するためのテンプレートです。

### 基本構造

```
【依頼】
以下のPythonコードを1行ずつ説明してください。

【コード】
```python
[理解したいコードを貼り付け]
```

【私のレベル】
- GASは使えます
- Pythonは初心者です

【特にわからない部分】
[具体的にわからない行や表現があれば記載]
```

### 実践例

**プロンプト:**
```
【依頼】
以下のPythonコードを1行ずつ説明してください。

【コード】
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [n for n in numbers if n % 2 == 0]
total = sum(evens)
print(f"偶数の合計: {total}")
```

【私のレベル】
- GASは使えます
- Pythonは初心者です

【特にわからない部分】
`[n for n in numbers if n % 2 == 0]` の意味がわかりません
```

**AIの回答例:**

1行ずつ説明します。

**1行目：**
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```
1から10までの数字が入ったリストを作成し、`numbers` という変数に代入しています。GASでは `const numbers = [1, 2, ...]` と書くのと同じです。

**2行目（リスト内包表記）：**
```python
evens = [n for n in numbers if n % 2 == 0]
```
これは「リスト内包表記」というPython独自の書き方です。分解して説明します：

```
[n for n in numbers if n % 2 == 0]
 ↑    ↑      ↑         ↑
 ①   ②     ③        ④

① n: 結果に入れる値
② for n in numbers: numbersの各要素をnとして取り出す
③ numbers: 元のリスト
④ if n % 2 == 0: nを2で割った余りが0（＝偶数）の場合のみ
```

GASで書くと：
```javascript
const evens = numbers.filter(n => n % 2 === 0);
```

**3行目：**
```python
total = sum(evens)
```
`sum()` 関数でリストの合計を計算します。GASでは `evens.reduce((a, b) => a + b, 0)` と書く必要がありますが、Pythonは組み込み関数で一発です。

**4行目：**
```python
print(f"偶数の合計: {total}")
```
f文字列で結果を表示します。GASの `` console.log(`偶数の合計: ${total}`) `` に相当します。

**全体の流れ：**
```
numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ↓ 偶数だけフィルタリング
evens: [2, 4, 6, 8, 10]
    ↓ 合計
total: 30
    ↓ 表示
"偶数の合計: 30"
```

---

## テンプレート4: 書き方を調べる

「〇〇をする方法」を聞くテンプレートです。

### 基本構造

```
【依頼】
Pythonで「〇〇」をする方法を教えてください。

【詳細】
[やりたいことの詳細説明]

【GASでの書き方】（もしあれば）
```javascript
[GASでの書き方]
```

【環境】
Google Colab
```

### 実践例

**プロンプト:**
```
【依頼】
Pythonで「リストの中から最大値と最小値を取得する」方法を教えてください。

【詳細】
売上データのリストから、最高売上と最低売上を取得したい

【GASでの書き方】
```javascript
const sales = [10000, 25000, 15000, 30000, 20000];
const maxSales = Math.max(...sales);
const minSales = Math.min(...sales);
```

【環境】
Google Colab
```

**AIの回答例:**

Pythonでは `max()` と `min()` という組み込み関数を使います。

```python
sales = [10000, 25000, 15000, 30000, 20000]

# 最大値
max_sales = max(sales)
print(f"最高売上: {max_sales}円")

# 最小値
min_sales = min(sales)
print(f"最低売上: {min_sales}円")

# 合計と平均も一緒に
total = sum(sales)
average = total / len(sales)
print(f"売上合計: {total}円")
print(f"平均売上: {average}円")
```

**実行結果：**
```
最高売上: 30000円
最低売上: 10000円
売上合計: 100000円
平均売上: 20000.0円
```

**GASとの比較：**

| 操作 | GAS | Python |
|------|-----|--------|
| 最大値 | `Math.max(...arr)` | `max(arr)` |
| 最小値 | `Math.min(...arr)` | `min(arr)` |
| 合計 | `arr.reduce((a,b)=>a+b,0)` | `sum(arr)` |
| 要素数 | `arr.length` | `len(arr)` |

Pythonの方がシンプルですね！

---

## よくある質問パターン集

### パターン1: 「GASでは〇〇と書くが、Pythonでは？」

```
GASでは配列の末尾に要素を追加するとき .push() を使いますが、
Pythonではどう書きますか？
```

### パターン2: 「このエラーの意味は？」

```
「TypeError: 'str' object is not callable」というエラーが出ました。
これはどういう意味ですか？原因と解決策を教えてください。
```

### パターン3: 「もっと短く書ける？」

```
以下のコードをもっと短く（Pythonらしく）書く方法はありますか？

[コードを貼り付け]
```

### パターン4: 「なぜ動くのか理解したい」

```
以下のコードは動きましたが、なぜ動くのかわかりません。
特に [わからない部分] の仕組みを教えてください。

[コードを貼り付け]
```

### パターン5: 「ベストプラクティスは？」

```
Pythonで [やりたいこと] をする場合、
どのように書くのがベストプラクティスですか？
```

---

## AIへの質問のコツ

### 1. 具体的に書く

```
悪い例: 「エラーが出ました」
良い例: 「TypeError: can only concatenate str (not "int") to str
        というエラーが出ました。コードは [コード] です。」
```

### 2. 自分のレベルを伝える

```
良い例: 「GASは使えますが、Pythonは初心者です」
      「プログラミング自体が初めてです」
```

### 3. やりたいことを明確に

```
悪い例: 「データを処理したい」
良い例: 「売上データのリストから、10000円以上のデータだけを抽出したい」
```

### 4. 環境を伝える

```
良い例: 「環境: Google Colab」
      「環境: Windows 11, Python 3.11」
```

---

## 練習：AIに質問してみよう

以下の質問をAI（ChatGPT、Claude等）に投げてみてください。

### 練習1
```
【依頼】
GASの以下のコードをPythonに変換してください。

【GASコード】
```javascript
function sumPrices() {
  const prices = [100, 200, 300, 400, 500];
  let total = 0;
  for (const price of prices) {
    total += price;
  }
  console.log("合計: " + total);
}
```

【環境】
Google Colab
```

### 練習2
```
【依頼】
Pythonで「辞書のリストから、特定のキーの値だけを抽出してリストにする」
方法を教えてください。

【具体例】
以下のデータから名前だけのリスト ["田中", "佐藤", "鈴木"] を作りたい。

data = [
    {"name": "田中", "age": 25},
    {"name": "佐藤", "age": 30},
    {"name": "鈴木", "age": 35}
]
```

---

## この節のまとめ

- AIは24時間対応の「プログラミング家庭教師」
- エラーが出たら、エラーメッセージとコードをそのままAIに質問
- 「GASではこう書くが、Pythonでは？」という質問が効果的
- 具体的に質問することで、具体的な回答が得られる
- わからないコードは「1行ずつ説明して」と依頼する

**次の節では、ローカル環境への移行について説明します。今はColabで十分ですが、将来のために知っておきましょう。**
