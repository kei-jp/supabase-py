# CSV to SQL Generator

This script generates SQL statements from a CSV file and a column definition JSON file. It is designed to create `CREATE TABLE` statements and `DELETE`/`INSERT` statements for the `eSys_ColumnDictionary`.

---

## Features

- **CREATE TABLE SQL**: Generates a table schema based on the CSV and JSON definitions.
- **Column Dictionary SQL**: Generates `DELETE` and `INSERT` statements for `eSys_ColumnDictionary`.
- **Type Inference**: Automatically infers column types (`INTEGER`, `DATE`, `TEXT`) if not specified in the JSON.
- **Encoding Detection**: Supports multiple encodings (`UTF-8`, `Shift_JIS`, `CP932`, etc.).
- **Error Handling**: Logs undefined columns to `errors.log`.

---

## File Structure

- **`generate_sql.py`**: Main script for generating SQL.
- **`csv_01.csv`**: Sample CSV file.
- **`columnDict.json`**: Column definition JSON file.
- **`create_bulk_csv_01.sql`**: Generated `CREATE TABLE` SQL.
- **`dict_bulk_csv_01.sql`**: Generated `eSys_ColumnDictionary` SQL.

---

## Usage

### Basic Execution

```bash
python generate_sql.py
```

### With Custom Files

```bash
python generate_sql.py input.csv columnDict.json
```

### With Options

```bash
python generate_sql.py --output-dir ./output --prefix myprefix
```

---

## Input Files

### CSV File

- **Example**: `csv_01.csv`
- **Structure**:
  ```
  店舗コード,取引日,数量,金額,商品名
  001,2024-01-15,10,1500,商品A
  002,2024-01-16,5,2000,商品B
  ```

### JSON File

- **Example**: `columnDict.json`
- **Structure**:
  ```json
  {
    "prefix": "bulk",
    "__common": {
      "店舗コード": { "column": "storeCode", "typeHint": "TEXT" },
      "取引日": { "column": "transactionDate", "typeHint": "DATE" },
      "数量": { "column": "quantity", "typeHint": "INTEGER" },
      "金額": { "column": "amount", "typeHint": "INTEGER" },
      "商品名": { "column": "productName", "typeHint": "TEXT" }
    }
  }
  ```

---

## Output Files

### `create_bulk_csv_01.sql`

```sql
CREATE TABLE "bulk_csv_01" (
  "storeCode" INTEGER,
  "transactionDate" DATE,
  "quantity" INTEGER,
  "amount" INTEGER,
  "productName" TEXT,
  "insertDate" TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
```

### `dict_bulk_csv_01.sql`

```sql
DELETE FROM "eSys_ColumnDictionary" WHERE "tableName" = 'bulk_csv_01';

INSERT INTO "eSys_ColumnDictionary" ("tableName", "columnName", "displayNameJa", "displayNameEn")
VALUES
  ('bulk_csv_01', 'storeCode', '店舗コード', 'storeCode'),
  ('bulk_csv_01', 'transactionDate', '取引日', 'transactionDate'),
  ('bulk_csv_01', 'quantity', '数量', 'quantity'),
  ('bulk_csv_01', 'amount', '金額', 'amount'),
  ('bulk_csv_01', 'productName', '商品名', 'productName');
```

---

## Error Handling

- Undefined columns are logged to `errors.log`:
  ```
  未定義カラム:
  カラム名1
  カラム名2
  ```

---

## Requirements

- Python 3.7+
- Libraries: `argparse`, `csv`, `json`, `os`, `sys`, `datetime`, `pathlib`

---

## License

This project is licensed under the MIT License.