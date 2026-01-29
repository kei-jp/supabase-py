# Coding Rules for Cline

本ドキュメントは、エージェントによるコーディング時の判断を減らし、
人間とエージェントが同じ前提でコードを読むことを目的とする。

フレームワーク・言語固有の規約は含めない。

---

## 基本方針

- ルールは「判断を不要にする」ためのものとする
- 自動化できるフォーマットはエディタ設定に委譲する
- 命名は人間だけでなくエージェントが読んでも役割を誤解しないことを重視する
- 曖昧な判断やケースバイケースな内容は rules に含めない

---

## 命名規則

### ファイル名

- `camelCase.ts`
- export される主要な識別子と対応させる

例:
- `userRepository.ts`
- `calcTotalPrice.ts`

---

### 関数名

- `camelCase`
- 役割が単語から推測できる名前にする

推奨される接頭辞:
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

- `snake_case`
- 一時的・構造的なデータであることを明示する

ルール:
- 意味のない名前（`tmp`, `data`, `value` など）は避ける
- スコープが広いほど具体的な名前にする

例:
- `user_id`
- `order_list`
- `total_amount`

---

### インターフェース名（TypeScript）

- `PascalCase`
- `I` プレフィックスは使わない（例: `User`, `OrderItem`）

理由:
- 型とドメインモデルを混同しないよう統一された命名を推奨

---

### 型エイリアス（`type`）

- `PascalCase`

例:
- `UserId`
- `ProductList`

---

### コンスタント（定数）
- `SCREAMING_SNAKE_CASE`

理由:
- 変更されない値であることを明示するため

例:
```
const MAX_RETRY_COUNT = 5
const API_BASE_URL = 'https://api.example.com'
```

---

### Enum（列挙型）

- Enum名: `PascalCase`
- 値: `SCREAMING_SNAKE_CASE`

例:
```ts
enum UserRole {
  ADMIN = 'admin',
  GUEST = 'guest',
}
```

---

### フォルダ名

- `kebab-case`

理由:
- CLIやエディタ操作の互換性を考慮

例:
- `csv-parser/`
- `user-service/`

---

### React フック

- `camelCase`
- `use` 接頭辞を必須とする

例:
- `useUserList`
- `useCsvUpload`


---

### テーブル名（PostgreSQL / Supabase）

- `prefix_CamelCase`
- スキーマ分離は行わず、プレフィックスで責務を分離する

理由:
- Supabase SDK の public スキーマ制約を考慮するため

例:
- `eSys_ColumnDictionary`
- `eAuth_UserAccount`

---

### カラム名（PostgreSQL）

- `camelCase`
- PostgreSQL の識別子仕様を前提とする

注意:
- camelCase のカラム名は常にダブルクォートされることを意識する

例:
- `"userId"`
- `"createdAt"`

---

## フォーマット・レイアウト

- フォーマットはエディタ設定を正とする
- 手動での整形は行わない
- フォーマット差分のみの変更は禁止する

---

## コーディング作法（概要）

- 1関数1責務を原則とする
- ネストは深くしすぎない
- 早期 return を許可する
- マジックナンバーは禁止し、意味のある名前を与える
- 同じロジックのコピーペーストを行わない

※ 詳細な判断基準は skills に委譲する

---

## コメント

- コメントは「何をしているか」ではなく「なぜそうしているか」を書く
- 自明なコードにコメントを書かない
- TODO / FIXME には理由を併記する

---

## 禁止事項

- 意図の分からない省略
- コピー元不明のコード
- 動作確認されていないコメントアウト
- 理由のない最適化

---

## skills への委譲対象

以下は本 rules では扱わない。

- 関数分割・抽象化の判断基準
- 命名に迷ったケース
- パフォーマンスと可読性のトレードオフ
- ドメイン知識に依存する設計判断
