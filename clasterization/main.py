#
# Выполнил Карманов Сергей и Лейманн Валерий
#

from csv import reader
from random import uniform
from copy import deepcopy

# Количество кластеров
k = 3
# Количество параметров
n = 4
# Заполнение списка начальными данными
data = []
with open ("iris.csv") as file:
        content = reader(file)
        for row in content:
            for i in range(0, n):
                row[i] = float(row[i])
            data.append(row)

# Нахождение максимального и минимального значений параметров
min_list = [min(item[i] for item in data) for i in range(n)]
max_list = [max(item[i] for item in data) for i in range(n)]

# Случайная генерация центроидов
centroids = [[ uniform(min_list[j], max_list[j]) for j in range(n)] for i in range(k)]
# Создание пустого списка кластеров
clusters_list = [[] for i in range(k)]

# Переменная для завершения цикла 
end = False
#Копируем список центроидов для того, чтобы позже сравнить текущие значения с предыдущими
previous_centroids = deepcopy(centroids)
# Цикл будет завершён тогда, когда текущие центроиды совпадут с предыдущими
while not end:

    # Цикл с проверкой количества кластеров, если один из кластеров будет пустым, центроиды будут сгенерированы заново и цикл повторится
    clusters_is_null = True
    while clusters_is_null:
        clusters_is_null = False
        for item in data:
            cluster_index = -1
            # Рассчёт Евклидовых расстояний между точкой и центроидами
            min_distance = float('inf')
            for i in range(k):
                distance = 0
                for j in range(n):
                    distance += (item[j] - centroids[i][j])**2
                distance = distance**(1/2)
                # Выбор минимального расстояния
                if min_distance > distance:
                    min_distance = distance
                    cluster_index = i
            # Добавление точки в кластер
            clusters_list[cluster_index].append(item)
        # Если один из кластеров пуст
        for item in clusters_list:
            if (len(item) == 0):
                # Центроиды генерируются заново
                centroids = [[ uniform(min_list[j], max_list[j]) for j in range(n)] for i in range(k)]
                clusters_is_null = True
                # Кластеры очищаются
                clusters_list = [[] for i in range(k)]
    
    # Рассчёт новых центров кластеров
    for i in range(k):
        for j in range(n):
            avg_param = 0
            for item in clusters_list[i]:
                avg_param += item[j]
            if len(clusters_list[i]) != 0:
                avg_param = avg_param / len(clusters_list[i])
            centroids[i][j] = avg_param

    # Если текущие и предыдущие центроиды равны цикл завершается
    if centroids == previous_centroids:
        end = True     
    else:
        # Иначе предыдущие значения центроидов перезаписываются
        previous_centroids = deepcopy(centroids)
        # и кластеры очищаются
        clusters_list = [[] for i in range(k)]

# Определение доминирующих сортов в кластерах
sort_list = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
index_list = []
for i in range(k):
    count_list = [0 for i in range(k)]
    for item in clusters_list[i]:
        for j in range(k):
            if item[n] == sort_list[j]:
                count_list[j] += 1
    index = count_list.index(max(count_list))
    index_list.append(index)

# Переменная для подсчета количества неверно определённых сортов
incorrect = 0
# Вывод
print("\nКластеризация методом k-средних")
for i in range(k):
    sort = sort_list[index_list[i]]
    print("\n\tСорт ", sort)
    for item in clusters_list[i]:
        print(item)
        if item[n] != sort:
            incorrect += 1
# Подсчет процента неверно определённых сортов
print("\nПроцент неверно определенных сортов: ", round((incorrect / len(data)) * 100, 1), "%")
