# Week5 Homework

## 課題

[tsp challenge](https://github.com/hayatoito/google-step-tsp) の実装

## 実行方法

1. https://github.com/hayatoito/google-step-tsp を `/week5` にクローン
1. `$cd week6`
1. `$gcc -o main main.c`
1. `$./main` 

### ビジュアライザ使用時
1. `cd /week5/google-step-tsp`
2. `$python3 -m http.server` 
3.  http://localhost:8000/visualizer/build/default/ にアクセス

## 実装方針

- 多出発
- 貪欲法で初期解を生成
- 2-optで解を改善