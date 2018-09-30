from fractions import Fraction
import copy

mtrx1 = [[ 2,  1, -2],
        [-2, -2,  1],
        [ 5,  1,  1],
        [ 0,  1, -1]]
'''
mtrx1 = [[ 3,  3, 1, 1],
        [ 8, 1,  2, 0],
        [ 1,  0,  0.5, 2],
        [ 0,  -2, -6, -7]]
'''
mtrx1 = [[Fraction(mtrx1[i][j]) for j in range(len(mtrx1[0]))] for i in range(len(mtrx1))]

varlist1 = [['s0', 'x1', 'x2'],
            ['x3', 'x4', 'x5', 'F']]
'''
varlist1 = [['s0', 'x1', 'x2', 'x3'],
            ['x4', 'x5', 'x6', 'F']]
'''

def solve_simplex(mtrx, varlist):
    stage1 = True #Флаг окончания этапа 1
    stage2 = True #Флаг окончания этапа 2
    n = len(mtrx) #Количество строк симплекс-таблицы
    m = len(mtrx[0]) #Количество столбцов симплекс-таблицы
    r = -1 #Номер разрешающей строки
    k = -1 #Номер разрешающего столбца
    answer = {'error1': 'None', #Ошибка на 1-м этапе
            'error2': 'None', #Ошибка на 2-м этапе
            'mtrx1': [], #Промежуточные симплек-таблицы этапа 1
            'vlst1': [],
            'mtrx2': [], #Промежуточные симплек-таблицы этапа 2
            'vlst2': [] }
    #Первоначальная симплекс таблица
    addmtrx = copy.deepcopy(mtrx)
    addmtrx.insert(0, varlist[0])
    for i in range(0, n):
        addmtrx[i+1].insert(0, varlist[1][i])
    answer['mtrx1'].append(addmtrx)
    #Этап №1. Поиск опорного решения
    while(stage1):
        stage1 = False
        for i in range(n-1):
            #Поиск отрицательного элемента в столбце свободных членов
            if mtrx[i][0] < 0:
                stage1 = True
                #Поиск разрешающего столбца
                for j in range(1, m):
                    if mtrx[i][j]<0:
                        k = j
                        break
                #Если не нашли отрицательного элемента, то решений нет
                else:
                    answer['error1'] = 'Нет допустимых решений.'
                    return answer
                #Поиск разрешающей строки
                searchlist = []
                for a in range(n-1):
                    if mtrx[a][k]!=0:
                        searchlist.append(mtrx[a][0] / mtrx[a][k])
                    else:
                        searchlist.append(-1)                
                r = sorted([(index, value) for (index, value) in enumerate(searchlist) if value > 0], key=lambda x: x[1])[0][0]
                #Замена переменных
                temp = varlist[0][k]
                varlist[0][k] = varlist[1][r]
                varlist[1][r] = temp
                newmtrx = [[0 for a in range(m)] for b in range(n)]
                #Пересчёт симплекс-таблицы
                for x in range(n):
                    for y in range(m):
                        if (x!=r and y!=k):
                            newmtrx[x][y] = mtrx[x][y] - mtrx[x][k] * mtrx[r][y] / mtrx[r][k]
                        elif (x==r and y!=k):
                            newmtrx[x][y] = mtrx[r][y] / mtrx[r][k]                  
                        elif (x!=r and y==k):
                            newmtrx[x][y] = - mtrx[x][k] / mtrx[r][k]
                        elif (x==r and y==k):
                            newmtrx[x][y] = 1 / mtrx[x][y]  
                mtrx = newmtrx
                addmtrx = copy.deepcopy(mtrx)
                addmtrx.insert(0, varlist[0])
                for i in range(0, n):
                    addmtrx[i+1].insert(0, varlist[1][i])
                answer['mtrx1'].append(addmtrx)
                break
    #Этап №2. Поиск оптимального решения
    while(stage2):
        stage2 = False
        for j in range(1, m):
            #Поиск разрешающего столбца
            if mtrx[n-1][j] > 0:
                stage2 = True
                k = j
                for i in range(n-1):
                    if mtrx[i][k] > 0:
                        break
                else:
                    answer['error2'] = 'Не существует оптимального решения.'
                    return answer
                #Поиск разрешающей строки
                searchlist = []
                for a in range(n-1):
                    if mtrx[a][k]!=0:
                        searchlist.append(mtrx[a][0] / mtrx[a][k])
                    else:
                        searchlist.append(-1)
                r = sorted([(index, value) for (index, value) in enumerate(searchlist) if value > 0], key=lambda x: x[1])[0][0]
                #Замена переменных
                temp = varlist[0][k]
                varlist[0][k] = varlist[1][r]
                varlist[1][r] = temp
                newmtrx = [[0 for a in range(m)] for b in range(n)]
                #Пересчёт симплекс-таблицы
                for x in range(n):
                    for y in range(m):
                        if (x!=r and y!=k):
                            newmtrx[x][y] = mtrx[x][y] - mtrx[x][k] * mtrx[r][y] / mtrx[r][k]
                        elif (x==r and y!=k):
                            newmtrx[x][y] = mtrx[r][y] / mtrx[r][k]                  
                        elif (x!=r and y==k):
                            newmtrx[x][y] = - mtrx[x][k] / mtrx[r][k]
                        elif (x==r and y==k):
                            newmtrx[x][y] = 1 / mtrx[x][y]  
                mtrx = newmtrx  
                addmtrx = copy.deepcopy(mtrx)
                addmtrx.insert(0, varlist[0])
                for i in range(0, n):
                    addmtrx[i+1].insert(0, varlist[1][i])
                answer['mtrx2'].append(addmtrx)
                break
    return answer


res = solve_simplex(mtrx1, varlist1)

print('stage 1')
for s1 in res['mtrx1']:
    for a in s1:
        print(' '.join([str(el) for el in a]))
print('stage2')
for s2 in res['mtrx2']:
    for a in s2:
        print(' '.join([str(el) for el in a]))

vb = dict([[row[0], str(row[1])] for row in res['mtrx2'][-1] if row[0]!='s0'])
print(vb)
sol = {}
for i in range(1, len(mtrx1[0])+1):
    sol['x{}'.format(i)] = vb.get('x{}'.format(i), '0')
sol['F'] = vb['F']
print(sol.items())

