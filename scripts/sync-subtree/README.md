# Git サブツリー自動同期ツール

## 概要

このツールは、Git リポジトリがクリーンな状態の場合のみ、指定されたサブツリーディレクトリの自動 pull を実行します。

## 機能

- 作業ツリーのクリーン状態チェック（`git status --porcelain`）
- 未プッシュコミットの存在チェック（`git rev-list HEAD..@{u}`）
- 複数のサブツリーに対応した自動同期
- 設定ファイルによる同期対象の管理
- エラー時もプロセスを継続（ログ出力あり）

## 使用方法

### 基本的な実行

**重要:** `--root` 引数は必須です。同期対象のローカルリポジトリのルートディレクトリを指定してください。

```bash
python sync_subtree.py --root /path/to/your/repo
```

または短縮形：

```bash
python sync_subtree.py -r /path/to/your/repo
```

### コマンドライン引数

#### 必須引数

- `--root`, `-r`: ローカルリポジトリのルートディレクトリパス（必須）

#### オプション引数

- `--config`, `-c`: 設定ファイルのパス（デフォルト: `subtree_config.json`）

### 使用例

```bash
# 基本的な使用方法
python sync_subtree.py --root /home/user/my-project

# カスタム設定ファイルを指定
python sync_subtree.py --root /home/user/my-project --config custom_config.json

# Windows環境での例
python sync_subtree.py -r "C:\projects\my-repo"

# 相対パスでの指定
python sync_subtree.py -r ./my-project
```

### 実行条件

ツールは以下の条件をすべて満たす場合のみサブツリー同期を実行します：

1. カレントディレクトリが Git リポジトリである
2. 作業ツリーがクリーンである（未コミットの変更がない）
3. 未プッシュのコミットがない

### 設定ファイル

`subtree_config.json` ファイルで同期対象を設定できます。

**設定ファイルの例：**

```json
{
  "subtrees": [
    {
      "prefix": "clinerules",
      "repo_url": "https://github.com/your-org/clinerules.git",
      "branch": "main"
    },
    {
      "prefix": "shared-utils",
      "repo_url": "https://github.com/your-org/shared-utils.git",
      "branch": "develop"
    }
  ]
}
```

**設定項目：**

- `prefix`: サブツリーのプレフィックスパス
- `repo_url`: リモートリポジトリの URL
- `branch`: 同期するブランチ名

### 設定ファイルが存在しない場合

設定ファイルが存在しない場合、以下のデフォルト設定が使用されます：

```json
{
  "prefix": "clinerules",
  "repo_url": "https://github.com/your-org/clinerules.git",
  "branch": "main"
}
```

## 終了コード

- `0`: すべての処理が正常に完了
- `1`: スキップ（リポジトリがクリーンでない、未プッシュコミットがあるなど）
- `2`: エラー（一部の処理で失敗したが、継続した）
- `130`: ユーザーによる中断（Ctrl+C）

## ログ出力

ツールは以下の形式でログを出力します：

```
2026-01-29 20:30:00 [INFO] Git サブツリー自動同期を開始します
2026-01-29 20:30:01 [INFO] 1 個のサブツリー設定を読み込みました
2026-01-29 20:30:01 [INFO] サブツリー同期を開始: clinerules
2026-01-29 20:30:05 [INFO] サブツリー同期が完了しました
2026-01-29 20:30:05 [INFO] すべての処理が正常に完了しました
```

## スキップされるケース

以下の場合、同期はスキップされ、理由が表示されます：

### Git リポジトリでない

```
[WARNING] 現在のディレクトリは Git リポジトリではありません
```

### 作業ツリーがクリーンでない

```
[WARNING] 同期をスキップします: 作業ツリーに未コミットの変更があります
```

### 未プッシュのコミットがある

```
[WARNING] 同期をスキップします: 3 個の未プッシュコミットがあります
```

## エラーハンドリング

- Git コマンドの実行エラーはログに記録されますが、プロセスは継続します
- 設定ファイルの読み込みエラー時はデフォルト設定を使用します
- 個々のサブツリー同期が失敗しても、他のサブツリーの処理は継続されます

## CLI 起動前の自動実行

このツールは CLI の起動前に自動実行することを想定しています。

**例：スクリプトやエイリアスでの実行**

```bash
# bashrc や zshrc に追加
alias my-cli="python /path/to/sync_subtree.py --root /path/to/repo && my-cli-command"

# または、ラッパースクリプトを作成
# wrapper.sh
#!/bin/bash
python /path/to/sync_subtree.py --root "$HOME/projects/my-repo"
if [ $? -eq 0 ] || [ $? -eq 1 ]; then
    # 成功またはスキップの場合は続行
    my-cli-command "$@"
fi
```

**Windows PowerShell での例：**

```powershell
# プロファイルに追加
function My-CLI {
    python C:\path\to\sync_subtree.py --root "C:\projects\my-repo"
    if ($LASTEXITCODE -le 1) {
        my-cli-command $args
    }
}
```

## 注意事項

- Git コマンドのタイムアウトは 30 秒に設定されています
- リモートトラッキングブランチが設定されていない場合、未プッシュチェックはスキップされます
- サブツリーが存在しない場合、初回は `git subtree add` を手動で実行する必要があります

## トラブルシューティング

### サブツリー同期が失敗する

1. リモートリポジトリの URL が正しいか確認
2. ネットワーク接続を確認
3. Git の認証情報が正しく設定されているか確認

### 設定ファイルのエラー

JSON の構文エラーがないか確認してください。エラーの場合、デフォルト設定が使用されます。

## ライセンス

このツールは MIT ライセンスの下で提供されています。