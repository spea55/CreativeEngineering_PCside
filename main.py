import time
import cv2
import random

import marker
import atk_maze as atk
import maze as df
import send_data as sd


def run_argolism(point:list, mode):
    # 移動情報取得
    print('me', point[0])
    print('goal', point[1])
    me = point_for_argolism(point[0])
    goal = point_for_argolism(point[1])

    if me == goal:
        return 0, [], []

    if mode == 0:
        # goal_maze = point_for_argolism(goal)
        k, drc, dis = maze.defence(me, goal)

    else:
        k, drc, dis = maze.defence(me, goal)

    return k, drc, dis


def point_for_argolism(points):
    point = [0, 0]
    for i in range(len(points)):
        point[i] = points[i]*2 + 1

    return point


if __name__ == '__main__':
    # 初期化
    count = 0
    cameraID = 0
    camera = marker.CameraSearch(cameraID)
    enemy = []
    goal_list = ((5, 0), (4, 4), (1, 4), (2, 1))

    # bbbとbluetooth通信開始
    # bt = sd.bluetooth()

    mode = int(input('mode 0:attack 1:defence :'))
    # if mode == 0:
    #     maze = atk
    # elif mode == 1:
    maze = df

    camera.save_frame()
    camera.get_filed_corners()
    print(camera.filed_corners)

    print(goal_list)
    while True:
        time.sleep(0.1)
        if not camera.cap.isOpened():
            print('connot get frame')
            continue
        # frame = camera.get_frame()
        # frame_markers = camera.marker_search(frame)
        img = cv2.imread(camera.file_name)
        frame_markers = camera.marker_search(img)
        camera.get_robot_point()

        camera.show_capture(frame_markers)

        print('me', camera.attack_point)

        if mode == 0:  # me:attack enemy:defence
            if camera.attack_point != None:
                # randomな値を取得
                rand = random.randrange(0, 3)
                if count == 0:  # 最初のループのみ実行
                    # 自分の座標をカメラで取った座標に
                    me = camera.camera_to_field(camera.attack_point)
                else:  # 2回目以降のループ
                    # cameraで取った自分の座標と敵の座標(目的座標)が同じかどうか
                    if camera.camera_to_field(camera.attack_point) == goal:
                        # True:自分の座標を前のgoalの座標に
                        me = goal
                    else:
                        # False:自分の座標をカメラで取った座標に
                        me = camera.camera_to_field(camera.attack_point)
                #　ゴール座標をあらかじめ決めたゴール座標のリストからランダムに取得
                goal = goal_list[rand]
                data = [me, goal]
            else:
                continue
        elif mode == 1:  # me:defence enemy:attack
            if camera.defence_point != None:
                # 前の敵の座標を保持
                pre_enemy_point = enemy
                # 敵の座標更新
                enemy = camera.camera_to_field(camera.attack_point)
                if count == 0:  # 最初のループのみ実行
                    # 自分の座標をカメラで取った座標に
                    me = camera.camera_to_field(camera.defence_point)
                    # 最初はここに向かう(敵の座標をゴール座標にするためenemyを更新)
                    enemy = [3, 3]
                else:  # 2回目以降のループ
                    # cameraで取った自分の座標と敵の座標(目的座標)が同じかどうか
                    if camera.camera_to_field(camera.defence_point) == enemy:
                        # True:自分の座標を前の敵の座標に
                        me = pre_enemy_point
                    else:
                        # False:自分の座標をカメラで取った座標に
                        me = camera.camera_to_field(camera.defence_point)
                data = [me, enemy]
            else:
                continue

        if count == 400 or count == 0:
            count = 0
            print(goal_list)
            num, drc, dis = run_argolism(data, mode)
            if num == 0:
                continue
            else:
                print('send data')
                # if bt.read_flag():
                # bt.serial_send_data(drc, dis)
                # else:
                #     pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            camera.cap.release()
            break

        count += 1
