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
**形式**: セクション分割版（7ファイル）

| ファイル | 内容 | 成果物 |
|---------|------|--------|
| `chapters/section_3-0_chapter_intro_v2.md` | 章のイントロ・完成イメージ | - |
| `chapters/section_3-1_openpyxl_v2.md` | openpyxl入門 | Excel読み書き |
| `chapters/section_3-2_pandas_v2.md` | pandas入門 | データ分析基礎 |
| `chapters/section_3-3_time_limit_v2.md` | GASの6分制限を超える | 大量データ処理 |
| `chapters/section_3-4_sales_report_v2.md` | **グラフ付き売上レポート** | レポート自動生成 |
| `chapters/section_3-5_excel_merge_v2.md` | **100枚Excel統合ツール** | 3秒で100ファイル統合 |
| `chapters/section_3-6_ai_prompts_v2.md` | AIプロンプトテンプレート | - |

**★ 第3章の目玉:**
- 「100枚のExcelを3秒で統合」
- 「グラフ付き売上レポート自動生成」

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

## サンプルデータ

```
content/samples/
├── sales_data_202401.xlsx       # 第3章: 売上データ（1月分）
├── sales_data_202402.xlsx       # 第3章: 売上データ（2月分）
├── sales_data_202403.xlsx       # 第3章: 売上データ（3月分）
├── employee_list.xlsx           # 社員名簿
├── product_master.xlsx          # 商品マスター
└── README.md                    # サンプルデータの説明
```

---

## ファイル命名規則

```
chapter[章番号]_[英語名]_v2.md     → 統合版（複数セクションを1ファイルに）
section_[章]-[節]_[英語名]_v2.md  → 分割版（セクションごとに1ファイル）
```
