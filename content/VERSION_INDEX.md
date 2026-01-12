# コンテンツバージョン管理

## 最新版ファイル一覧

すべての `_v2.md` ファイルが本番品質の最新版です。

---

## 第0章：はじめに
**形式**: 1ファイル統合版

| ファイル | 内容 |
|---------|------|
| `chapters/chapter00_introduction_v2.md` | 0-1〜0-4 全セクション統合 |

---

## 第1章：環境構築ゼロで始める
**形式**: セクション分割版

| ファイル | 内容 |
|---------|------|
| `chapters/section_1-1_colab_start_v2.md` | Colabで即スタート |
| `chapters/section_1-2_why_colab_v2.md` | なぜColabから始めるのか |
| `chapters/section_1-3_syntax_comparison_v2.md` | GAS vs Python 文法比較 |
| `chapters/section_1-4_python_basics_v2.md` | Python基礎文法 |
| `chapters/section_1-5_ai_prompts_v2.md` | AIプロンプトテンプレート |
| `chapters/section_1-6_local_later_v2.md` | ローカル環境は後でOK |

---

## 第2章：AIを学習パートナーに
**形式**: 1ファイル統合版

| ファイル | 内容 |
|---------|------|
| `chapters/chapter02_ai_partner_v2.md` | 2-1〜2-5 全セクション統合 |

---

## 第3章：Excel×Pythonで成果を出す
**形式**: セクション分割版

| ファイル | 内容 |
|---------|------|
| `chapters/section_3-1_openpyxl_v2.md` | openpyxl入門 |
| `chapters/section_3-2_pandas_v2.md` | pandas入門 |
| `chapters/section_3-3_time_limit_v2.md` | GASの6分制限を超える |
| `chapters/section_3-4_sales_system_v2.md` | 売上集計システム |
| `chapters/section_3-5_batch_processing_v2.md` | 複数ファイル一括処理 |
| `chapters/section_3-6_ai_prompts_v2.md` | AIプロンプトテンプレート |

---

## 第4章：ローカル環境への移行
**形式**: セクション分割版

| ファイル | 内容 |
|---------|------|
| `chapters/section_4-1_why_local_v2.md` | なぜローカル環境が必要か |
| `chapters/section_4-2_three_rules_v2.md` | 壊さないための鉄則3つ |
| `chapters/section_4-3_install_python_v2.md` | Pythonインストール |
| `chapters/section_4-4_venv_hands_on_v2.md` | venv実践ハンズオン |
| `chapters/section_4-5_troubleshooting_v2.md` | トラブルシューティング |
| `chapters/section_4-6_pyinstaller_v2.md` | PyInstallerでexe化 |
| `chapters/section_4-7_ai_prompts_v2.md` | AIプロンプトテンプレート |

---

## 第5章：GAS×Python連携
**形式**: セクション分割版

| ファイル | 内容 |
|---------|------|
| `chapters/section_5-1_when_to_use_v2.md` | GASとPythonの使い分け |
| `chapters/section_5-2_gspread_v2.md` | gspreadでスプレッドシート操作 |
| `chapters/section_5-3_gas_webapi_v2.md` | GAS WebAPI連携 |
| `chapters/section_5-4_next_steps_v2.md` | 次のステップへ |

---

## ファイル命名規則

```
chapter[章番号]_[英語名]_v2.md     → 統合版（複数セクションを1ファイルに）
section_[章]-[節]_[英語名]_v2.md  → 分割版（セクションごとに1ファイル）
```

## 削除済みファイル（旧版）

以下は本番品質版作成前のドラフトで、削除済み：
- ~~chapter01_colab_start.md~~
- ~~chapter03_excel_python.md~~

---

## 未作成（今後の課題）

### サンプルデータ
```
content/samples/
├── 社員名簿.xlsx          ← 未作成
├── 売上データ_1月.xlsx    ← 未作成
├── 売上データ_2月.xlsx    ← 未作成
└── ...
```

### 完成コード
```
content/code/
├── chapter03/
│   ├── excel_merge.py     ← 100枚Excel統合ツール
│   ├── sales_report.py    ← グラフ付きレポート生成
│   └── ...
└── chapter04/
    └── ...
```
