# Week 4 課題

## 課題

### 宿題 1

find_shortest_path() 関数を書いて、あるページから別のページへの最短経路を求めてください 😀

### 宿題 2

find_most_popular_pages() 関数を書いて、ページランクを計算して、重要度の高いページトップ 10 を求めてください

## 実行方法

```bash
$ python3 main.py ./wikipedia_dataset/pages_medium.txt ./wikipedia_dataset/links_medium.txt
```

## 工夫した点など

### 宿題 1

- BFS と並行して経路を持つ辞書を作成し、最短経路を求めた（時間計算量を抑えられる）

### 宿題 2

- `len` 関数の使用回数を減らした