# Week5 Homework

## 課題

[tsp challenge](https://github.com/hayatoito/google-step-tsp) の実装

## 実行方法

1. https://github.com/hayatoito/google-step-tsp を `/week5` にクローン
1. `python3 main.py` を実行
1. (ビジュアライザ使用時) `python3 -m http.server` を実行してから、 http://localhost:8000/visualizer/build/default/ にアクセス

## 実装方針

- 多出発
- 貪欲法で初期解を生成
- 焼きなまし法で解を改善