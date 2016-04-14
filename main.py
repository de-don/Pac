import operator
import random

__author__ = 'Denis & Artem'


class City:
    N = 0  # кол-во вершин
    M = 0  # кол-во ребер
    Vertex = dict()  # Вершины
    City = dict()  # Карта
    Names = list()  # Названия вернищ
    Weight = dict()  # переменная для хранения весов
    Now = 0  # Текущее положение
    Lucky = 1 / 5  # удача (вероятность пойти по направлению)
    """
    Ключ словаря - кортеж (v1,v2,v3)
    v1 - наша текущая вершина
    v2 - следующая вершина
    v3 - куда держим путь
    Значение словаря - float - вес
    """

    def max_width(self):
        return max(self.Vertex.values(), key=operator.itemgetter(0))[0]

    def max_heigth(self):
        return max(self.Vertex.values(), key=operator.itemgetter(1))[1]

    def distance(self, v1, v2):
        return int(
            ((self.Vertex[v1][0] - self.Vertex[v2][0]) ** 2 + (self.Vertex[v1][1] - self.Vertex[v2][1]) ** 2) ** .5)

    def __init__(self, fname="input_big_1.txt", rev=1):
        file = [i.strip() for i in open(fname, "r")]
        self.N = int(file[0])
        self.M = int(file[self.N + 1])
        self.Names = [s.split()[0] for s in file[1:1 + self.N]]

        #  считываем вершины
        self.Vertex = dict.fromkeys(self.Names, (0, 0))
        for i in range(1, self.N + 1):
            v, x, y = file[i].split(' ')
            self.Vertex[v] = (int(x), int(y))

        # считываем карту
        self.City = {name: dict() for name in self.Names}
        for i in range(self.N + 2, self.N + 2 + self.M):
            v1, v2 = file[i].split()
            self.City[v1].update([(v2, self.distance(v1, v2))])
            if rev:
                self.City[v2].update([(v1, self.distance(v1, v2))])

        for k, v in self.City.items():
            print(k, v)

    def GetWeight(self, v1, v2, v3):
        return self.Weight.get((v1, v2, v3), 0)

    def GoTo(self, pTo, pFrom=None, Way=[]):
        Way.append(pFrom)

        if pFrom == pTo:
            return Way

        if pFrom is None:
            pFrom = self.Now

        # Берем все смежные вершины, и убираем из них уже посещенные
        #  Для каждой вершины вытаскиваем из базы вес
        arr = {k: self.GetWeight(pFrom, k, pTo) for k, _ in self.City[pFrom].items() if k not in Way}

        if not arr:
            return 0

        # Сортировка по значению с сохранением ключей
        arr = sorted(arr.items(), key=operator.itemgetter(1), reverse=True)

        #  Если все элементы с нулевым весом - перемешиваем
        if arr[0][1] == 0:
            random.shuffle(arr)

        # Если повезло - ориентируемся и идем в правильную сторону
        if random.randint(1, int(1 / self.Lucky)) == 1:
            arr = {k: self.distance(k, pTo) for k, _ in arr}
            arr = sorted(arr.items(), key=operator.itemgetter(1))

        # Идем в каждую вершину по порядку, рекурсией, пока не будет возвращено 1
        for k, _ in arr:
            W = self.GoTo(pTo, k, Way[:])
            if W:
                return W
        Way.pop()
        return 0

    def UpdateWeight(self, Way):
        #  Обновляем веса

        for i in range(len(Way) - 1):
            pTo = Way[-i]

            for i in range(1, len(Way) - i):
                k = (Way[i - 1], Way[i], pTo)
                v = self.Weight.get(k, 0)
                v = [v * 1.1, 1][v == 0]
                self.Weight.update({k: v})


# для отладки
if __name__ == '__main__':

    T = City()

    max = len(T.Names) - 1
    r = random.randint(0, max)
    Now = T.Names[r]

    for i in range(1000):
        r = random.randint(0, max)
        To = T.Names[r]

        if (Now != To):
            W = T.GoTo(pFrom=Now, pTo=To, Way=[])
            print(Now, "=>", To, W)
            T.UpdateWeight(W)
            Now = To

    print(T.Weight)
