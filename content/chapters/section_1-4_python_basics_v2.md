# 1-4. Python基礎文法を実践で学ぶ

## この節で学ぶこと

- Pythonのデータ型を理解する
- 型変換を使いこなす
- リストと辞書の操作をマスターする
- リスト内包表記（Pythonの強力な機能）を学ぶ
- よくあるエラーと対処法を知る

---

## Step 1: データ型を理解する

Pythonの主要なデータ型を、実際に動かして確認しましょう。

```python
# ===== Pythonの主要なデータ型 =====

# 整数（int）
age = 25
print(f"age = {age}, 型: {type(age)}")

# 浮動小数点数（float）
price = 1980.5
print(f"price = {price}, 型: {type(price)}")

# 文字列（str）
name = "田中太郎"
print(f"name = {name}, 型: {type(name)}")

# 真偽値（bool）
is_active = True
is_deleted = False
print(f"is_active = {is_active}, 型: {type(is_active)}")

# None（何もない状態。GASのnullに相当）
data = None
print(f"data = {data}, 型: {type(data)}")

# リスト（配列に相当）
fruits = ["りんご", "みかん", "ぶどう"]
print(f"fruits = {fruits}, 型: {type(fruits)}")

# 辞書（オブジェクトに相当）
person = {"name": "田中", "age": 25}
print(f"person = {person}, 型: {type(person)}")
```

**実行結果：**
```
age = 25, 型: <class 'int'>
price = 1980.5, 型: <class 'float'>
name = 田中太郎, 型: <class 'str'>
is_active = True, 型: <class 'bool'>
data = None, 型: <class 'NoneType'>
fruits = ['りんご', 'みかん', 'ぶどう'], 型: <class 'list'>
person = {'name': '田中', 'age': 25}, 型: <class 'dict'>
```

### データ型の対応表

| 概念 | GAS (JavaScript) | Python |
|------|-----------------|--------|
| 整数 | `number` | `int` |
| 小数 | `number` | `float` |
| 文字列 | `string` | `str` |
| 真偽値 | `boolean` | `bool` |
| 空値 | `null`, `undefined` | `None` |
| 配列 | `Array` | `list` |
| オブジェクト | `Object` | `dict` |

### type()関数

`type(変数)` で変数の型を確認できます。デバッグに便利です。

```python
# 型を確認する
x = 100
print(type(x))  # <class 'int'>

x = "文字列に変更"
print(type(x))  # <class 'str'>
```

**実行結果：**
```
<class 'int'>
<class 'str'>
```

> **GASとの違い**
> GASでは `typeof x` で型を確認しますが、Pythonでは `type(x)` を使います。

---

## Step 2: 型変換を使いこなす

異なる型を変換する方法を学びます。

```python
# ===== 型変換 =====

# 文字列 → 整数
num_str = "123"
num = int(num_str)
print(f"int('123') = {num}, 型: {type(num)}")

# 文字列 → 浮動小数点
price_str = "1980.5"
price = float(price_str)
print(f"float('1980.5') = {price}, 型: {type(price)}")

# 数値 → 文字列
age = 25
age_str = str(age)
print(f"str(25) = '{age_str}', 型: {type(age_str)}")

# 整数 → 浮動小数点
x = 10
x_float = float(x)
print(f"float(10) = {x_float}, 型: {type(x_float)}")

# 浮動小数点 → 整数（小数点以下切り捨て）
y = 3.7
y_int = int(y)
print(f"int(3.7) = {y_int}, 型: {type(y_int)}")
```

**実行結果：**
```
int('123') = 123, 型: <class 'int'>
float('1980.5') = 1980.5, 型: <class 'float'>
str(25) = '25', 型: <class 'str'>
float(10) = 10.0, 型: <class 'float'>
int(3.7) = 3, 型: <class 'int'>
```

### 型変換の対応表

| 変換 | GAS | Python |
|------|-----|--------|
| 文字列→整数 | `parseInt("123")` | `int("123")` |
| 文字列→小数 | `parseFloat("1.5")` | `float("1.5")` |
| 数値→文字列 | `String(123)` | `str(123)` |

### よくあるエラー：型変換の失敗

```python
# 数値に変換できない文字列
try:
    num = int("abc")
except ValueError as e:
    print(f"エラー: {e}")

# 正しく変換できる文字列
num = int("123")
print(f"成功: {num}")
```

**実行結果：**
```
エラー: invalid literal for int() with base 10: 'abc'
成功: 123
```

---

## Step 3: リストの操作をマスターする

リストはPythonで最もよく使うデータ構造です。

### 基本操作

```python
# ===== リストの基本操作 =====

# リストの作成
fruits = ["りんご", "みかん", "ぶどう"]
print(f"元のリスト: {fruits}")

# 要素へのアクセス
print(f"fruits[0]: {fruits[0]}")      # 最初の要素
print(f"fruits[-1]: {fruits[-1]}")    # 最後の要素

# 要素の追加
fruits.append("いちご")
print(f"append後: {fruits}")

# 特定位置に挿入
fruits.insert(1, "メロン")
print(f"insert後: {fruits}")

# 要素の削除（値を指定）
fruits.remove("みかん")
print(f"remove後: {fruits}")

# 要素の削除（インデックスを指定）
del fruits[0]
print(f"del後: {fruits}")

# 最後の要素を取り出して削除
last = fruits.pop()
print(f"pop()で取り出し: {last}")
print(f"pop後: {fruits}")
```

**実行結果：**
```
元のリスト: ['りんご', 'みかん', 'ぶどう']
fruits[0]: りんご
fruits[-1]: ぶどう
append後: ['りんご', 'みかん', 'ぶどう', 'いちご']
insert後: ['りんご', 'メロン', 'みかん', 'ぶどう', 'いちご']
remove後: ['りんご', 'メロン', 'ぶどう', 'いちご']
del後: ['メロン', 'ぶどう', 'いちご']
pop()で取り出し: いちご
pop後: ['メロン', 'ぶどう']
```

### スライス（GASにはない便利機能）

```python
# ===== スライス =====

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"元のリスト: {numbers}")

# [開始:終了] - 開始から終了未満
print(f"numbers[2:5]: {numbers[2:5]}")    # [2, 3, 4]

# [:終了] - 最初から終了未満
print(f"numbers[:3]: {numbers[:3]}")       # [0, 1, 2]

# [開始:] - 開始から最後まで
print(f"numbers[7:]: {numbers[7:]}")       # [7, 8, 9]

# [開始:終了:間隔]
print(f"numbers[::2]: {numbers[::2]}")     # [0, 2, 4, 6, 8]（偶数インデックス）
print(f"numbers[1::2]: {numbers[1::2]}")   # [1, 3, 5, 7, 9]（奇数インデックス）

# 逆順
print(f"numbers[::-1]: {numbers[::-1]}")   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

**実行結果：**
```
元のリスト: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
numbers[2:5]: [2, 3, 4]
numbers[:3]: [0, 1, 2]
numbers[7:]: [7, 8, 9]
numbers[::2]: [0, 2, 4, 6, 8]
numbers[1::2]: [1, 3, 5, 7, 9]
numbers[::-1]: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

### 便利なリスト関数

```python
# ===== 便利なリスト関数 =====

numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

print(f"元のリスト: {numbers}")
print(f"len(): {len(numbers)}")      # 要素数
print(f"sum(): {sum(numbers)}")      # 合計
print(f"max(): {max(numbers)}")      # 最大値
print(f"min(): {min(numbers)}")      # 最小値

# ソート（新しいリストを作成）
sorted_numbers = sorted(numbers)
print(f"sorted(): {sorted_numbers}")
print(f"元のリスト: {numbers}")  # 元は変わらない

# ソート（元のリストを変更）
numbers.sort()
print(f"sort()後: {numbers}")

# 要素の存在確認
print(f"5 in numbers: {5 in numbers}")  # True
print(f"99 in numbers: {99 in numbers}")  # False

# 要素の出現回数
print(f"numbers.count(5): {numbers.count(5)}")

# 要素のインデックス
print(f"numbers.index(9): {numbers.index(9)}")
```

**実行結果：**
```
元のリスト: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
len(): 10
sum(): 39
max(): 9
min(): 1
sorted(): [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
元のリスト: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
sort()後: [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
5 in numbers: True
99 in numbers: False
numbers.count(5): 2
numbers.index(9): 9
```

---

## Step 4: 辞書の操作をマスターする

辞書はキーと値のペアでデータを管理します。

```python
# ===== 辞書の基本操作 =====

# 辞書の作成
person = {
    "name": "田中太郎",
    "age": 25,
    "department": "営業部"
}
print(f"元の辞書: {person}")

# 値へのアクセス
print(f"person['name']: {person['name']}")

# 値の変更
person["age"] = 26
print(f"age変更後: {person}")

# 新しいキーの追加
person["email"] = "tanaka@example.com"
print(f"email追加後: {person}")

# キーの削除
del person["department"]
print(f"department削除後: {person}")

# キーの存在確認
print(f"'name' in person: {'name' in person}")
print(f"'salary' in person: {'salary' in person}")

# 安全に値を取得（キーがなくてもエラーにならない）
salary = person.get("salary", 0)  # キーがなければ0を返す
print(f"person.get('salary', 0): {salary}")
```

**実行結果：**
```
元の辞書: {'name': '田中太郎', 'age': 25, 'department': '営業部'}
person['name']: 田中太郎
age変更後: {'name': '田中太郎', 'age': 26, 'department': '営業部'}
email追加後: {'name': '田中太郎', 'age': 26, 'department': '営業部', 'email': 'tanaka@example.com'}
department削除後: {'name': '田中太郎', 'age': 26, 'email': 'tanaka@example.com'}
'name' in person: True
'salary' in person: False
person.get('salary', 0): 0
```

### 辞書のループ

```python
# ===== 辞書のループ =====

person = {
    "name": "田中太郎",
    "age": 25,
    "department": "営業部"
}

# キーだけを取得
print("=== キーだけ ===")
for key in person.keys():
    print(key)

# 値だけを取得
print("\n=== 値だけ ===")
for value in person.values():
    print(value)

# キーと値のペアを取得（最もよく使う）
print("\n=== キーと値のペア ===")
for key, value in person.items():
    print(f"{key}: {value}")
```

**実行結果：**
```
=== キーだけ ===
name
age
department

=== 値だけ ===
田中太郎
25
営業部

=== キーと値のペア ===
name: 田中太郎
age: 25
department: 営業部
```

---

## Step 5: リスト内包表記（Python独自の強力機能）

GASにはない、Pythonの強力な機能を学びましょう。

### 通常の書き方 vs リスト内包表記

```python
# ===== 通常の書き方 =====
numbers = [1, 2, 3, 4, 5]
doubled = []

for n in numbers:
    doubled.append(n * 2)

print(f"通常の書き方: {doubled}")

# ===== リスト内包表記 =====
numbers = [1, 2, 3, 4, 5]
doubled = [n * 2 for n in numbers]  # 1行で書ける！

print(f"リスト内包表記: {doubled}")
```

**実行結果：**
```
通常の書き方: [2, 4, 6, 8, 10]
リスト内包表記: [2, 4, 6, 8, 10]
```

### リスト内包表記の構文

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  [式 for 変数 in イテラブル]                                │
│                                                              │
│  例: [n * 2 for n in numbers]                               │
│       ↑       ↑         ↑                                  │
│     各要素に  変数名    元のリスト                          │
│     適用する式                                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 条件付きリスト内包表記

```python
# ===== 条件付き =====
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 偶数だけを抽出
evens = [n for n in numbers if n % 2 == 0]
print(f"偶数: {evens}")

# 5より大きい数を2倍
result = [n * 2 for n in numbers if n > 5]
print(f"5より大きい数を2倍: {result}")
```

**実行結果：**
```
偶数: [2, 4, 6, 8, 10]
5より大きい数を2倍: [12, 14, 16, 18, 20]
```

### 実践例：売上データの加工

```python
# ===== 実践例 =====

# 売上データ（辞書のリスト）
sales = [
    {"item": "商品A", "price": 1000},
    {"item": "商品B", "price": 2000},
    {"item": "商品C", "price": 1500},
    {"item": "商品D", "price": 3000},
]

# 価格だけのリストを抽出
prices = [s["price"] for s in sales]
print(f"価格リスト: {prices}")
print(f"合計: {sum(prices)}")

# 2000円以上の商品名だけ抽出
expensive_items = [s["item"] for s in sales if s["price"] >= 2000]
print(f"2000円以上の商品: {expensive_items}")

# 税込価格を追加した新しいリストを作成
sales_with_tax = [
    {**s, "price_with_tax": int(s["price"] * 1.1)}
    for s in sales
]
print(f"税込価格追加: {sales_with_tax}")
```

**実行結果：**
```
価格リスト: [1000, 2000, 1500, 3000]
合計: 7500
2000円以上の商品: ['商品B', '商品D']
税込価格追加: [{'item': '商品A', 'price': 1000, 'price_with_tax': 1100}, {'item': '商品B', 'price': 2000, 'price_with_tax': 2200}, {'item': '商品C', 'price': 1500, 'price_with_tax': 1650}, {'item': '商品D', 'price': 3000, 'price_with_tax': 3300}]
```

---

## Step 6: よくあるエラーと対処法

### エラー1: NameError（変数が未定義）

```python
# エラーが出るコード
print(undefined_variable)
```

**エラーメッセージ：**
```
NameError: name 'undefined_variable' is not defined
```

**原因と対処法：**
- 変数を使う前に定義していない
- 変数名のスペルミス
- 定義しているセルを実行していない

```python
# 正しいコード
defined_variable = "Hello"
print(defined_variable)
```

### エラー2: TypeError（型の不一致）

```python
# エラーが出るコード
result = "年齢: " + 25
```

**エラーメッセージ：**
```
TypeError: can only concatenate str (not "int") to str
```

**原因と対処法：**
- 文字列と数値を `+` で連結しようとした

```python
# 正しいコード
result = "年齢: " + str(25)  # str()で変換
# または
result = f"年齢: {25}"       # f文字列を使う（推奨）
```

### エラー3: IndexError（インデックスが範囲外）

```python
# エラーが出るコード
fruits = ["りんご", "みかん", "ぶどう"]
print(fruits[5])  # インデックス5は存在しない
```

**エラーメッセージ：**
```
IndexError: list index out of range
```

**原因と対処法：**
- リストの範囲外のインデックスを指定した
- リストの長さを確認してからアクセスする

```python
# 正しいコード
fruits = ["りんご", "みかん", "ぶどう"]
if len(fruits) > 5:
    print(fruits[5])
else:
    print("インデックス5は存在しません")
```

### エラー4: KeyError（辞書のキーが存在しない）

```python
# エラーが出るコード
person = {"name": "田中", "age": 25}
print(person["salary"])  # salaryキーは存在しない
```

**エラーメッセージ：**
```
KeyError: 'salary'
```

**原因と対処法：**
- 存在しないキーにアクセスした
- `get()` メソッドを使う

```python
# 正しいコード
person = {"name": "田中", "age": 25}

# 方法1: get()を使う（存在しなければNoneを返す）
salary = person.get("salary")
print(salary)  # None

# 方法2: get()でデフォルト値を指定
salary = person.get("salary", 0)
print(salary)  # 0

# 方法3: 存在確認してからアクセス
if "salary" in person:
    print(person["salary"])
else:
    print("salaryキーは存在しません")
```

### エラー5: IndentationError（インデントが不正）

```python
# エラーが出るコード
if True:
print("Hello")  # インデントがない！
```

**エラーメッセージ：**
```
IndentationError: expected an indented block after 'if' statement on line 1
```

**原因と対処法：**
- `if`, `for`, `def` などの後にインデントがない
- 4スペースでインデントする

```python
# 正しいコード
if True:
    print("Hello")  # 4スペースでインデント
```

---

## 練習問題

### 問題1: リスト操作

以下の処理を行ってください：
1. `[10, 20, 30, 40, 50]` というリストを作成
2. 末尾に `60` を追加
3. 先頭の要素を削除
4. 結果を表示

<details>
<summary>解答例</summary>

```python
numbers = [10, 20, 30, 40, 50]
numbers.append(60)
del numbers[0]
print(numbers)  # [20, 30, 40, 50, 60]
```

</details>

### 問題2: 辞書操作

以下の社員情報を辞書で作成し、メールアドレスを追加してから全情報を表示してください：
- 名前: 佐藤花子
- 年齢: 30
- 部署: 開発部

<details>
<summary>解答例</summary>

```python
employee = {
    "name": "佐藤花子",
    "age": 30,
    "department": "開発部"
}
employee["email"] = "sato@example.com"

for key, value in employee.items():
    print(f"{key}: {value}")
```

**実行結果：**
```
name: 佐藤花子
age: 30
department: 開発部
email: sato@example.com
```

</details>

### 問題3: リスト内包表記

`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` から奇数だけを抽出し、それぞれを3倍したリストを作成してください。

<details>
<summary>解答例</summary>

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = [n * 3 for n in numbers if n % 2 == 1]
print(result)  # [3, 9, 15, 21, 27]
```

</details>

---

## この節のまとめ

- Pythonの主要なデータ型：`int`, `float`, `str`, `bool`, `None`, `list`, `dict`
- `type()` で変数の型を確認できる
- 型変換：`int()`, `float()`, `str()`
- リスト操作：`append()`, `insert()`, `remove()`, `pop()`, スライス
- 辞書操作：`[]` でアクセス、`get()` で安全にアクセス、`items()` でループ
- リスト内包表記：`[式 for 変数 in リスト if 条件]`
- エラーメッセージを読んで、原因を特定する習慣をつける

**次の節では、AIを活用した学習方法を学びます。わからないことはAIに聞けば解決できます！**
