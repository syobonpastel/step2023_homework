#include <glob.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    int index;
    double x;
    double y;
} city;

int read_cities(city* cities, char* filename)
{
    FILE* fp = fopen(filename, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: cannot open %s\n", filename);
        return -1;
    }

    char buf[256];
    fgets(buf, sizeof(buf), fp);  // 1行目は読み飛ばす
    int i;
    while (fgets(buf, sizeof(buf), fp) != NULL) {
        sscanf(buf, "%lf,%lf", &cities[i].x, &cities[i].y);
        cities[i].index = i;
        i++;
    }
    fclose(fp);
    return i;
}

void write_cities(int* route, int n, char* filename)
{
    FILE* fp = fopen(filename, "w");

    if (fp == NULL) {
        fprintf(stderr, "Error: cannot open %s\n", filename);
        return;
    }

    fprintf(fp, "index\n");
    for (int i = 0; i < n; i++) {
        fprintf(fp, "%d\n", route[i]);
    }
    fclose(fp);
}

double calc_distance(city* c1, city* c2)
{
    double dx = c1->x - c2->x;
    double dy = c1->y - c2->y;
    return sqrt(dx * dx + dy * dy);
}

double calc_total_distance(city* cities, int* route, int n)
{
    double sum_distance = 0;
    for (int i = 0; i < n; i++) {
        sum_distance += calc_distance(&cities[route[i]], &cities[route[(i + 1) % n]]);
    }
    return sum_distance;
}

void swap(int i, int j, int* route)
{
    // i と j の間を反転
    while (i < j) {
        int tmp = route[i];
        route[i] = route[j];
        route[j] = tmp;
        i++;
        j--;
    }
}

int main()
{
    glob_t globbuf;
    const double alpha = 0.7;

    int ret = glob("../week5/google-step-tsp/input_[6-6].csv", 0, NULL, &globbuf);
    for (int i = 0; i < globbuf.gl_pathc; i++) {
        city cities[10000];
        int cities_num = read_cities(cities, globbuf.gl_pathv[i]);
        printf("%s: %d\n", globbuf.gl_pathv[i], cities_num);

        // 2 都市間の距離を計算
        // double distances[cities_num][cities_num];
        // for (int i = 0; i < cities_num; i++) {
        //     for (int j = i; j < cities_num; j++) {
        //         distances[i][j] = calc_distance(&cities[i], &cities[j]);
        //         distances[j][i] = distances[i][j];
        //     }
        // }

        // for (int i = 0; i < cities_num; i++) {
        //     for (int j = 0; j < cities_num; j++) {
        //         printf("%lf ", distances[i][j]);
        //     }
        //     printf("\n");
        // }

        int best_route[cities_num];
        double best_score = 1e100;

        for (int l = 0; l < 1; l++) {

            // 貪欲法
            int route[cities_num];
            srand((unsigned int)time(NULL));
            int current_city = rand() % cities_num;
            route[0] = current_city;
            bool visited[cities_num];
            for (int i = 0; i < cities_num; i++) {
                visited[i] = false;
            }
            visited[current_city] = true;
            for (int i = 1; i < cities_num; i++) {
                double min_distance = 1e100;
                int next_city = -1;
                for (int j = 0; j < cities_num; j++) {
                    if (visited[j]) {
                        continue;
                    }
                    if (calc_distance(&cities[current_city], &cities[j]) < min_distance) {
                        min_distance = calc_distance(&cities[current_city], &cities[j]);
                        next_city = j;
                    }
                }
                route[i] = next_city;
                current_city = next_city;
                visited[current_city] = true;
            }

            double score = calc_total_distance(cities, route, cities_num);

            printf("greedy: %lf\n", score);

            // greedy の score が best_score*1.1 よりも大きければ採用しない
            if (score > best_score * 1.1) {
                continue;
            }

            // 2-opt
            // スコアが改善しない場合も確率的に採用
            int count = 0;
            for (int k = 0; k < 50000000; k++) {
                int i = rand() % cities_num;
                int j = rand() % cities_num;
                if (i == j) {
                    continue;
                }

                swap(i, j, route);
                double new_score = calc_total_distance(cities, route, cities_num);

                if (new_score < score || pow(alpha, (new_score - score)) > (double)rand() / RAND_MAX) {
                    score = new_score;
                } else {
                    swap(i, j, route);
                }

                if (k % 500000 == 0 && k > 0) {
                    printf("%d: %lf\n", k, score);
                }
            }

            if (score < best_score) {
                best_score = score;
                for (int i = 0; i < cities_num; i++) {
                    best_route[i] = route[i];
                }
            }
        }

        // 結果を出力
        char output_filename[256];
        int num = globbuf.gl_pathv[i][strlen(globbuf.gl_pathv[i]) - 5] - '0';
        sprintf(output_filename, "../week5/google-step-tsp/output_%d.csv", num);
        write_cities(best_route, cities_num, output_filename);
        printf("%s's score: %lf\n", output_filename, best_score);
    }
    globfree(&globbuf);

    return 0;
}