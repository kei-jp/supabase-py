# Python Coding Rules for Cline

本ドキュメントは、Pythonコードを生成・修正する際に、
エージェントと人間が同じ前提でコードを理解できるようにするためのルールを定義する。

本ルールは **Python固有の規約のみ** を扱い、
言語非依存の思想・原則は別ドキュメントに委譲する。

---

## 基本方針

- PEP8 を前提とする
- 可読性と保守性を最優先する
- 暗黙的な挙動より明示的なコードを優先する
- Cline が「迷わず書ける」ことを重視する

---

## 命名規則

### ファイル名

- `snake_case.py` を使用する
- ファイルの責務が名前から明確に分かること

例:
- `main.py`
- `config_loader.py`
- `csv_processor.py`
- `supabase_client.py`

---

### 関数名

- `snake_case`
- 動詞 + 目的語を基本形とする

推奨プレフィックス:
- 判定: `is_`, `has_`, `can_`
- 取得: `get_`, `fetch_`, `load_`
- 生成: `create_`, `build_`
- 変換: `convert_`, `map_`, `normalize_`
- 実行: `run_`, `execute_`

例:
- `is_valid_config`
- `load_csv_file`
- `convert_row_to_dict`

---

### クラス名

- `PascalCase`
- 実体・責務が明確な名詞を使用する

例:
- `CsvProcessor`
- `SupabaseClient`
- `JobLogger`

---

### 変数名・引数名

- `snake_case`
- スコープが広いほど具体的な名前にする

禁止例:
- `tmp`
- `data`
- `value`

推奨例:
- `csv_file_path`
- `staging_table_name`
- `error_count`

---

### 定数

- `SCREAMING_SNAKE_CASE`
- `constants.py` に集約することを推奨

例:
```py
DEFAULT_ENCODING = "utf-8"
MAX_RETRY_COUNT = 3
````

---

## 型ヒント（Type Hints）

* Python 3.10+ を前提とする
* 公開関数・主要関数には型ヒントを付与する
* 戻り値がない場合は `-> None` を明示する

例:

```py
def load_config(path: str) -> dict:
    ...
```

---

## 例外・エラーハンドリング

* 例外は握りつぶさない
* 業務処理では **例外送出よりログ＋継続** を優先する
* `try/except` は最小スコープで使用する

禁止例:

```py
except Exception:
    pass
```

推奨例:

```py
except ValueError as e:
    logger.warning(f"Invalid value: {e}")
```

---

## ログ

* `print` は使用しない
* `logging` モジュールを使用する
* ログレベルを明確に使い分ける

| レベル     | 用途        |
| ------- | --------- |
| INFO    | 正常系の進行ログ  |
| WARNING | 処理継続可能な異常 |
| ERROR   | 処理失敗・スキップ |

---

## モジュール設計

* 1ファイル1責務
* `main.py` は制御のみを担当する
* 業務ロジックは必ず別モジュールに分離する

禁止:

* `main.py` に大量のロジックを書くこと

---

## テスト

* `pytest` を前提とする
* 副作用のある処理（DB / API）は分離する
* 単体テスト可能な関数構造を優先する

---

## コメント

* 「何をしているか」ではなく「なぜそうしているか」を書く
* 業務ルール・制約条件はコメントで明示する

---

## skills への委譲対象

* 関数分割の粒度判断
* パフォーマンス最適化の要否
* ドメイン知識に依存する設計判断

