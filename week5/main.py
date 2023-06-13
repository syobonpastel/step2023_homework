import math
import glob
import random

def read_input_csv(file_name):
    cities = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            x, y = line.strip().split(',')
            cities.append({'x': float(x), 'y': float(y), 'index': i - 1})
    return cities


def write_output_csv(file_name, cities):
    with open(file_name, 'w') as f:
        f.write('index\n')
        for city in cities:
            f.write('{}\n'.format(city['index']))


def calc_distance(city1, city2):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def calc_total_distance(cities):
    total_distance = 0
    for i in range(len(cities)):
        city1 = cities[i]
        city2 = cities[(i + 1) % len(cities)]
        total_distance += calc_distance(city1, city2)
    return total_distance


def main():
    input_files = glob.glob('./google-step-tsp/input_[0-9].csv')
    # input_files = input_files[5:]
    for input_file in input_files:
        cities = read_input_csv(input_file)
        total_distance = calc_total_distance(cities)

        for _ in range(10000):
            # ランダムに2つ選んで入れ替える->スコアがよくなるなら採用
            i = random.randint(0, len(cities) - 1)
            j = random.randint(0, len(cities) - 1)
            if i == j:
                continue
            else:
                cities[i], cities[j] = cities[j], cities[i]
                new_total_distance = calc_total_distance(cities)
                if new_total_distance < total_distance:
                    total_distance = new_total_distance
                else:
                    cities[i], cities[j] = cities[j], cities[i]

        write_output_csv('./google-step-tsp/output_' + input_file[len('./google-step-tsp/input_'):], cities)

if __name__ == '__main__':
    main()