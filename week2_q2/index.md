# Week2 課題 2

## 問題

木構造を使えば O(log N)、ハッシュテーブルを使えばほぼ O(1) で検索・追加・削除を実現することができて、これだけ見ればハッシュテーブルのほうが優れているように見える。ところが現実の大規模なデータベースでは、ハッシュテーブルではなく木構造が使われることが多い。その理由を考えよ。

## 解答

- 1 回あたりの計算量が一定ではない（ rehash 時だけ）ので、クエリの処理速度を安定させるのが難しい。
  - 時間帯によってサービスの使用量にばらつきがある場合、クエリが少ない時間に rehash することである程度解決できそう。
- ハッシュテーブルでデータを保存する場合、計算量を安定させるには N よりも大きなサイズのハッシュテーブルを用意する必要があり、木構造よりも多くのメモリを必要とする。
- stack や cue のようなデータ構造を実現するために必要な、順序情報を木構造は持っている。
  - 課題 3 のようなデータ構造を取れば解決する。
- ハッシュ関数による衝突頻度のばらつきが、木構造では存在しない。