# “Mujina” found your den!
(作成中)Notionを活用した論文調査を支援するSlack bot

Slackにメンション付き`@mujina`で論文のPDFを送信すると，論文の要約を生成してユーザーのNotionに記録していきます．

開発期間: 2024/06/05 ~

## Background

自分の研究活動の中で，検証したい内容に近い内容を行っている「いい感じ」の論文を見つけるまでの時間がボトルネックになっています．

これを解消するために，(1)論文のおおまかな内容を高速に把握すると同時に(2)文献調査の証跡を残しながらオートメーションを行うことができるツールを開発したいと考えました．

## System Design

|名称|選定理由|
| --- | --- |
|AWS Lambda| 一連の処理ではサーバーを常時運用する必要がなく，サーバーレス(FaaS)で問題なかったため．FaaSの中では料金・ドキュメント量ともに大差がなかったため※1，今後使用する可能性が高いAWSを採用． |
|OpenAI API (gpt-4o)| 高速・安価・高性能なため※2．特にレイテンシについては，AWS API Gatewayのタイムアウト時間(29秒)※3に間に合わせる必要がある．|

※1 参考: https://cloud-ace.jp/column/detail322/

※2 参考 Artifical Analysis: https://artificialanalysis.ai/

※3 参考 AWS API Gateway: https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/limits.html#api-gateway-execution-service-limits-table

## TODO

|タイトル|内容|意図・懸念点など|
| --- | --- | --- |
|gpt-4oによる要約|OpenAI APIに論文テキストを送信し，gpt-4oによる要約生成を行う|必須機能|
|Notion Integrationとの連携| NotionのDBに論文の情報を保存する |必須機能|
|PDF読み取りライブラリの再検討|PythonのPDF読み取りライブラリpypdfでは日本語のエンコードができないため，pdfminer.sixへの乗り換えを検討|pdfminer.sixはzipに圧縮した際の容量が大きい(>10MB)ため使用を回避したい．現時点では英語論文のみに使えればよいためpypdfのまま開発を続行する．|
|PDFテキスト前処理|読み取った論文PDFのテキストを処理するメソッドを実装する|(1)gpt-4oに送信するトークン量を減らしたい(2)要約の品質を高めたい|

## In the future
個人用にミニマルなシステムを開発して，(金銭的・技術的に)可能であればリリースできる形へとスケールさせることを検討しています．
 1. 自分用に使いやすいシステムを開発する
 2.  他の人に試してもらい(ex. 研究室のSlackに無償で提供する)，UXの検証・改善
 3. (可能であれば)Slack Marketplaceへのリリース
