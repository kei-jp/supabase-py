# TypeScript Coding Rules for Cline

このドキュメントは、TypeScript におけるコード生成・修正の際に、
エージェントと人間が同じ前提でコードを理解できるようにするためのルールを定義する。

本ルールは TypeScript / JavaScript 専用です。
他言語（Pythonなど）では適用しません。

---

## 基本方針

- ルールは「判断を不要にする」ためのものとする
- 自動整形はエディタ設定に委ねる（Prettier など）
- 命名はエージェントが誤解しないことを優先
- 曖昧なケースや例外処理は含めず、skills に委譲する

---

## 命名規則

### ファイル名

- `kebab-case.ts` を推奨
- export される主要識別子と関連性を持たせる

例:
- `user-repository.ts`
- `calc-total-price.ts`

---

### 関数名

- `camelCase`
- 意味が明確な動詞ベースの命名を使う

推奨接頭辞:
- 判定: `is`, `has`, `can`
- 取得: `get`, `fetch`
- 設定: `set`
- 計算: `calc`
- 変換: `convert`, `map`

例:
- `isValidUser`
- `fetchOrderList`
- `calcTotalAmount`

---

### クラス名

- `PascalCase`

例:
- `UserService`
- `OrderRepository`

---

### 変数・引数名

- `camelCase`
- 明確な意味を持つ名前を使用する

NG例:
- `tmp`, `data`, `value`

OK例:
- `userId`, `orderList`, `totalAmount`

---

### インターフェース名

- `PascalCase`
- `I` プレフィックスは使用しない

例:
- `User`, `OrderItem`

---

### 型エイリアス

- `PascalCase`

例:
- `UserId`, `ProductList`

---

### 定数

- `SCREAMING_SNAKE_CASE`

例:
```ts
const MAX_RETRY_COUNT = 5
const API_BASE_URL = 'https://api.example.com'
````

---

### Enum（列挙型）

* Enum名: `PascalCase`
* 値: `SCREAMING_SNAKE_CASE`

例:

```ts
enum UserRole {
  ADMIN = 'admin',
  GUEST = 'guest',
}
```

---

### フォルダ名

* `kebab-case`

例:

* `csv-parser/`
* `user-service/`

---

### React フック

* `camelCase`
* `use` 接頭辞を必須とする

例:

* `useUserList`
* `useCsvUpload`

---

## DB設計ルール（Supabase 前提）

### テーブル名

* `prefix_CamelCase` 形式を使用する
* スキーマ分離は行わず、プレフィックスで責務を分離する

理由:

* Supabase SDK の public スキーマ制約を考慮

例:

* `eSys_ColumnDictionary`
* `eAuth_UserAccount`

※ PostgreSQL 本来の命名規則とは異なるが、プロジェクトルールとして明示

---

### カラム名

* `camelCase`
* PostgreSQLの仕様上、常にダブルクォートが必要になる点に注意

例:

* `"userId"`, `"createdAt"`

---

## フォーマット・レイアウト

* フォーマットはエディタ（Prettier）設定に準拠
* フォーマット差分だけのコミットは禁止

---

## コーディング作法

* 1関数1責務を原則とする
* ネストは浅く保つ
* 早期 return を許可する
* マジックナンバーは禁止（定数化する）
* 同一ロジックのコピペは禁止

---

## コメント

* 「なぜこの実装なのか」をコメントする
* 自明なコードにコメントは不要
* TODO / FIXME には理由を併記する

---

## 禁止事項

* 意図の不明な省略記法
* 出典不明なコピーコード
* 未確認のコメントアウト
* 不要な最適化

---

## skills に委譲する内容

以下はこのルールでは扱わず、skills.md に委譲する：

* 関数の抽象化基準
* 命名に迷ったケース
* パフォーマンスと可読性のトレードオフ
* ドメイン依存の設計判断

