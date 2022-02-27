# keibaAI
競馬情報サイトからスクレイピングして得た情報を利用したSVMを用いた分類器です。3着以内に入るか予測します.
<h2>概要
 <h2>使用技術
   <h5>・Python3.7
   <h5>・SQlite3
   <h5>・scikit-learn
<h2>使い方
<h3>各ファイルについて
  <h5>・sc.py  → 競馬情報サイトからスクレイピングを行い,データベースに格納します
  <h5>・sitelist.py  → sc.pyがどのURLからデータを取ってくるか記述する用(netkeibaのレース結果画面のURLを使用)
  <h5>・keibaAI  → データベースからデータを利用したSVMを用いた分類器です。
  <h5>・database.sqlite3  → データベースのファイルです。
  <h5>・sqlite3  → sqlite3をコマンドプロンプトで動かす為のファイルです
   
   ###ads
   -a
   -a
   -a
   -a
    
  
