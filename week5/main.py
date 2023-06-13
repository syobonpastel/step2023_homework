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
    alpha = 0.5
    # input_files = input_files[5:]
    for input_file in input_files:
        cities = read_input_csv(input_file)

        # 初期解の生成
        # 象限ごとに分けて、x座標が小さい順に並べる
        x_min = min([city['x'] for city in cities])
        x_max = max([city['x'] for city in cities])
        y_min = min([city['y'] for city in cities])
        y_max = max([city['y'] for city in cities])

        city_groups = [[], [], [], []]
        for city in cities:
            if city['x'] < x_min + (x_max - x_min) / 2:
                if city['y'] < y_min + (y_max - y_min) / 2:
                    city_groups[0].append(city)
                else:
                    city_groups[1].append(city)
            else:
                if city['y'] < y_min + (y_max - y_min) / 2:
                    city_groups[2].append(city)
                else:
                    city_groups[3].append(city)

        cities = []
        for i, city_group in enumerate(city_groups):
            city_group.sort(key=lambda city: city['x'])
            if i % 2 == 1:
                city_group.reverse()
            cities += city_group

        total_distance=calc_total_distance(cities)
        cities_count=len(cities)

        for _ in range(cities_count * 100):
            # ランダムに2つ選んで入れ替える->スコアがよくなるなら採用/スコアが良くならない場合でも確率的に採用
            i=random.randint(0, cities_count - 1)
            j=random.randint(0, cities_count - 1)
            if i == j:
                continue
            else:
                cities[i], cities[j]=cities[j], cities[i]
                new_total_distance=calc_total_distance(cities)
                if new_total_distance < total_distance:
                    total_distance=new_total_distance
                elif random.random() < alpha**(new_total_distance - total_distance):
                    total_distance=new_total_distance
                else:
                    cities[i], cities[j]=cities[j], cities[i]

        write_output_csv('./google-step-tsp/output_' +
                         input_file[len('./google-step-tsp/input_'):], cities)


if __name__ == '__main__':
    main()
