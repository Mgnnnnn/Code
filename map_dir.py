def AngleTransform(Curdir, RotateDir):
    if Curdir == 90:
        if RotateDir == 'left':
            angle = 90
        elif RotateDir == 'right':
            angle = - 90
        elif RotateDir == 'forward':
            angle = 0
        else:
            angle = 180

    elif Curdir == -90:
        if RotateDir == 'left':
            angle = - 90
        elif RotateDir == 'right':
            angle = 90
        elif RotateDir == 'forward':
            angle = 0
        else:
            angle = 180

    elif Curdir == 180:
        if RotateDir == 'left':
            angle = 90
        elif RotateDir == 'right':
            angle = - 90
        elif RotateDir == 'forward':
            angle = 0
        else:
            angle = 180
    else:
        if RotateDir == 'left':
            angle = 90
        elif RotateDir == 'right':
            angle = - 90
        elif RotateDir == 'forward':
            angle = 0
        else:
            angle = 180

    return angle



def rotaMat(coordXY, DirVec, theta, distance):
    M = np.mat([[np.cos(theta * np.pi/180), -1 * np.sin(theta * np.pi/180)], \
        [np.sin(theta * np.pi/180), np.cos(theta * np.pi/180)]])

    ChangedDirVec = np.ravel(np.dot(M, DirVec))
    ChangedDirVec[0], ChangedDirVec[1] = int(ChangedDirVec[0]), int(ChangedDirVec[1])

    coordXY += ChangedDirVec * distance
    return coordXY, ChangedDirVec 



# a1 坐标
a1 = [1, 1]
# a1 方向向量
a1_dirvec = [0, 1]

# 逆时针旋转90度, 行进距离5
a2, a2_dirvec = rotaMat(a1, a1_dirvec, 90, 5)

print(a2, a2_dirvec)