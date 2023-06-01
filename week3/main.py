#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def read_left_parenthesis(line, index, parenthesis_pair_index):
    token = {'type': 'LEFT_PARENTHESIS', 'parenthesis_pair': parenthesis_pair_index}
    return token, index + 1


def read_right_parenthesis(line, index, parenthesis_pair_index):
    token = {'type': 'RIGHT_PARENTHESIS',
             'parenthesis_pair': parenthesis_pair_index}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    parenthesis_depth_tmp = 0
    parenthesis_depth_max = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parenthesis(line, index, parenthesis_depth_tmp)
            parenthesis_depth_tmp += 1
            if parenthesis_depth_tmp > parenthesis_depth_max:
                parenthesis_depth_max = parenthesis_depth_tmp
        elif line[index] == ')':
            if parenthesis_depth_tmp == 0:
                print('Invalid: ")" is not found')
                exit(1)
            parenthesis_depth_tmp -= 1
            (token, index) = read_right_parenthesis(
                line, index, parenthesis_depth_tmp)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens, parenthesis_depth_max


def evaluate_block(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        # 掛け算と割り算を先に計算する
        if tokens[index]['type'] == 'MULTIPLY':
            tokens[index - 1]['number'] *= tokens[index + 1]['number']
            del tokens[index: index + 2]
        elif tokens[index]['type'] == 'DIVIDE':
            tokens[index - 1]['number'] /= tokens[index + 1]['number']
            del tokens[index: index + 2]
        else:
            index += 1
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def evaluate(tokens, parenthesis_depth_max):
    # 括弧の深さが最大のものから順に計算する
    for parenthesis_depth in range(parenthesis_depth_max, -1, -1):
        index = 0
        while index < len(tokens):
            if tokens[index]['type'] == 'LEFT_PARENTHESIS' and tokens[index]['parenthesis_pair'] == parenthesis_depth:
                # 括弧の対応する右括弧の位置を探す
                index_right_parenthesis = index + 1
                while index_right_parenthesis < len(tokens):
                    if tokens[index_right_parenthesis]['type'] == 'RIGHT_PARENTHESIS' and tokens[index_right_parenthesis]['parenthesis_pair'] == parenthesis_depth:
                        break
                    index_right_parenthesis += 1
                else:
                    print('Invalid: ")" is not found')
                    exit(1)
                # 括弧内の式を計算する
                answer = evaluate_block(tokens[index + 1: index_right_parenthesis])
                # 括弧内の式を計算した結果をtokensに反映させる
                tokens[index: index_right_parenthesis + 1] = [
                    {'type': 'NUMBER', 'number': answer}]
            index += 1
    answer = evaluate_block(tokens)
    return answer


def test(line):
    tokens, parenthesis_depth_max = tokenize(line)
    actual_answer = evaluate(tokens, parenthesis_depth_max)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0/2.0*3.0+4.0-5.0")
    test("1.0+2.0/2.0+3.0")
    test("(1.0+2.0)/3.0*3.0")
    test("1.0+2.0*(3.0+4.0)")
    test("(3.0+4*(2-1))/5")
    test("1.0+2.0*(3.0+(2.0+1.0)*2)/9.0")
    test("(1+2)*1")
    print("==== Test finished! ====\n")


if __name__ == '__main__':

    run_test()

    while True:
        print('> ', end="")
        line = input()
        tokens, parenthesis_depth_max = tokenize(line)
        answer = evaluate(tokens, parenthesis_depth_max)
        print("answer = %f\n" % answer)
