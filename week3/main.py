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


def read_left_parenthesis(line, index):
    token = {'type': 'LEFT_PARENTHESIS'}
    return token, index + 1


def read_right_parenthesis(line, index):
    token = {'type': 'RIGHT_PARENTHESIS'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
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
            (token, index) = read_left_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parenthesis(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_block(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' tokens
    index = 1
    tmp_tokens = []
    while index < len(tokens) and tokens[index]['type'] != 'RIGHT_PARENTHESIS':
        # 掛け算と割り算を先に計算する
        if tokens[index]['type'] == 'MULTIPLY':
            if tokens[index + 1]['type'] == 'LEFT_PARENTHESIS':
                # 括弧内の計算結果をtmp_tokensに追加する
                tmp_calced, tmp_index = evaluate_block(tokens[index + 2:])
                tmp_tokens.append(
                    {'type': 'NUMBER', 'number': tmp_calced * tmp_tokens.pop()['number']})
                index += tmp_index + 3
                print("mal",tokens[index:])
            else:
                tmp_tokens.append({'type': 'NUMBER',
                                   'number': tmp_tokens.pop()['number'] * tokens[index + 1]['number']})
                index += 2
        elif tokens[index]['type'] == 'DIVIDE':
            if tokens[index + 1]['type'] == 'LEFT_PARENTHESIS':
                # 括弧内の計算結果をtmp_tokensに追加する
                tmp_calced, tmp_index = evaluate_block(tokens[index + 2:])
                tmp_tokens.append(
                    {'type': 'NUMBER', 'number': tmp_calced / tmp_tokens.pop()['number']})
                index += tmp_index + 3
                # print(tokens[index:])
            else:
                tmp_tokens.append({'type': 'NUMBER',
                                   'number': tmp_tokens.pop()['number'] / tokens[index + 1]['number']})
                index += 2
        else:
            tmp_tokens.append(tokens[index])
            index += 1
    index = 1
    if tmp_tokens[0]['type'] != 'MINUS':
        tmp_tokens.insert(0, {'type': 'PLUS'})
    print(tmp_tokens)
    while index < len(tmp_tokens) and tmp_tokens[index]['type'] != 'RIGHT_PARENTHESIS':
        if tmp_tokens[index]['type'] == 'NUMBER':
            if tmp_tokens[index - 1]['type'] == 'PLUS':
                answer += tmp_tokens[index]['number']
            elif tmp_tokens[index - 1]['type'] == 'MINUS':
                answer -= tmp_tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        elif tmp_tokens[index]['type'] == 'LEFT_PARENTHESIS':
            # print(tmp_tokens[index + 1:])
            tmp_calced, tmp_index = evaluate_block(tmp_tokens[index + 1:])
            tmp_token = {'type': 'NUMBER', 'number': tmp_calced}
            if tmp_tokens[index - 1]['type'] == 'PLUS':
                answer += tmp_token['number']
            elif tmp_tokens[index - 1]['type'] == 'MINUS':
                answer -= tmp_token['number']
            else:
                print('Invalid syntax')
                exit(1)
            index += tmp_index + 1
        index += 1
    return answer, index


def evaluate(tokens):
    # 括弧を見つけたら、括弧内を取り出して再帰的にevaluateする
    # 括弧内の計算が終わったら、indexを括弧の終わりの次のindexに移動させる
    answer, index = evaluate_block(tokens)
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("-1")
    test("1+2")
    test("1.0+2.1-3")
    test("-2.0*3.0")
    test("1.0/2.0*3.0+4.0-5.0")
    test("1.0+2.0/2.0+3.0")
    test("(1.0+2.0)/3.0*3.0")
    test("1.0+2.0*(3.0+4.0)")
    test("(((1)))")
    test("(1.0+2.0)*(3.0+4.0)")
    test("(3.0+4*(2-1))/5")
    test("1.0+2.0*(3.0+(2.0+1.0)*2)/9.0")
    test("(1+2)*1")
    print("==== Test finished! ====\n")


if __name__ == '__main__':

    run_test()

    while True:
        print('> ', end="")
        line = input()
        tokens = tokenize(line)
        answer = evaluate(tokens)
        print("answer = %f\n" % answer)
