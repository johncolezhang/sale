import numpy as np

m = int(input("Input M:"))
# random a m*m 0-1 matrix
treasure = np.array(list(map(lambda x: 0 if x < 0.5 else 1, np.random.rand(m * m)))).reshape((m, m))


n = int(input("Input N:"))
# random a n*n 0-1 matrix
map = np.array(list(map(lambda x: 0 if x < 0.5 else 1, np.random.rand(n * n)))).reshape((n, n))


treasure_90 = np.rot90(treasure) #counter clockwise 90 degree
treasure_180 = np.rot90(treasure_90) #counter clockwise 180 degree
treasure_270 = np.rot90(treasure_180) #counter clockwise 270 degree

print("0 degree\n", treasure)
print("90 degree\n", treasure_90)
print("180 degree\n", treasure_180)
print("270 degree\n", treasure_270)


def convolution(map, n, treasure, m):
    for i in range(n - m + 1): #小矩阵在大矩阵里纵向移动n-m+1次
        for j in range(n - m + 1): #小矩阵在大矩阵里横向移动n-m+1次
            flag = 1
            # 小矩阵左上角移动到大矩阵的i，j位置时，判断小矩阵与大矩阵是否相同
            for k in range(m):
                for l in range(m):
                    if treasure[k, l] != map[i + k, j + l]:
                        #有一个位置值不同，则flag=0
                        flag = 0
            # 如果flag=1说明匹配成功，返回左上角坐标
            if flag == 1:
                return i, j
    return -1, -1


# 旋转的4种情况都去匹配一遍
row, column = convolution(map, n, treasure, m)
print("0 degree", row, column)
row_90, column_90 = convolution(map, n, treasure_90, m)
print("90 degree", row_90, column_90)
row_180, column_180 = convolution(map, n, treasure_180, m)
print("180 degree", row_180, column_180)
row_270, column_270 = convolution(map, n, treasure_270, m)
print("270 degree", row_270, column_270)

if row == -1 and row_90 == -1 and row_180 == -1 and row_270 == -1:
    print("match fail")


