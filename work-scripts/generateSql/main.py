#!/usr/bin/env python3
"""
CSV から SQL を自動生成するスクリプト

仕様:
- CSV ファイルとカラム定義 JSON をもとに SQL を生成
- CREATE TABLE ステートメント
- eSys_ColumnDictionary 用の DELETE/INSERT ステートメント
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

from matplotlib import table


def read_csv(file_path: str) -> Tuple[List[str], List[List[str]]]:
    """CSV ファイルを読み込み、ヘッダと行を返す。"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV ファイルが見つかりません: {file_path}")

    # エンコーディングを自動検出して読み込み
    encodings = ['utf-8', 'shift_jis', 'cp932', 'utf-8-sig']
    for encoding in encodings:
        try:
            with open(file_path, encoding=encoding) as f:
                reader = csv.reader(f)
                header = next(reader)
                rows = list(reader)
            return header, rows
        except UnicodeDecodeError:
            continue

    raise ValueError(f"ファイル {file_path} のエンコーディングを検出できませんでした")


def read_json(file_path: str) -> Dict[str, Any]:
    """JSON ファイルを読み込み、その内容を返す。"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON ファイルが見つかりません: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def infer_type(value: str) -> str:
    """サンプル値から SQL 型を推定する。"""
    if not value or value.strip() == "":
        return "TEXT"

    # 整数かチェック
    try:
        int(value)
        return "INTEGER"
    except ValueError:
        pass

    # 日付かチェック (YYYY-MM-DD 形式)
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return "DATE"
    except ValueError:
        pass

    # その他は TEXT
    return "TEXT"


def get_column_info(
    header: List[str],
    column_dict: Dict[str, Any],
    table_key: str
) -> Tuple[List[Tuple[str, str]], List[str]]:
    """カラム情報を取得し、未定義カラムもチェックする。"""
    columns = []
    undefined_columns = []

    for japanese_name in header:
        # table_key セクションから探す
        if japanese_name in column_dict.get(table_key, {}):
            col_info = column_dict[table_key][japanese_name]
        # __common セクションから探す
        elif japanese_name in column_dict.get("__common", {}):
            col_info = column_dict["__common"][japanese_name]
        else:
            undefined_columns.append(japanese_name)
            continue

        column_name = col_info["column"]
        data_type = col_info.get("typeHint", "TEXT")
        columns.append((column_name, data_type))

    return columns, undefined_columns


def generate_create_table_sql(
        table_name: str, columns: List[Tuple[str, str]]) -> str:
    """CREATE TABLE SQL ステートメントを生成する。"""
    column_definitions = [
        f'  "{col_name}" {data_type}'
        for col_name, data_type in columns
    ]
    column_definitions.append(
        '  "insertDate" TIMESTAMP WITHOUT TIME ZONE DEFAULT now()'
    )

    sql = f"DROP TABLE IF EXISTS {table_name};\n"
    sql += f'CREATE TABLE "{table_name}" (\n'
    sql += ",\n".join(column_definitions)
    sql += "\n);"

    return sql


def generate_dict_sql(
    table_name: str,
    columns: List[Tuple[str, str]],
    header: List[str]
) -> Tuple[str, str]:
    """eSys_ColumnDictionary 用の DELETE/INSERT SQL を生成する。"""
    delete_sql = (
        f'DELETE FROM "eSys_ColumnDictionary" '
        f'WHERE "tableName" = \'{table_name}\';'
    )

    insert_values = []
    col_index = 0
    for japanese_name in header:
        if col_index < len(columns):
            col_name, _ = columns[col_index]
            insert_values.append(
                f"  ('{table_name}', '{col_name}', "
                f"'{japanese_name}', '{col_name}')"
            )
            col_index += 1

    insert_sql = (
        'INSERT INTO "eSys_ColumnDictionary" '
        '("tableName", "columnName", "displayNameJa", "displayNameEn")\n'
        'VALUES\n' + ",\n".join(insert_values) + ";"
    )

    return delete_sql, insert_sql


def write_errors(undefined_columns: List[str], output_dir: str = ".") -> None:
    """未定義カラムをエラーログに出力する。"""
    error_file = os.path.join(output_dir, "errors.log")
    with open(error_file, "w", encoding="utf-8") as f:
        f.write("未定義カラム:\n")
        f.write("\n".join(undefined_columns))
    print(f"未定義カラムが見つかりました。詳細は {error_file} を確認してください。")


def process_csv(
    csv_file: str,
    json_file: str,
    output_dir: str = ".",
    table_prefix: str = "bulk"
) -> bool:
    """CSV ファイルを処理して SQL ファイルを生成する。"""
    try:
        # ファイル読み込み
        header, rows = read_csv(csv_file)
        column_dict = read_json(json_file)

        # テーブル名生成
        table_key = Path(csv_file).stem
        table_name = f"{table_prefix}_{table_key}"

        # カラム情報取得
        columns, undefined_columns = get_column_info(
            header, column_dict, table_key
        )

        # 未定義カラムがある場合はエラー
        if undefined_columns:
            write_errors(undefined_columns, output_dir)
            return False

        # 型推定（typeHint が未指定の場合）
        final_columns = []
        for i, (col_name, data_type) in enumerate(columns):
            if data_type == "TEXT" and i < len(rows) and len(rows[0]) > i:
                # サンプルデータから型推定
                inferred_type = infer_type(rows[0][i])
                final_columns.append((col_name, inferred_type))
            else:
                final_columns.append((col_name, data_type))

        # SQL 生成
        create_table_sql = generate_create_table_sql(table_name, final_columns)
        delete_sql, insert_sql = generate_dict_sql(
            table_name, final_columns, header
        )

        # ファイル出力
        sql_file = os.path.join(output_dir, f"{table_name}.sql")

        with open(sql_file, "w", encoding="utf-8") as f:
            f.write(create_table_sql)
            f.write("\n\n")
            f.write(delete_sql + "\n\n" + insert_sql)

        print(f"SQL ファイルを生成しました: {sql_file}")
        return True

    except FileNotFoundError as e:
        print(f"エラー: {e}")
        return False
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return False


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="CSV から SQL を自動生成するスクリプト"
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default="csv_01.csv",
        help="CSV ファイルのパス (デフォルト: csv_01.csv)"
    )
    parser.add_argument(
        "json_file",
        nargs="?",
        default="columnDict.json",
        help="カラム定義 JSON ファイルのパス (デフォルト: columnDict.json)"
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="出力ディレクトリ (デフォルト: 現在のディレクトリ)"
    )
    parser.add_argument(
        "--prefix",
        "-p",
        default="bulk",
        help="テーブル名のプレフィックス (デフォルト: bulk)"
    )

    args = parser.parse_args()

    # 出力ディレクトリ作成
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    # CSV 処理実行
    success = process_csv(
        args.csv_file,
        args.json_file,
        args.output_dir,
        args.prefix
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
