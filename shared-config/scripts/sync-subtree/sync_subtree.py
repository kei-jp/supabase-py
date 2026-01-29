#!/usr/bin/env python
"""
Git サブツリー自動同期ツール

Git リポジトリがクリーンな状態の場合のみ、
指定されたサブツリーディレクトリの自動 pull を実行する。
"""

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# デフォルト設定
DEFAULT_CONFIG_FILE = "subtree_config.json"
DEFAULT_SUBTREE_PREFIX = "clinerules"
DEFAULT_SUBTREE_REPO_URL = "https://github.com/your-org/clinerules.git"
DEFAULT_SUBTREE_BRANCH = "main"


def load_config(config_path: str = DEFAULT_CONFIG_FILE) -> list[dict]:
    """
    設定ファイルから同期対象のサブツリー情報を読み込む。
    
    Args:
        config_path: 設定ファイルのパス
    
    Returns:
        サブツリー設定のリスト
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        logger.info(f"設定ファイルが見つかりません: {config_path}")
        logger.info("デフォルト設定を使用します")
        return [{
            "prefix": DEFAULT_SUBTREE_PREFIX,
            "repo_url": DEFAULT_SUBTREE_REPO_URL,
            "branch": DEFAULT_SUBTREE_BRANCH
        }]
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        
        subtrees = config_data.get("subtrees", [])
        
        if not subtrees:
            logger.warning("設定ファイルにサブツリー情報がありません")
            logger.info("デフォルト設定を使用します")
            return [{
                "prefix": DEFAULT_SUBTREE_PREFIX,
                "repo_url": DEFAULT_SUBTREE_REPO_URL,
                "branch": DEFAULT_SUBTREE_BRANCH
            }]
        
        logger.info(f"{len(subtrees)} 個のサブツリー設定を読み込みました")
        return subtrees
    
    except json.JSONDecodeError as e:
        logger.error(f"設定ファイルの読み込みに失敗しました: {e}")
        logger.info("デフォルト設定を使用します")
        return [{
            "prefix": DEFAULT_SUBTREE_PREFIX,
            "repo_url": DEFAULT_SUBTREE_REPO_URL,
            "branch": DEFAULT_SUBTREE_BRANCH
        }]
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        logger.info("デフォルト設定を使用します")
        return [{
            "prefix": DEFAULT_SUBTREE_PREFIX,
            "repo_url": DEFAULT_SUBTREE_REPO_URL,
            "branch": DEFAULT_SUBTREE_BRANCH
        }]


def run_git_command(args: list[str]) -> tuple[bool, str, str]:
    """
    Git コマンドを実行し、結果を返す。
    
    Args:
        args: Git コマンド引数のリスト（git は含まない）
    
    Returns:
        (成功フラグ, stdout, stderr) のタプル
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        logger.error("Git コマンドがタイムアウトしました")
        return False, "", "Command timed out"
    except Exception as e:
        logger.error(f"Git コマンド実行中にエラーが発生しました: {e}")
        return False, "", str(e)


def is_git_repository() -> bool:
    """
    現在のディレクトリが Git リポジトリかどうかを確認する。
    
    Returns:
        Git リポジトリの場合 True
    """
    success, _, _ = run_git_command(["rev-parse", "--git-dir"])
    return success


def is_working_tree_clean() -> tuple[bool, Optional[str]]:
    """
    作業ツリーがクリーンかどうかを確認する。
    
    Returns:
        (クリーンかどうか, 理由メッセージ) のタプル
    """
    success, stdout, _ = run_git_command(["status", "--porcelain"])
    
    if not success:
        return False, "git status の実行に失敗しました"
    
    if stdout:
        return False, "作業ツリーに未コミットの変更があります"
    
    return True, None


def has_unpushed_commits() -> tuple[bool, Optional[str]]:
    """
    未プッシュのコミットがあるかどうかを確認する。
    
    Returns:
        (未プッシュコミットがあるかどうか, 理由メッセージ) のタプル
    """
    # まず、リモートトラッキングブランチが存在するか確認
    success, stdout, _ = run_git_command(["rev-parse", "--abbrev-ref", "@{u}"])
    
    if not success:
        # リモートトラッキングブランチが設定されていない場合はスキップ
        logger.info("リモートトラッキングブランチが設定されていません。未プッシュチェックをスキップします。")
        return False, None
    
    # 未プッシュコミットの確認
    success, stdout, _ = run_git_command(["rev-list", "HEAD..@{u}"])
    
    if not success:
        return False, "未プッシュコミットの確認に失敗しました"
    
    if stdout:
        commit_count = len(stdout.splitlines())
        return True, f"{commit_count} 個の未プッシュコミットがあります"
    
    return False, None


def sync_subtree(
    prefix: str,
    repo_url: str,
    branch: str
) -> bool:
    """
    指定されたサブツリーを同期する。
    
    Args:
        prefix: サブツリーのプレフィックスパス
        repo_url: リモートリポジトリの URL
        branch: 同期するブランチ名
    
    Returns:
        成功した場合 True
    """
    logger.info(f"サブツリー同期を開始: {prefix}")
    logger.info(f"リポジトリ: {repo_url}")
    logger.info(f"ブランチ: {branch}")
    
    success, stdout, stderr = run_git_command([
        "subtree",
        "pull",
        f"--prefix={prefix}",
        repo_url,
        branch,
        "--squash"
    ])
    
    if success:
        logger.info("サブツリー同期が完了しました")
        if stdout:
            logger.info(stdout)
        return True
    else:
        logger.error("サブツリー同期に失敗しました")
        if stderr:
            logger.error(stderr)
        return False


def main() -> int:
    """
    メイン処理。
    
    Returns:
        終了コード（0: 成功, 1: スキップ, 2: エラー）
    """
    logger.info("Git サブツリー自動同期を開始します")
    
    # Git リポジトリかどうか確認
    if not is_git_repository():
        logger.warning("現在のディレクトリは Git リポジトリではありません")
        return 1
    
    # 作業ツリーのクリーンチェック
    is_clean, reason = is_working_tree_clean()
    if not is_clean:
        logger.warning(f"同期をスキップします: {reason}")
        return 1
    
    # 未プッシュコミットのチェック
    has_unpushed, reason = has_unpushed_commits()
    if has_unpushed:
        logger.warning(f"同期をスキップします: {reason}")
        return 1
    
    # 設定ファイルから同期対象を読み込み
    subtree_configs = load_config()
    
    # サブツリー同期実行
    all_success = True
    for config in subtree_configs:
        prefix = config.get("prefix")
        repo_url = config.get("repo_url")
        branch = config.get("branch")
        
        if not all([prefix, repo_url, branch]):
            logger.error(f"不正な設定をスキップします: {config}")
            all_success = False
            continue
        
        # 型チェックを通過しているため、str として扱う
        success = sync_subtree(str(prefix), str(repo_url), str(branch))
        if not success:
            all_success = False
    
    if all_success:
        logger.info("すべての処理が正常に完了しました")
        return 0
    else:
        logger.error("一部の処理でエラーが発生しましたが、継続しました")
        return 2


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("処理が中断されました")
        sys.exit(130)
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        sys.exit(2)