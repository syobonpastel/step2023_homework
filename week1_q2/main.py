# week1_q2
# 与えられた文字列の全ての文字を使わなくても良いように関数をアップグレードする

import sys
import copy

# 1 point: a, e, h, i, n, o, r, s, t
# 2 points: c, d, l, m, u
# 3 points: b, f, g, p, v, w, y
# 4 points: j, k, q, x, z

score_table = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4,
               2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]


def sort_str(str):
    return ''.join(sorted(str))


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


def anagram(str, sort_dictionary):
    # 入力文字列の一部を使って作れるAnagramを探す
    # input_str_sorted = sort_str(str)
    input_char_list = count_char(str)
    anagram_list = []

    for i in range(len(sort_dictionary)):
        if sort_dictionary[i][0] > len(str):
            break
        else:
            for j in range(26):
                if input_char_list[j] < sort_dictionary[i][3][j]:
                    break
            else:
                anagram_list.append(
                    [sort_dictionary[i][2], sort_dictionary[i][3]])

    return anagram_list


def highest_anagram_score(output_list):
    # 最大スコアのAnagramを探す
    max_score = 0
    max_score_word = ''
    for i in range(len(output_list)):
        score = calulate_score(output_list[i][1])
        if score > max_score:
            max_score = score
            max_score_word = output_list[i][0]

    return max_score_word


if __name__ == '__main__':
    # 辞書ファイルの読み込み
    with open('words.txt', 'r') as f:
        dictionary = f.read().splitlines()

    sort_dictionary = []
    for i in range(len(dictionary)):
        sort_dictionary.append(
            [len(dictionary[i]), sort_str(dictionary[i]), dictionary[i], count_char(dictionary[i])])

    sort_dictionary.sort()

    # 入力文字列の読み込み
    file = ["small", "medium", "large"]
    # file = ["small"]
    for k in range(len(file)):
        input_str = []
        with open(file[k]+'.txt', 'r') as f:
            input_str = f.read().splitlines()

        # Anagramを探す
        output_list = []
        for str in input_str:
            output = anagram(str, sort_dictionary)
            if len(output) == 0:
                output_list.append('')
            else:
                max_score_word = highest_anagram_score(output)
                output_list.append(max_score_word)

        with open('output_'+file[k]+'.txt', 'w') as f:
            for str in output_list:
                f.write(str+'\n')