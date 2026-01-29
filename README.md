# shared-config 導入手順（サブツリー + シンボリックリンク構成）

このリポジトリは、複数のプロジェクトで共通利用する設定・ルール（例：`.clinerules`/`.github`）を `git subtree` を使って導入・管理しています。

---

## 🔧 初回導入手順

### サブツリーとして導入

```bash
git subtree add --prefix=shared-config https://github.com/kei-jp/shared-config.git main --squash
```
※ すでに存在する場合は `subtree pull` を参照。

---

### `.clinerules` のシンボリックリンクを作成

Windows の場合（管理者権限で実行）：

```bash
mklink .clinerules shared-config/.clinerules
mklink /D .github shared-config/.github
```

macOS / Linux の場合：

```bash
ln -s shared-config/.clinerules .clinerules
ln -s shared-config/.github .github
```

---

## 🔄 更新手順（最新を取得する）

```bash
git subtree pull --prefix=shared-config https://github.com/kei-jp/shared-config.git main --squash
```

---

## 🚨 注意点

* `.clinerules` はワークスペースのルートに必要です（`cline` の仕様）。
* サブツリー配下のファイルを直接編集しても `shared-config` 本体には反映されません。
* 変更を共有したい場合は `shared-config` リポジトリへ直接プッシュしてください。

---

## 📝 補足

* シンボリックリンク作成は初回のみ必要です。
* `.clinerules` 以外にも共通化したいファイルがある場合は `shared-config` 側にまとめて管理しましょう。
