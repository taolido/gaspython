# 第1章：環境構築ゼロで始める - Google Colabで即スタート

## このパートで学ぶこと

- Google Colabで即座にPythonを実行する
- GASとPythonの文法の違いを理解する
- Python基本文法を習得する
- なぜ「環境構築を後回し」にするのかを理解する

---

## 1-1. Google Colabを開いて3分でHello World

### Google Colabとは

**Google Colaboratory（Colab）** は、Googleが無料で提供するクラウド上のPython実行環境です。

GAS経験者のあなたには、こう説明すると分かりやすいでしょう：

> **Colabは「PythonのためのGASエディタ」**

GASがブラウザだけでJavaScriptを書いて実行できたように、ColabはブラウザだけでPythonを書いて実行できます。

### GASとColabの比較

| 項目 | GAS | Colab |
|------|-----|-------|
| 言語 | JavaScript | Python |
| 実行環境 | Googleのサーバー | Googleのサーバー |
| 必要なもの | Googleアカウント | Googleアカウント |
| 環境構築 | 不要 | 不要 |
| 保存先 | Googleドライブ | Googleドライブ |
| 実行単位 | 関数 | セル |

### Colabを開く

1. ブラウザで [https://colab.research.google.com/](https://colab.research.google.com/) にアクセス
2. Googleアカウントでログイン
3. 「ノートブックを新規作成」をクリック

以上！これだけでPythonを書く準備が整いました。

### ノートブックの構成

Colabの画面は「セル」で構成されています。

```
┌─────────────────────────────────────────────────────┐
│ [ファイル名.ipynb]                                    │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────┐ │
│ │ [▶] print("Hello World!")                       │ │ ← コードセル
│ └─────────────────────────────────────────────────┘ │
│                                                      │
│ ┌─────────────────────────────────────────────────┐ │
│ │ # これはメモです                                   │ │ ← テキストセル
│ └─────────────────────────────────────────────────┘ │
│                                                      │
│ ┌─────────────────────────────────────────────────┐ │
│ │ [▶] x = 10                                       │ │ ← コードセル
│ │     print(x * 2)                                 │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

| 要素 | 説明 |
|------|------|
| コードセル | Pythonコードを書いて実行する |
| テキストセル | メモや説明を書く（Markdown形式） |
| [▶]ボタン | セルを実行（Shift+Enterでも可） |

### 最初のプログラム

コードセルに以下を入力して、[▶]ボタンをクリック（またはShift+Enter）：

```python
print("Hello World!")
```

**出力:**
```
Hello World!
```

おめでとうございます！Pythonプログラムを実行できました。

### GASとの違い：関数を書かなくていい

**GASの場合:**
```javascript
function myFunction() {
  console.log("Hello World!");
}
// 関数を選んで実行ボタンを押す
```

**Pythonの場合:**
```python
print("Hello World!")
# そのまま実行できる
```

Pythonでは、関数で囲まなくてもコードを直接実行できます。これが「スクリプト言語」の特徴です。

---

## 1-2. なぜColabから始めるのか

### 環境構築の壁

Pythonを始めようとして、こんな経験はありませんか？

```
「Pythonを始めよう！」
    ↓
「まずインストール...」
    ↓
「PATHの設定？」
    ↓
「pip? venv? Anaconda?」
    ↓
「エラーが出る...」
    ↓
「もういいや...」 ← 挫折
```

この「環境構築の壁」で9割の人が挫折します。

### Colabなら壊しようがない

Colabの最大のメリットは**「壊しようがない」**ことです。

| 状況 | ローカル環境 | Colab |
|------|------------|-------|
| 変なライブラリを入れた | 環境が壊れる | セッション終了でリセット |
| Pythonのバージョン問題 | 複雑な対応が必要 | Googleが管理 |
| PCを変えた | 再セットアップ | ブラウザで即アクセス |

### GASと同じ「クラウドの安心感」

GASを使っていて、環境構築で困ったことはありましたか？なかったはずです。

それは、GASがGoogleのサーバーで動いているからです。Colabも同じです。

> **ローカル環境は「必要になったら」で大丈夫**
>
> - exe化して配布したい → 第4章で学ぶ
> - 定期実行したい → 第4章で学ぶ
> - 大量データを処理したい → まずColabで試す

---

## 1-3. GAS経験者向け：文法比較チートシート

GASはJavaScriptベースなので、Pythonとは文法が異なります。でも安心してください。概念は同じで、書き方が違うだけです。

### 変数宣言

**GAS (JavaScript):**
```javascript
let name = "田中太郎";
const TAX_RATE = 0.1;
var oldStyle = "古い書き方";  // 非推奨
```

**Python:**
```python
name = "田中太郎"
TAX_RATE = 0.1  # 慣習的に大文字で定数を表現
# let/const/var は不要！
```

> **ポイント**: Pythonでは変数宣言のキーワードが不要です。いきなり`変数名 = 値`で書けます。

### 文字列

**GAS:**
```javascript
const name = "田中";
const message = `こんにちは、${name}さん`;  // テンプレートリテラル
```

**Python:**
```python
name = "田中"
message = f"こんにちは、{name}さん"  # f文字列（f-string）
```

> **ポイント**: Pythonの`f""`はGASのテンプレートリテラル（バッククォート）に相当します。

### 出力

**GAS:**
```javascript
console.log("Hello");
Logger.log("Hello");
```

**Python:**
```python
print("Hello")
```

### 条件分岐

**GAS:**
```javascript
if (score >= 80) {
  console.log("合格");
} else if (score >= 60) {
  console.log("追試");
} else {
  console.log("不合格");
}
```

**Python:**
```python
if score >= 80:
    print("合格")
elif score >= 60:
    print("追試")
else:
    print("不合格")
```

> **重要な違い:**
> - `{}` が不要、代わりに**インデント（字下げ）**で範囲を示す
> - `else if` → `elif`
> - 条件の後に `:` が必要

### 配列（リスト）

**GAS:**
```javascript
const fruits = ["りんご", "みかん", "ぶどう"];
fruits.push("いちご");           // 追加
console.log(fruits[0]);          // りんご
console.log(fruits.length);      // 4
```

**Python:**
```python
fruits = ["りんご", "みかん", "ぶどう"]
fruits.append("いちご")          # 追加
print(fruits[0])                 # りんご
print(len(fruits))               # 4
```

> **違い:**
> - `push()` → `append()`
> - `.length` → `len()`

### オブジェクト（辞書）

**GAS:**
```javascript
const person = {
  name: "田中太郎",
  age: 25,
  department: "営業部"
};
console.log(person.name);
console.log(person["age"]);
```

**Python:**
```python
person = {
    "name": "田中太郎",
    "age": 25,
    "department": "営業部"
}
print(person["name"])
# person.name は使えない（辞書の場合）
```

> **違い:** Pythonの辞書ではキーを必ずクォートで囲み、アクセスは`[]`で行います。

### 繰り返し（for文）

**GAS:**
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

**Python:**
```python
# リストのループ
fruits = ["りんご", "みかん", "ぶどう"]
for fruit in fruits:
    print(fruit)

# 回数指定のループ
for i in range(5):
    print(i)
```

> **違い:**
> - `for...of` → `for...in`
> - `for (let i = 0; i < 5; i++)` → `for i in range(5)`

### 関数定義

**GAS:**
```javascript
function greet(name) {
  return `こんにちは、${name}さん`;
}

// アロー関数
const add = (a, b) => a + b;
```

**Python:**
```python
def greet(name):
    return f"こんにちは、{name}さん"

# ラムダ式（アロー関数に相当）
add = lambda a, b: a + b
```

> **違い:** `function` → `def`

### 文法比較チートシート（まとめ）

| 項目 | GAS (JavaScript) | Python |
|------|-----------------|--------|
| 変数宣言 | `let x = 10` | `x = 10` |
| 定数 | `const X = 10` | `X = 10`（慣習） |
| 文字列結合 | `` `Hello ${name}` `` | `f"Hello {name}"` |
| 出力 | `console.log()` | `print()` |
| 条件分岐 | `if () {}` | `if :` + インデント |
| else if | `else if` | `elif` |
| 配列/リスト | `[]`, `.push()` | `[]`, `.append()` |
| 配列の長さ | `.length` | `len()` |
| オブジェクト/辞書 | `{key: value}` | `{"key": value}` |
| for (配列) | `for (x of arr)` | `for x in arr:` |
| for (回数) | `for (let i=0; i<n; i++)` | `for i in range(n):` |
| 関数定義 | `function f() {}` | `def f():` |
| 文末セミコロン | 必須（推奨） | 不要 |
| ブロック | `{}` | インデント |
| コメント | `//` または `/* */` | `#` |

---

## 1-4. Python基礎文法

GASとの比較を踏まえて、Python固有の文法を学びましょう。

### インデントの重要性

Pythonでは**インデント（字下げ）**がプログラムの構造を決めます。

```python
# 正しい
if score >= 60:
    print("合格")      # 4スペースでインデント
    print("おめでとう")  # 同じブロック内

# 間違い（IndentationError）
if score >= 60:
print("合格")  # インデントがない！
```

> **GASとの違い**
> GASでは`{}`でブロックを示すので、インデントは見た目だけの問題でした。
> Pythonではインデントが文法的に意味を持ちます。

### データ型

```python
# 整数（int）
age = 25
print(type(age))  # <class 'int'>

# 浮動小数点数（float）
price = 1980.5
print(type(price))  # <class 'float'>

# 文字列（str）
name = "田中太郎"
print(type(name))  # <class 'str'>

# 真偽値（bool）
is_active = True   # GASと同じ
is_deleted = False
print(type(is_active))  # <class 'bool'>

# None（JavaScriptのnullに相当）
data = None
```

### 型変換

```python
# 文字列 → 整数
num_str = "123"
num = int(num_str)
print(num + 1)  # 124

# 整数 → 文字列
age = 25
message = "年齢は" + str(age) + "歳です"
# または f文字列を使う（推奨）
message = f"年齢は{age}歳です"

# 文字列 → 浮動小数点
price_str = "1980.5"
price = float(price_str)
```

### リストの操作

```python
# リストの作成
fruits = ["りんご", "みかん", "ぶどう"]

# 要素へのアクセス
print(fruits[0])   # りんご
print(fruits[-1])  # ぶどう（末尾）

# スライス（GASにはない便利機能！）
print(fruits[0:2])  # ['りんご', 'みかん']
print(fruits[1:])   # ['みかん', 'ぶどう']
print(fruits[:2])   # ['りんご', 'みかん']

# 要素の追加
fruits.append("いちご")

# 要素の削除
fruits.remove("みかん")  # 値を指定
del fruits[0]            # インデックスを指定

# リストの結合
more_fruits = ["メロン", "スイカ"]
all_fruits = fruits + more_fruits
```

### 辞書の操作

```python
# 辞書の作成
person = {
    "name": "田中太郎",
    "age": 25,
    "department": "営業部"
}

# 値へのアクセス
print(person["name"])  # 田中太郎

# 値の変更
person["age"] = 26

# キーの追加
person["email"] = "tanaka@example.com"

# キーの存在確認
if "name" in person:
    print("nameキーがあります")

# 全キーを取得
print(person.keys())    # dict_keys(['name', 'age', ...])

# 全値を取得
print(person.values())  # dict_values(['田中太郎', 26, ...])

# キーと値のペアを取得
for key, value in person.items():
    print(f"{key}: {value}")
```

### リスト内包表記（GASにはない便利機能！）

```python
# 通常の書き方
numbers = [1, 2, 3, 4, 5]
doubled = []
for n in numbers:
    doubled.append(n * 2)

# リスト内包表記（Pythonらしい書き方）
doubled = [n * 2 for n in numbers]
print(doubled)  # [2, 4, 6, 8, 10]

# 条件付き
evens = [n for n in numbers if n % 2 == 0]
print(evens)  # [2, 4]
```

---

## 1-5. 【AIプロンプト】基礎文法で迷ったら聞くフレーズ集

### GASからの変換

```
GASでは以下のように書きますが、Pythonではどう書きますか？

[GASのコードを貼り付け]
```

### 書き方の確認

```
Pythonで「〇〇」をするには、どのように書きますか？
簡単な例を示してください。
```

### エラーの解決

```
Pythonで以下のエラーが出ました。原因と解決策を教えてください。

【エラーメッセージ】
[エラーメッセージを貼り付け]

【実行したコード】
[コードを貼り付け]
```

### コードの理解

```
以下のPythonコードを1行ずつ説明してください。
特に [わからない部分] が理解できません。

[コードを貼り付け]
```

### 実践例

```
【質問】
GASでは配列の末尾に要素を追加するとき fruits.push("いちご") と書きますが、
Pythonではどう書きますか？

【AIの回答例】
Pythonでは `append()` メソッドを使います。

fruits = ["りんご", "みかん"]
fruits.append("いちご")
print(fruits)  # ['りんご', 'みかん', 'いちご']
```

---

## 1-6. ローカル環境は「必要になったら」でOK

### 今はColabで十分

第1〜3章で学ぶ内容は、すべてColabで実行できます。

```
第1章：基礎文法 → Colabで十分
第2章：AI活用 → Colabで十分
第3章：Excel処理 → Colabで十分
第4章：ローカル環境 → ここで初めて必要に
第5章：GAS連携 → 両方使う
```

### ローカル環境が必要になるとき

| やりたいこと | 理由 |
|-------------|------|
| exe化して配布 | Colabではexe作成不可 |
| 定期実行（毎日自動実行） | Colabはセッションが切れる |
| 大量ファイルの処理 | アップロードが面倒 |
| 機密データの処理 | Googleに送りたくない |

### 焦らなくていい理由

1. **Colabで基礎を固める** - 環境トラブルなしで学習に集中
2. **「動く喜び」を先に体験** - モチベーション維持
3. **第4章で丁寧に解説** - 「壊さない」作法を学んでから

> **GASのときを思い出してください**
> GASを始めるとき、「Node.jsをインストールして...」なんてやりませんでしたよね？
> ブラウザで即座に書いて動かせたから、学習が続いたはずです。
> Pythonも同じアプローチで始めましょう。

---

## このパートのまとめ

このパートで学んだことを確認しましょう。

- [ ] Google Colabでノートブックを作成できる
- [ ] コードセルでPythonを実行できる
- [ ] GASとPythonの文法の違いを理解した
- [ ] 変数、リスト、辞書の基本操作ができる
- [ ] for文、if文を書ける
- [ ] インデントの重要性を理解した

### GASとの違いのポイント

| 項目 | GAS | Python |
|------|-----|--------|
| ブロックの表現 | `{}` | インデント |
| 変数宣言 | `let`/`const` | 不要 |
| 文末 | `;` | 不要 |
| else if | `else if` | `elif` |
| 配列への追加 | `.push()` | `.append()` |
| 文字列結合 | バッククォート | f文字列 |

---

## 練習問題

### 問題1：Hello World

自分の名前を表示するプログラムを書いてください。

### 問題2：文法変換

以下のGASコードをPythonに変換してください。

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

### 問題3：辞書の操作

以下の社員情報を辞書で作成し、全項目を表示してください。
- 名前: 田中太郎
- 年齢: 25
- 部署: 営業部

<details>
<summary>解答例</summary>

```python
# 問題1
name = "田中太郎"  # 自分の名前に変更
print(f"こんにちは、{name}さん！")

# 問題2
prices = [100, 200, 300, 400, 500]
total = 0

for price in prices:
    total += price

print(f"合計: {total}円")

# または、Pythonらしく
prices = [100, 200, 300, 400, 500]
total = sum(prices)  # sum()関数で一発
print(f"合計: {total}円")

# 問題3
employee = {
    "name": "田中太郎",
    "age": 25,
    "department": "営業部"
}

for key, value in employee.items():
    print(f"{key}: {value}")

# または
print(f"名前: {employee['name']}")
print(f"年齢: {employee['age']}")
print(f"部署: {employee['department']}")
```

</details>

---

## 次のパートへ

お疲れさまでした！Colabでpythonを動かせるようになりました。

GASとPythonの違いを理解し、基本的な文法を習得できたと思います。

次のパートでは、**AIを「プログラミング家庭教師」にする方法**を学びます。

- AIへの効果的な質問の仕方
- エラーが出たときの対処法
- 「なぜそうなるか」を理解するサイクル

AIをパートナーにすれば、学習効率が劇的に上がります。一緒に学んでいきましょう！
