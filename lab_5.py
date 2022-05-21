"""С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10]. 
Формируется матрица F следующим образом: скопировать в нее А и  если в Е сумма чисел по периметру больше, чем количество нулей по периметру ,то поменять местами  В и С симметрично,
иначе В и Е поменять местами несимметрично.При этом матрица А не меняется.После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,
то вычисляется выражение: A*A^T – K * F, иначе вычисляется выражение (A^-1 +G-F^-1)*K, где G-нижняя треугольная матрица, полученная из А.Выводятся по мере формирования А, F и все матричные операции последовательно."""


import random
import time
import numpy as np

def print_matrix(M, matr_name, tt):
    print("матрица " + matr_name + ", промежуточное время = " + str(format(tt, '0.2f')) + " seconds.")
    for i in M:  # делаем перебор всех строк матрицы
        for j in i:  # перебираем все элементы в строке
            print("%5d" % j, end=' ')
        print()

print("\n-----Результат работы программы-------")
try:
    row_q = int(input("Введите количество строк (столбцов) квадратной матрицы в интервале от 6 до 100:"))
    while row_q < 6 or row_q > 100:
        row_q = int(input("Вы ввели неверное число\nВведите количество строк (столбцов) квадратной матрицы в интервале от 6 до 100:"))
        
    K = int(input("Введите число К="))
    start = time.time()
    
    A,F,AF = [],[],[]                   # задаем матрицы 
    for x in range(row_q):
        A.append([0]*row_q)
        F.append([0]*row_q)
        AF.append([0]*row_q)
        
    time_next = time.time()
    print_matrix(F, "F", time_next - start)

    for x in range(row_q):  # заполняем матрицу А
        for y in range(row_q):
            #A[x][y] = random.randint(-10, 10)
            if x < y:
                A[x][y] = 1
            elif x > y:
                A[x][y] = 2
           

    time_prev = time_next
    time_next = time.time()
    print_matrix(A,"A",time_next-time_prev)

    for x in range(row_q):  # формируем матрицу F
        for y in range(row_q):
            F[x][y] = A[x][y]
            
    time_prev = time_next
    time_next = time.time()
    print_matrix(F, "F", time_next - time_prev)

    E = []  # задаем подматрицу E
    size = row_q // 2
    for x in range(size):
        E.append([0] * size)

    for x in range(size):  # формируем подматрицу E
        for y in range(size):
            E[x][y] = F[x][y]
            
    time_prev = time_next
    time_next = time.time()
    print_matrix(E, "E", time_next - time_prev)

    # сумма чисел по периметру в подматрице E

    summa = 0

    for x in range(size):
        for y in range(size):
            if x == 0 or x == size - 1 or y == 0 or y == size - 1:
                summa += E[x][y]

    # количество нулей по периметру в подматрице E

    quantity_zeros = 0

    for x in range(size):
        for y in range(size):
            if E[x][y] == 0 and (x == 0 or x == size - 1 or y == 0 or y == size - 1):
                quantity_zeros += 1
    
        
    if summa > quantity_zeros:
        print("В подматрице E сумма чисел по периметру больше, чем количество нулей по периметру")

        # меняем B и C симметрично

        for x in range(size):  
            for y in range(row_q - size, row_q):
                F[x][y], F[row_q-x-1][y] = F[row_q-x-1][y], F[x][y] 
    else:
        print("В подматрице E количество нулей по периметру больше, чем сумма чисел по периметру")

        # меняем B и E несимметрично

        for x in range(size):  
            for y in range(size):
                F[x][y], F[x][row_q-size+y] = F[x][row_q-size+y], F[x][y]
          
    time_prev = time_next
    time_next = time.time()
    print_matrix(F, "F", time_next - time_prev)

    if np.linalg.det(A) == 0 or np.linalg.det(F) == 0:
        print("A или F вырожденая матрица,т.е вычислить нельзя")
        
    elif np.linalg.det(A) > np.trace(F):
        print("Определитель матрицы A больше, чем сумма диагональных элементов матрицы F")  # A * A^T - K * F

        AF = (np.matmul(A, np.transpose(A))) - (K * F)

        time_prev = time_next
        time_next = time.time()
        print_matrix(AF, "A * A^T - K * F", time_next - time_prev)
        
    else:
        print("Cумма диагональных элементов матрицы F больше, чем определитель матрицы A")  # (A^-1 + G - F^-1) * K
        
        G = np.tril(A) # G - нижняя треугольная матрица, полученная из матрицы A

        time_prev = time_next
        time_next = time.time()
        print_matrix(G, "G", time_next - time_prev)

        AF = K * (np.linalg.inv(A) + G - np.linalg.inv(F))

        time_prev = time_next
        time_next = time.time()
        print_matrix(AF, "(A^-1 + G - F^-1) * K", time_next - time_prev)

    finish = time.time()
    result = finish - start
    print("Program time: " + str(result) + " seconds.")
    
except ValueError:
    print("\nэто не число") 
                    
except FileNotFoundError:
    print("\nФайл text.txt в директории проекта не обнаружен.\nДобавьте файл в директорию или переименуйте существующий *.txt файл.")
