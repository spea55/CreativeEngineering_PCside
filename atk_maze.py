import copy

POINT_MAX = 999999

MEIRO_WIDTH = 13
MEIRO_HEIGHT = 13
# 迷路サイズ

PATH = 0
WALL = 1
GOAL = 2
PASSED = 3

sum = 0


def army(maze_now):
    # 敵から1マス:6 2マス:7
    for i in range(6):
        for j in range(6):
            if maze_now == 5:
                continue

            for y in range(-2, 3):
                for x in range(-2, 3):
                    if y != 0 or x != 0:
                        if not(i+y < 0 or i+y > 5 or j+x < 0 or j+x > 5):
                            amy = maze_now[i+y][j+x]

                            if amy == 5:
                                if x == 2 or y == 2 or x == -2 or y == -2:
                                    maze_now[i][j] = 7
                                else:
                                    maze_now[i][j] = 6
    return maze_now


def summ(maze, maze_now, i, j):
    global sum
    l = 0
    # 上

    # 上
    if maze[j-1][i] == PASSED:

        while 1:
            l += 1
            if not(maze[j-l][i] == PASSED):
                break
            if l % 2 == 0:
                sum += maze_now[i//2][(j-l)//2]

        maze[j-l+2][i] = WALL
        summ(maze, maze_now, i, j-l+1)
    # 下
    if maze[j+1][i] == PASSED:
        while 1:
            l += 1
            if not(maze[j+l][i] == PASSED):
                break
            if l % 2 == 0:
                sum += maze_now[i//2][(j+l)//2]

        maze[j+l-2][i] = WALL
        summ(maze, maze_now, i, j+l-1)
     # 右
    if maze[j][i+1] == PASSED:
        while 1:
            l += 1
            if not(maze[j][i+l] == PASSED):
                break
            if l % 2 == 0:
                sum += maze_now[(i+l)//2][j//2]

        maze[j][i+l-2] = WALL
        summ(maze, maze_now, i+l-1, j)
    # 左
    if maze[j-1][i] == PASSED:
        while 1:
            l += 1
            if not(maze[j][i-l] == PASSED):
                break
            if l % 2 == 0:
                sum += maze_now[(i-l)//2][j//2]

        maze[j][i-l+2] = WALL
        summ(maze, maze_now, i-l+1, j)
    return sum


def move(i, j, GOALL, maze, maze_res, maze_now, START):
    global POINT_MAX

    if i < 0 or i >= MEIRO_WIDTH or j < 0 or j >= MEIRO_HEIGHT:
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

                if maze[nj][ni] == GOAL:
                    maze_kakashi = copy.deepcopy(maze)
                    sum = 0
                    sum = summ(maze, maze_now, START[0], START[1])
                    print_keiro(maze)
                    if sum < POINT_MAX:
                        POINT_MAX = sum
                        # print(maze2[GOAL_X][GOAL_Y])
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze_kakashi[a][b]
                move(ni, nj, GOALL, maze, maze_res, maze_now, START)

    # 下
    ni = i
    nj = j+1
    if nj < MEIRO_HEIGHT:
        if not(maze[nj][ni] == WALL):
            if not(maze[nj][ni] == PASSED):

                if maze[nj][ni] == GOAL:
                    maze_kakashi = copy.deepcopy(maze)
                    sum = 0
                    sum = summ(maze, maze_now, START[0], START[1])
                    print_keiro(maze)
                    if sum < POINT_MAX:
                        POINT_MAX = sum
                        # print(maze2[GOAL_X][GOAL_Y])
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze_kakashi[a][b]
                move(ni, nj, GOALL, maze, maze_res, maze_now, START)
    # 左
    ni = i-1
    nj = j
    if ni >= 0:
        if not(maze[nj][ni] == WALL):
            if not(maze[nj][ni] == PASSED):

                if maze[nj][ni] == GOAL:
                    maze_kakashi = copy.deepcopy(maze)
                    sum = 0
                    sum = summ(maze, maze_now, START[0], START[1])
                    print_keiro(maze)
                    if sum < POINT_MAX:
                        POINT_MAX = sum
                        # print(maze2[GOAL_X][GOAL_Y])
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze_kakashi[a][b]
                move(ni, nj, GOALL, maze, maze_res, maze_now, START)

    # 右
    ni = i+1
    nj = j
    if ni < MEIRO_WIDTH:
        if not(maze[nj][ni] == WALL):
            if not(maze[nj][ni] == PASSED):

                if maze[nj][ni] == GOAL:
                    maze_kakashi = copy.deepcopy(maze)
                    sum = 0
                    sum = summ(maze, maze_now, START[0], START[1])
                    print_keiro(maze)
                    if sum < POINT_MAX:
                        POINT_MAX = sum
                        # print(maze2[GOAL_X][GOAL_Y])
                        for a in range(13):
                            for b in range(13):
                                maze_res[a][b] = maze_kakashi[a][b]
                move(ni, nj, GOALL, maze, maze_res, maze_now, START)

    maze[j][i] = 0


def rute(i, j, drc, dis, maze_res):

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
        rute(i, j-l+1, drc, dis, maze_res)
    # 下
    if maze_res[j+1][i] == PASSED:
        drc.append(2)
        while 1:
            l += 1
            if not(maze_res[j+l][i] == PASSED):
                break
        dis.append((l-1)//2)
        maze_res[j+l-2][i] = WALL
        rute(i, j+l-1, drc, dis, maze_res)
     # 右
    if maze_res[j][i+1] == PASSED:
        drc.append(3)
        while 1:
            l += 1
            if not(maze_res[j][i+l] == PASSED):
                break
        dis.append((l-1)//2)
        maze_res[j][i+l-2] = WALL
        rute(i+l-1, j, drc, dis, maze_res)
    # 左
    if maze_res[j][i-1] == PASSED:
        drc.append(4)
        while 1:
            l += 1
            if not(maze_res[j][i-l] == PASSED):
                break
        dis.append((l-1)//2)
        maze_res[j][i-l+2] = WALL
        rute(i-l+1, j, drc, dis, maze_res)


def print_keiro(maze_res):
    print('ポイント', sum)

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


def print_youso(k, drc, dis):
    for i in range(k):
        if drc[i] == 1:
            print(i+1, '=上方向', ',距離', dis[i], 'マス', sep='')
        elif drc[i] == 2:
            print(i+1, '=下方向', ',距離', dis[i], 'マス', sep='')
        elif drc[i] == 3:
            print(i+1, '=右方向', ',距離', dis[i], 'マス', sep='')
        elif drc[i] == 4:
            print(i+1, '=左方向', ',距離', dis[i], 'マス', sep='')


def attack(start, goal, enemy):
    start = []
    goal = []
    # スタート＆ゴール座標
    for i in range(2):
        start.append(int(input()))
    for i in range(2):
        goal.append(int(input()))

    drc = []
    dis = []

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

    # 現在の得点状況 3:通過済み 5:敵
    maze_now = [
        [0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 3, 3, 3, 0, 0],
        [0, 0, 0, 3, 0, 0],
        [3, 3, 3, 3, 0, 0],
    ]

    maze_res = copy.deepcopy(maze)
    maze[goal[1]][goal[0]] = GOAL

    # 敵の周囲２マスを危険地帯に設定
    maze_now = army(maze_now)
    print(maze_now)
    move(start[0], start[1], goal, maze, maze_res, maze_now, start)
    print_keiro(maze_res)
    rute(start[0], start[1], drc, dis, maze_res)
    k = len(dis)

    print_youso(k, drc, dis)
    return k, drc, dis

if __name__ == '__main__':
    attack()
