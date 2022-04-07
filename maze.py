import copy

DEP_MIN = 1000

MAZE_WIDTH = 13
MAZE_HEIGHT = 13
# 迷路サイズ

PATH = 0
WALL = 1
GOAL = 2
PASSED = 3


def move(i, j, GOAL_X, GOAL_Y, maze, maze2, maze_res):
    global DEP_MIN

    if i < 0 or i >= MAZE_WIDTH or j < 0 or j >= MAZE_HEIGHT:
        return
    if maze[j][i] == GOAL:
        return
    maze[j][i] = PASSED

    # 上
    ni = i
    nj = j-1
    if nj >= 0:
        if not(maze[nj][ni] == WALL):
            if not(maze[nj][ni] == PASSED):
                maze2[ni][nj] = maze2[ni][nj+1]+1

                if maze[nj][ni] == GOAL:
                    # print_rote()
                    if maze2[GOAL_X][GOAL_Y] < DEP_MIN:
                        DEP_MIN = maze2[GOAL_X][GOAL_Y]
                        # print(maze2[GOAL_X][GOAL_Y])
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze[a][b]
                move(ni, nj, GOAL_X, GOAL_Y, maze, maze2, maze_res)

    # 下
    ni = i
    nj = j+1
    if nj < MAZE_HEIGHT:
        if not(maze[nj][ni] == WALL):
            if not(maze[nj][ni] == PASSED):
                maze2[ni][nj] = maze2[ni][nj-1]+1

                if maze[nj][ni] == GOAL:
                    # print_rote()
                    if DEP_MIN > maze2[GOAL_X][GOAL_Y]:
                        DEP_MIN = maze2[GOAL_X][GOAL_Y]
                        # print(maze2[GOAL_X][GOAL_Y])
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze[a][b]
                move(ni, nj, GOAL_X, GOAL_Y, maze, maze2, maze_res)
    # 左
    ni = i-1
    nj = j
    if ni >= 0:
        if not(maze[nj][ni] == WALL):
            if not(maze[nj][ni] == PASSED):
                maze2[ni][nj] = maze2[ni+1][nj]+1

                if maze[nj][ni] == GOAL:
                    # print_rote()
                    if DEP_MIN > maze2[GOAL_X][GOAL_Y]:
                        DEP_MIN = maze2[GOAL_X][GOAL_Y]
                        # print(maze2[GOAL_X][GOAL_Y])
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze[a][b]
                move(ni, nj, GOAL_X, GOAL_Y, maze, maze2, maze_res)

    # 右
    ni = i+1
    nj = j
    if ni < MAZE_WIDTH:
        if not(maze[nj][ni] == WALL):
            if not(maze[nj][ni] == PASSED):
                maze2[ni][nj] = maze2[ni-1][nj]+1

                if maze[nj][ni] == GOAL:
                    # print_rote()
                    if DEP_MIN > maze2[GOAL_X][GOAL_Y]:
                        DEP_MIN = maze2[GOAL_X][GOAL_Y]
                        # print(DEP_MIN)
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze[a][b]
                move(ni, nj, GOAL_X, GOAL_Y, maze, maze2, maze_res)

    maze[j][i] = 0


def rote(i, j, drc:list, dis:list, maze, maze2, maze_res):

    l = 0

    # 上
    if maze_res[j-1][i] == PASSED:
        drc.append(1)
        while 1:
            l += 1
            if not(maze_res[j-l][i] == PASSED):
                break
        dis.append((l-1)//2)
        maze_res[j-l+2][i] = WALL
        rote(i, j-l+1, drc, dis, maze, maze2, maze_res)
    # 下
    if maze_res[j+1][i] == PASSED:
        drc.append(2)
        while 1:
            l += 1
            if not(maze_res[j+l][i] == PASSED):
                break
        dis.append((l-1)//2)
        maze_res[j+l-2][i] = WALL
        rote(i, j+l-1, drc, dis, maze, maze2, maze_res)
    # 右
    if maze_res[j][i+1] == PASSED:
        drc.append(3)
        while 1:
            l += 1
            if not(maze_res[j][i+l] == PASSED):
                break
        dis.append((l-1)//2)
        maze_res[j][i+l-2] = WALL
        rote(i+l-1, j, drc, dis, maze, maze2, maze_res)
    # 左
    if maze_res[j][i-1] == PASSED:
        drc.append(4)
        while 1:
            l += 1
            if not(maze_res[j][i-l] == PASSED):
                break
        dis.append((l-1)//2)
        maze_res[j][i-l+2] = WALL
        rote(i-l+1, j, drc, dis, maze, maze2, maze_res)


def print_rote(maze_res):
    print(DEP_MIN, '手')

    for i in range(13):
        for j in range(13):
            if maze_res[i][j] == PATH:
                print(' ', end='')
            if maze_res[i][j] == WALL:
                print('#', end='')
            if maze_res[i][j] == PASSED:
                print('o', end='')
            if maze_res[i][j] == GOAL:
                print('G', end='')
        print()
    print()


def print_index(k, drc, dis):
    for i in range(k):
        if drc[i] == 1:
            print(i+1, '=上方向', ',距離', dis[i], 'マス', sep='')
        elif drc[i] == 2:
            print(i+1, '=下方向', ',距離', dis[i], 'マス', sep='')
        elif drc[i] == 3:
            print(i+1, '=右方向', ',距離', dis[i], 'マス', sep='')
        elif drc[i] == 4:
            print(i+1, '=左方向', ',距離', dis[i], 'マス', sep='')


def defence(start, goal):
    global DEP_MIN
    DEP_MIN = 1000

    START_X = start[0]
    START_Y = start[1]
    GOAL_X = goal[0]
    GOAL_Y = goal[1]

    # START_X=int(input('START_X'))
    # START_Y=int(input('START_Y'))
    # GOAL_X=int(input('GOAL_X'))
    # GOAL_Y=int(input('GOAL_Y'))

    drc = []
    dis = []
    k = 0

    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    maze2 = copy.deepcopy(maze)
    maze_res = copy.deepcopy(maze)

    maze[GOAL_Y][GOAL_X] = GOAL
    move(START_X, START_Y, GOAL_X, GOAL_Y, maze, maze2, maze_res)

    print_rote(maze_res)
    rote(START_X, START_Y, drc, dis, maze, maze2, maze_res)

    k = len(dis)
    dis[k-1] += 1

    print_index(k, drc, dis)

    return k, drc, dis
