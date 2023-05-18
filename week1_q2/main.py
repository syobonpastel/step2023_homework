# week1_q2
# 与えられた文字列の全ての文字を使わなくても良いように関数をアップグレードする

import sys

# 1 point: a, e, h, i, n, o, r, s, t
# 2 points: c, d, l, m, u
# 3 points: b, f, g, p, v, w, y
# 4 points: j, k, q, x, z

score_table = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4,
               2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]


def count_char(str):
    count = []
    for i in range(26):
        count.append(str.count(chr(ord('a') + i)))

    return count


def calulate_score(str):
    score = 0
    for i in range(26):
        score += score_table[i] * str[i]

    return score


def anagram(str, sorted_dictionary):
    # 入力文字列の一部を使って作れるAnagramを探す
    # input_str_sorted = sort_str(str)
    input_char_list = count_char(str)
    for dictionary_word in sorted_dictionary:
        if dictionary_word['length'] > len(str):
            continue
        for j in range(26):
            if input_char_list[j] < dictionary_word['counted_char'][j]:
                break
        else:
            return dictionary_word['word']

    return ""


def main():
    # 辞書ファイルの読み込み
    with open('words.txt', 'r') as f:
        dictionary = f.read().splitlines()

    sorted_dictionary = []
    for dictionary_word in dictionary:
        sorted_dictionary.append({
            'length': len(dictionary_word),
            'word': dictionary_word,
            'counted_char': count_char(dictionary_word),
            'score': calulate_score(count_char(dictionary_word))
        })

    sorted_dictionary.sort(key=lambda x: x['score'], reverse=True)

    # 入力文字列の読み込み
    file_list = ["small", "medium", "large"]
    # file_list = ["large"]
    for file in file_list:
        input_str_list = []
        with open(file+'.txt', 'r') as f:
            input_str_list = f.read().splitlines()

        # Anagramを探す
        with open('output_'+file+'.txt', 'w') as f:
            for str in input_str_list:
                f.write(anagram(str, sorted_dictionary)+'\n')


if __name__ == '__main__':
    main()
