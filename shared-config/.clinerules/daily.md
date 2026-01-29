rules:
  - name: 日報
    description: "会社提出用に①②③形式で整形。ファイル作成・更新は行わず必ずCline Outputに表示だけ。"
    mode: preview
    transform: |
      ① {{#section "今日の完了タスク"}}{{#each rows}}{{content}}{{#unless @last}}・{{/unless}}{{/each}}{{/section}}{{#section "作業中タスク"}}{{#each rows}}{{content}}{{#unless @last}}・{{/unless}}{{/each}}{{/section}}
      ② {{#section "作業中タスク"}}{{#each rows}}{{content}}{{#unless @last}}・{{/unless}}{{/each}}{{/section}}{{#section "明日のタスク"}}{{#each rows}}{{content}}{{#unless @last}}・{{/unless}}{{/each}}{{/section}}
      ③ 今日のひとこと。100〜150文字。必ずどうでもいい日常の独り言。
         - 題材はランダム（食べ物・天気・道具・会話・季節・音・街並み・小さな失敗など）。
         - 文体もランダム（短文・箇条書き・ポエム調・語尾伸ばし・くだけた口調など）。
         - 意味は薄く、スカスカ感を保つ。
