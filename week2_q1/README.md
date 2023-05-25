# Week2 課題 1

## アルゴリズムの説明

チェイン法を利用して、キーと値のペアをハッシュテーブルに保存するデータ構造を実装した。

## プログラムの実行方法

`main.py` があるディレクトリで以下のコマンドを実行する。

```bash
python3 main.py 
```

このとき、次のような出力が期待される。

```bash
Functional tests passed!
0 0.148053
1 0.195106
2 0.135594
(略)
Performance tests passed!
```

## 工夫した点

- 素数のテーブルを持たせ、文字と単語内での文字の位置に対してそれぞれ割り当てた素数を掛け合わせてハッシュ値を計算した。これにより、ハッシュ値の衝突を減らすことができる。
    ```python
    hash += prime_num_table[ord(c) % prime_num_table_len] * \
                prime_num_table[i % prime_num_table_len] * ord(c)
    ```