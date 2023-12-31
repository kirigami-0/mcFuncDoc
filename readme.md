# mcFuncDoc

Minecraft専用データパックドキュメント化ツール  
  
# 動作確認済みOS
- windows11
  
# 必要環境  
- python  
- VSCode(任意)  

# ドキュメントルール
以下のルールに従ってドキュメント化されます。  
1. `#>`からコメントが途切れるまで  
   例:
   ```mcfunction
   #> ドキュメント始まり
   # ここもドキュメント化対象
   execute ~~~~
   # ここはドキュメント化されない  

   #> ここはドキュメント対象  
       # インデントを開けてもドキュメント対象
   ```
   結果：  
   ```
   #> ドキュメント始まり
   # ここもドキュメント化対象  

   #> ここはドキュメント対象  
       # インデントを開けてもドキュメント対象
   ```
2. アノテーションの文字が変化する。

# 使い方  
### ドキュメント化実行手順  
1. `config.json`ファイルの`datapackPath`にデータパックのパスを指定する。  
   ※ 複数のデータパックも同時にドキュメント可
2. `main.py`を実行する  
3. `docs/データパック名/`にhtmlファイルが生成されれば正常  

### ドキュメントカスタマイズ手順  
現状だとダークテーマ的なHTMLファイルが生成されるが、  
オリジナルの配色へ変更することが可能  
- アノテーションの色を変更したい(カラーコードの知識が必要)  
  - `config.json`内の`annotationsColor`の中身を変更することで色を変えることができる  
  例：  
  ```json
  "@api": "#0000FF" // こうすることでコメント内の@apiの文字が青色となる。
  "@common": "#000000" // @+色を変えたい文字: 16進数RGBで指定することで自由に色を変更できる
  ```
- ダークテーマじゃないかわいいテーマに変更したい。(CSSの知識が必要)
  - `config.json`内の`theme`の中身を変更することでテーマを変更できる
  - 内容を書き換えた場合、`modules`フォルダーにテーマ名と同じCSSファイルを作成する必要がある。
  例：  
  ```json
  // config.json
  "theme": "blue" //ブルーテーマに変更する
  ```
  ```
  // modulesフォルダ
  ファイル名: blue.module.cssでCSSを作成する。
  default.module.cssを参考に、クラス名を変更せずに内容を変更することでテーマを変更できる。
  ```
  
# バグ報告に関して  
[issues](https://github.com/kirigami-0/mcFuncDoc/issues)で受け付けてます。  
  
# ライセンスに関して  
このソースのライセンスは、MITライセンスです。  
