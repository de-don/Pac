__author__ = 'Denis & Artem'

def LenV(v1, v2, Vertex):
    return int(((Vertex[v1][0]-Vertex[v2][0])**2+(Vertex[v1][1]-Vertex[v2][1])**2)**.5)

file = [i.strip() for i in open("input.txt", "r")]
N = int(file[0]) # кол-во вершин
M = int(file[N+1]) # кол-во ребер
Names = [s.split()[0] for s in file[1:1+N]]

#  считываем вершины
Vertex = dict.fromkeys(Names, (0,0))
for i in range(1,N+1):
    v, x, y = file[i].split(' ')
    Vertex[v] = (int(x), int(y))

# считываем карту
City = {name: dict() for name in Names}
for i in range(N+2, N+2+M):
    v1, v2 = file[i].split()
    City[v1].update([(v2, LenV(v1, v2, Vertex))])

for k,v in City.items():
    print(k, v)

# переменная для хранения весов
Weight = dict()
"""
Ключ словаря - кортеж (v1,v2,v3)
v1 - наша текущая вершина
v2 - следующая вершина
v3 - куда держим путь
Значение словаря - float - вес
"""
def GetWeight(v1, v2, v3):
    return Weight.get((v1, v2, v3), 0)

