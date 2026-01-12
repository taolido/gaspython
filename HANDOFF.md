# Claude Code 引き継ぎプロンプト

以下をClaude Codeに貼り付けてください。

---

## プロジェクト概要

Python講座「挫折しない・壊さないPython入門 ─ AIと一緒に学ぶ、GASの次のステップ」の企画ドキュメント一式です。

添付のzipファイルを解凍して、GitHubリポジトリ `https://github.com/taolido/gaspython` にプッシュしてください。

## ファイル構成

```
gaspython/
├── README.md                    # プロジェクト概要
├── docs/
│   ├── 00_course_overview.md    # 講座全体設計
│   ├── 01_curriculum.md         # カリキュラム詳細（6章構成）
│   ├── 02_sources.md            # 情報源マッピング
│   └── 03_differentiation.md    # 差別化ポイント
└── research/
    ├── frustration_points.md    # Python挫折ポイント調査
    ├── gas_python_comparison.md # GAS vs Python比較
    └── gas_python_integration.md # GAS×Python連携方法
```

## 完了済みタスク

- [x] GAS講座成功要因の分析
- [x] 講座コンセプト策定（4本柱）
- [x] 6章構成カリキュラム設計
- [x] 情報源リサーチ（全章分）
- [x] GAS vs Python比較
- [x] GAS×Python連携方法調査
- [x] 差別化ポイント整理
- [x] OS対応方針決定（Windows優先、Mac補足）

## 次のタスク（優先度順）

### 優先度A（必須）
1. GitHubへのプッシュ
2. 各章の詳細設計（節ごとの学習目標・演習課題）

### 優先度B（推奨）
3. 第2章「AI活用メソッド」の具体化
4. サンプルコンテンツ作成（特定章を実際に書く）

### 優先度C（検討）
5. 講座形式の検討（テキスト/動画/ハンズオン比率）
6. 料金設定・販売戦略

## 主要な決定事項

| 項目 | 決定内容 |
|------|----------|
| タイトル | 「挫折しない・壊さないPython入門」 |
| 4本柱 | 環境構築で挫折させない / AI学習パートナー / 早期成果 / 壊さない作法 |
| 環境 | 第1-3章 Colab → 第4-5章 ローカル |
| OS | Windows優先、Mac補足 |
| 環境管理 | venv必須、Anaconda非推奨 |
| 主要情報源 | Python-izm（第1・3章）、gspread系記事（第5章） |

## プッシュコマンド

zipは既にgit初期化・コミット済みなので：

```bash
cd gaspython
git remote add origin https://github.com/taolido/gaspython.git
git push -u origin main
```

---
