import math
import glob
import random
import copy


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
    input_files = glob.glob('./google-step-tsp/input_[0-6].csv')
    # input_files = glob.glob('./google-step-tsp/input_3.csv')
    alpha = 0.85
    # input_files = input_files[5:]
    for input_file in input_files:
        cities = read_input_csv(input_file)

        best_total_distance = calc_total_distance(cities)
        best_cities = copy.deepcopy(cities)
        cities_count = len(cities)

        for _ in range (30):
            # 初期解の生成
            # 貪欲法
            current_city = random.choice(cities)
            unvisited_cities = copy.deepcopy(cities)
            unvisited_cities.remove(current_city)
            visited_cities = [current_city]
            while len(unvisited_cities) > 0:
                next_city = min(unvisited_cities, key=lambda city: calc_distance(
                    current_city, city))
                unvisited_cities.remove(next_city)
                visited_cities.append(next_city)
                current_city = next_city

            total_distance = calc_total_distance(visited_cities)
            assert cities_count == len(visited_cities)

            for k in range(min(cities_count * 1000, 100000)):
                # ランダムに2つ選んで入れ替える->スコアがよくなるなら採用/スコアが良くならない場合でも確率的に採用
                i = random.randint(0, cities_count - 1)
                j = random.randint(0, cities_count - 1)
                if i == j:
                    continue
                else:
                    visited_cities[i], visited_cities[j] = visited_cities[j], visited_cities[i]
                    new_total_distance = calc_total_distance(visited_cities)
                    if new_total_distance < total_distance:
                        total_distance = new_total_distance
                    elif random.random() < alpha**((new_total_distance - total_distance)):
                        total_distance = new_total_distance
                        # print('accept')
                    else:
                        visited_cities[i], visited_cities[j] = visited_cities[j], visited_cities[i]
                        # print('reject')
                
                if k % 10000 == 0:
                    print(k, total_distance)

            if total_distance < best_total_distance:
                best_total_distance = total_distance
                best_cities = copy.deepcopy(visited_cities)

        assert cities_count == len(best_cities)

        write_output_csv('./google-step-tsp/output_' +
                         input_file[len('./google-step-tsp/input_'):], best_cities)
        print(input_file, best_total_distance)


if __name__ == '__main__':
    main()
