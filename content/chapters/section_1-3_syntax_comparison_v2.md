# 1-3. GAS経験者向け：文法比較チートシート

## この節で学ぶこと

- GAS（JavaScript）とPythonの文法の違いを理解する
- 「これGASでどう書くんだっけ」を「Pythonだとこう書く」に変換する
- 各文法の違いを実際に実行して体験する

---

## 最も重要な3つの違い

Pythonを書くとき、GAS経験者が最初に戸惑う3つのポイントがあります。

```
┌─────────────────────────────────────────────────────────────┐
│  GAS → Python で最初に覚えるべき3つの違い                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. {} が不要、代わりにインデント                           │
│                                                              │
│  2. let/const/var が不要                                    │
│                                                              │
│  3. 文末の ; が不要                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

これだけ覚えておけば、あとは「GASに似ている」と感じるはずです。

---

## 1. 変数宣言

### GAS（JavaScript）の場合

```javascript
let name = "田中太郎";     // 変更可能な変数
const TAX_RATE = 0.1;      // 定数（変更不可）
var oldStyle = "古い書き方"; // 非推奨
```

### Pythonの場合

**Colabで実行してみよう：**
```python
name = "田中太郎"     # let/const/var は不要！
TAX_RATE = 0.1        # 大文字は「定数のつもり」という慣習
old_style = "古い書き方"

print(f"名前: {name}")
print(f"税率: {TAX_RATE}")
```

**実行結果：**
```
名前: 田中太郎
税率: 0.1
```

### ポイント

```
┌────────────────────────────────────────────────────────────┐
│  GAS                          Python                        │
├────────────────────────────────────────────────────────────┤
│  let name = "田中";          name = "田中"                  │
│  const TAX = 0.1;            TAX = 0.1    ← 大文字で慣習的 │
│      ↑       ↑                         ↑                  │
│   キーワード  セミコロン             どちらも不要          │
└────────────────────────────────────────────────────────────┘
```

> **注意**: Pythonには本当の「定数」はありません。`TAX_RATE = 0.1` と書いても、後から `TAX_RATE = 0.2` と変更できてしまいます。大文字で書くのは「これは定数として扱ってね」という**慣習**です。

---

## 2. 文字列とf文字列

### GAS（JavaScript）の場合

```javascript
const name = "田中";
const age = 25;

// テンプレートリテラル（バッククォート）
const message = `こんにちは、${name}さん。${age}歳ですね。`;
console.log(message);
```

### Pythonの場合

**Colabで実行してみよう：**
```python
name = "田中"
age = 25

# f文字列（フォーマット文字列）
message = f"こんにちは、{name}さん。{age}歳ですね。"
print(message)
```

**実行結果：**
```
こんにちは、田中さん。25歳ですね。
```

### 比較

| 項目 | GAS | Python |
|------|-----|--------|
| 構文 | `` `${変数}` `` | `f"{変数}"` |
| 記号 | バッククォート | 普通のクォート + `f` |
| 変数埋め込み | `${name}` | `{name}` |

### f文字列の便利な機能

```python
# 計算式も埋め込める
price = 1000
tax_rate = 0.1
print(f"税込価格: {price * (1 + tax_rate)}円")

# 桁区切り
big_number = 1234567890
print(f"金額: {big_number:,}円")

# 小数点以下の桁数指定
pi = 3.141592653589793
print(f"円周率: {pi:.2f}")  # 小数点以下2桁
```

**実行結果：**
```
税込価格: 1100.0円
金額: 1,234,567,890円
円周率: 3.14
```

---

## 3. 出力（print）

### GAS（JavaScript）の場合

```javascript
console.log("Hello");
Logger.log("Hello");  // GAS独自
```

### Pythonの場合

**Colabで実行してみよう：**
```python
print("Hello")
print("複数の", "値を", "出力")  # カンマ区切りで複数出力
print("改行なし", end="")        # 改行しない
print(" ← 続き")
```

**実行結果：**
```
Hello
複数の 値を 出力
改行なし ← 続き
```

---

## 4. 条件分岐（if文）

### GAS（JavaScript）の場合

```javascript
const score = 75;

if (score >= 80) {
  console.log("合格");
} else if (score >= 60) {
  console.log("追試");
} else {
  console.log("不合格");
}
```

### Pythonの場合

**Colabで実行してみよう：**
```python
score = 75

if score >= 80:
    print("合格")
elif score >= 60:
    print("追試")
else:
    print("不合格")
```

**実行結果：**
```
追試
```

### 重要な違い

```
┌────────────────────────────────────────────────────────────┐
│  GAS                                Python                  │
├────────────────────────────────────────────────────────────┤
│  if (条件) {                       if 条件:                 │
│      処理                              処理  ← インデント  │
│  } else if (条件) {                elif 条件:               │
│      処理                              処理                 │
│  } else {                          else:                    │
│      処理                              処理                 │
│  }                                                          │
├────────────────────────────────────────────────────────────┤
│  ・条件を () で囲む必要がある     ・() は不要              │
│  ・{} でブロックを示す             ・インデントで示す       │
│  ・else if                         ・elif                   │
│  ・条件の後に : 不要              ・条件の後に : 必須      │
└────────────────────────────────────────────────────────────┘
```

### インデントの重要性

**Pythonではインデント（字下げ）が文法的に意味を持ちます：**

```python
# 正しい（4スペースでインデント）
if score >= 60:
    print("合格")
    print("おめでとう")  # ← 同じブロック

# 間違い（インデントがない）
if score >= 60:
print("合格")  # ← IndentationError: expected an indented block
```

**エラー例：**
```
IndentationError: expected an indented block after 'if' statement on line 1
```

---

## 5. 配列（リスト）

### GAS（JavaScript）の場合

```javascript
const fruits = ["りんご", "みかん", "ぶどう"];
fruits.push("いちご");           // 追加
console.log(fruits[0]);          // りんご
console.log(fruits.length);      // 4
```

### Pythonの場合

**Colabで実行してみよう：**
```python
fruits = ["りんご", "みかん", "ぶどう"]
fruits.append("いちご")          # 追加（pushではなくappend）
print(fruits[0])                 # りんご
print(len(fruits))               # 4（.lengthではなくlen()関数）

# リストの内容を確認
print(fruits)
```

**実行結果：**
```
りんご
4
['りんご', 'みかん', 'ぶどう', 'いちご']
```

### 主な違い

| 操作 | GAS | Python |
|------|-----|--------|
| 追加 | `.push()` | `.append()` |
| 長さ | `.length` | `len()` |
| 末尾要素 | `arr[arr.length - 1]` | `arr[-1]` |
| 削除（値指定） | `.splice(index, 1)` | `.remove(値)` |

### Pythonのリスト独自機能：マイナスインデックス

```python
fruits = ["りんご", "みかん", "ぶどう", "いちご"]

print(fruits[-1])   # いちご（末尾）
print(fruits[-2])   # ぶどう（末尾から2番目）
```

**実行結果：**
```
いちご
ぶどう
```

### Pythonのリスト独自機能：スライス

```python
fruits = ["りんご", "みかん", "ぶどう", "いちご", "メロン"]

print(fruits[1:3])   # インデックス1から3未満
print(fruits[:2])    # 最初から2未満
print(fruits[2:])    # インデックス2から最後まで
print(fruits[::2])   # 2つおき
```

**実行結果：**
```
['みかん', 'ぶどう']
['りんご', 'みかん']
['ぶどう', 'いちご', 'メロン']
['りんご', 'ぶどう', 'メロン']
```

---

## 6. オブジェクト（辞書）

### GAS（JavaScript）の場合

```javascript
const person = {
  name: "田中太郎",
  age: 25,
  department: "営業部"
};

console.log(person.name);        // ドット記法
console.log(person["age"]);      // ブラケット記法
```

### Pythonの場合

**Colabで実行してみよう：**
```python
person = {
    "name": "田中太郎",
    "age": 25,
    "department": "営業部"
}

# ブラケット記法のみ（ドット記法は使えない）
print(person["name"])
print(person["age"])

# 全体を表示
print(person)
```

**実行結果：**
```
田中太郎
25
{'name': '田中太郎', 'age': 25, 'department': '営業部'}
```

### 重要な違い

```
┌────────────────────────────────────────────────────────────┐
│  GAS                                Python                  │
├────────────────────────────────────────────────────────────┤
│  {                                  {                       │
│    name: "田中",    ← キー裸       "name": "田中",  ←クォート必須│
│    age: 25                          "age": 25               │
│  }                                  }                       │
├────────────────────────────────────────────────────────────┤
│  person.name       ← ドット記法OK  person["name"]  ← ブラケットのみ│
│  person["name"]    ← こちらもOK                             │
└────────────────────────────────────────────────────────────┘
```

### 辞書の操作

```python
person = {"name": "田中太郎", "age": 25}

# 値の変更
person["age"] = 26

# 新しいキーの追加
person["email"] = "tanaka@example.com"

# キーの存在確認
if "name" in person:
    print("nameキーがあります")

# 全キーを取得
print(list(person.keys()))

# 全値を取得
print(list(person.values()))

# キーと値のペアを取得
for key, value in person.items():
    print(f"{key}: {value}")
```

**実行結果：**
```
nameキーがあります
['name', 'age', 'email']
['田中太郎', 26, 'tanaka@example.com']
name: 田中太郎
age: 26
email: tanaka@example.com
```

---

## 7. 繰り返し（for文）

### GAS（JavaScript）の場合

```javascript
// 配列のループ
const fruits = ["りんご", "みかん", "ぶどう"];
for (const fruit of fruits) {
  console.log(fruit);
}

// 回数指定のループ
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

### Pythonの場合

**Colabで実行してみよう：**
```python
# リストのループ
fruits = ["りんご", "みかん", "ぶどう"]
for fruit in fruits:
    print(fruit)
```

**実行結果：**
```
りんご
みかん
ぶどう
```

```python
# 回数指定のループ
for i in range(5):
    print(i)
```

**実行結果：**
```
0
1
2
3
4
```

### 違いのまとめ

| パターン | GAS | Python |
|----------|-----|--------|
| 配列ループ | `for (const x of arr)` | `for x in arr:` |
| 回数ループ | `for (let i = 0; i < n; i++)` | `for i in range(n):` |
| 範囲ループ | `for (let i = 1; i <= 5; i++)` | `for i in range(1, 6):` |

### range()の使い方

```python
# range(終了)：0から終了-1まで
print(list(range(5)))       # [0, 1, 2, 3, 4]

# range(開始, 終了)：開始から終了-1まで
print(list(range(1, 6)))    # [1, 2, 3, 4, 5]

# range(開始, 終了, 間隔)
print(list(range(0, 10, 2))) # [0, 2, 4, 6, 8]
print(list(range(10, 0, -1))) # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

**実行結果：**
```
[0, 1, 2, 3, 4]
[1, 2, 3, 4, 5]
[0, 2, 4, 6, 8]
[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

### インデックスと値を同時に取得（enumerate）

```python
fruits = ["りんご", "みかん", "ぶどう"]

# GASでは for (let i = 0; i < arr.length; i++) と書く
# Pythonでは enumerate() を使う

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

**実行結果：**
```
0: りんご
1: みかん
2: ぶどう
```

---

## 8. 関数定義

### GAS（JavaScript）の場合

```javascript
function greet(name) {
  return `こんにちは、${name}さん`;
}

// アロー関数
const add = (a, b) => a + b;

console.log(greet("田中"));
console.log(add(3, 5));
```

### Pythonの場合

**Colabで実行してみよう：**
```python
def greet(name):
    return f"こんにちは、{name}さん"

# ラムダ式（アロー関数に相当）
add = lambda a, b: a + b

print(greet("田中"))
print(add(3, 5))
```

**実行結果：**
```
こんにちは、田中さん
8
```

### 比較

| 項目 | GAS | Python |
|------|-----|--------|
| 通常の関数 | `function 名前() {}` | `def 名前():` |
| 無名関数 | `(a, b) => a + b` | `lambda a, b: a + b` |
| 戻り値 | `return 値;` | `return 値` |

### デフォルト引数

```python
def greet(name, greeting="こんにちは"):
    return f"{greeting}、{name}さん"

print(greet("田中"))              # デフォルト値を使用
print(greet("田中", "おはよう"))  # 引数を指定
```

**実行結果：**
```
こんにちは、田中さん
おはよう、田中さん
```

---

## 9. コメント

### GAS（JavaScript）の場合

```javascript
// 1行コメント

/*
複数行コメント
ここも無視される
*/
```

### Pythonの場合

```python
# 1行コメント

# 複数行コメントは
# 各行に # を付ける

"""
または、ダブルクォート3つで
複数行の文字列として書ける
（ドキュメンテーション文字列として使う）
"""
```

---

## 文法比較チートシート（総まとめ）

**Colabで保存しておくと便利なチートシートです：**

```python
# ============================================
# GAS → Python 文法チートシート
# ============================================

# ----- 変数宣言 -----
# GAS:  let x = 10;  const Y = 20;
# Python:
x = 10
Y = 20  # 大文字で定数を表現（慣習）

# ----- 文字列結合 -----
# GAS:  `Hello ${name}`
# Python:
name = "世界"
message = f"Hello {name}"

# ----- 出力 -----
# GAS:  console.log()
# Python:
print("Hello")

# ----- 条件分岐 -----
# GAS:  if () {} else if {} else {}
# Python:
score = 75
if score >= 80:
    print("合格")
elif score >= 60:
    print("追試")
else:
    print("不合格")

# ----- 配列/リスト -----
# GAS:  arr.push(), arr.length
# Python:
arr = [1, 2, 3]
arr.append(4)       # push → append
print(len(arr))     # .length → len()
print(arr[-1])      # 末尾要素

# ----- オブジェクト/辞書 -----
# GAS:  {name: "田中"}, obj.name
# Python:
obj = {"name": "田中"}
print(obj["name"])  # ドット記法は使えない

# ----- forループ -----
# GAS:  for (const x of arr), for (let i = 0; i < n; i++)
# Python:
for x in arr:
    print(x)
for i in range(5):
    print(i)

# ----- 関数定義 -----
# GAS:  function greet(name) {}
# Python:
def greet(name):
    return f"こんにちは、{name}さん"

# ============================================
print("チートシート読み込み完了！")
```

---

## 練習問題

### 問題1: GASコードをPythonに変換

以下のGASコードをPythonに変換してください：

```javascript
function calculateTotal() {
  const prices = [100, 200, 300, 400, 500];
  let total = 0;

  for (const price of prices) {
    total += price;
  }

  console.log(`合計: ${total}円`);
}
```

<details>
<summary>解答例</summary>

```python
def calculate_total():
    prices = [100, 200, 300, 400, 500]
    total = 0

    for price in prices:
        total += price

    print(f"合計: {total}円")

# 関数を呼び出す
calculate_total()
```

**実行結果：**
```
合計: 1500円
```

**さらにPythonらしく書くと：**
```python
prices = [100, 200, 300, 400, 500]
total = sum(prices)  # sum()関数で一発
print(f"合計: {total}円")
```

</details>

### 問題2: 辞書の操作

以下のGASコードをPythonに変換してください：

```javascript
const employee = {
  name: "田中太郎",
  age: 25,
  department: "営業部"
};

for (const key in employee) {
  console.log(`${key}: ${employee[key]}`);
}
```

<details>
<summary>解答例</summary>

```python
employee = {
    "name": "田中太郎",
    "age": 25,
    "department": "営業部"
}

for key, value in employee.items():
    print(f"{key}: {value}")
```

**実行結果：**
```
name: 田中太郎
age: 25
department: 営業部
```

</details>

---

## この節のまとめ

| 項目 | GAS (JavaScript) | Python |
|------|-----------------|--------|
| 変数宣言 | `let x = 10;` | `x = 10` |
| 定数 | `const X = 10;` | `X = 10`（慣習） |
| 文字列結合 | `` `Hello ${name}` `` | `f"Hello {name}"` |
| 出力 | `console.log()` | `print()` |
| 条件分岐 | `if () {}` | `if :` + インデント |
| else if | `else if` | `elif` |
| 配列への追加 | `.push()` | `.append()` |
| 配列の長さ | `.length` | `len()` |
| オブジェクト | `{key: value}` | `{"key": value}` |
| forループ | `for (x of arr)` | `for x in arr:` |
| 回数ループ | `for (let i=0; i<n; i++)` | `for i in range(n):` |
| 関数定義 | `function f() {}` | `def f():` |
| 文末 | `;` 必要 | 不要 |
| ブロック | `{}` | インデント |
| コメント | `//` | `#` |

**次の節では、Python固有の文法をより詳しく学びます。**
