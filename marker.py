import cv2
from cv2 import aruco
import os
import numpy as np


class CameraSearch:
    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()
    file_name = 'picture/field.jpg'
    dir_path = 'C:/Users/spea5/python/CreativeEngineering/picture'
    basename = 'field'

    def __init__(self, cameraID):
        self.cap = cv2.VideoCapture(cameraID)
        self.enemy_point = []
        self.me_point = []

    def get_frame(self):
        _, frame = self.cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return frame

    def marker_search(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ARマーカー検知
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters)

        # 検知箇所を画像にマーキング
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        # 検知したマーカーの角の座標とidを保存
        self.marker_corners = corners
        self.marker_ids = np.ravel(ids)

        return frame_markers

    def get_filed_corners(self):  # フィールドの対角の２点の角の座標を得る
        img = cv2.imread(self.file_name)
        self.marker_search(img)
        ids = self.marker_ids
        filed_corners = []
        for id in range(2):
            if id in ids:
                index = np.where(ids == id)[0][0]
                cornerUL = self.marker_corners[index][0][0]
                filed_corners.append(cornerUL)

        self.filed_corners = filed_corners

    def get_robot_point(self):  # filed上の味方と敵のロボットを検知
        defenceID = 3
        attackID = 2

        self.defence_point = self.__get_marker_center_point(defenceID)
        self.attack_point = self.__get_marker_center_point(attackID)

    def __get_marker_center_point(self, id):
        ids = self.marker_ids
        corners = self.marker_corners

        if id in ids:
            index = np.where(ids == id)[0][0]
            cornerUL = corners[index][0][0]
            cornerBR = corners[index][0][2]

            center = [(cornerUL[0]+cornerBR[0])/2, (cornerUL[1]+cornerBR[1])/2]

            return center

        return None

    def camera_to_field(self, camera_point):
        cornerUL = self.filed_corners[0]
        cornerBR = self.filed_corners[1]
        field_point = []

        # x座標とy座標の１マス当たりのpixel
        div_x = (cornerBR[0] - cornerUL[0]) / 6.0
        div_y = (cornerBR[1] - cornerUL[1]) / 6.0

        # 型の判定
        if camera_point != None:
            # x座標とy座標の変換
            x = int((camera_point[0] - cornerUL[0]) / div_x)
            y = int((camera_point[1] - cornerUL[1]) / div_y)
        else:
            x = 0
            y = 0

        field_point.append(x)
        field_point.append(y)

        return field_point

    def show_capture(self, frame):
        cv2.imshow('frame', frame)

    def save_frame(self, ext='jpg', delay=1):
        if not self.cap.isOpened():
            return

        os.makedirs(self.dir_path, exist_ok=True)
        base_path = os.path.join(self.dir_path, self.basename)

        n = 0
        while True:
            frame = self.get_frame()
            self.show_capture(frame)
            key = cv2.waitKey(delay) & 0xFF
            if key == ord('c'):
                file_name = '{}.{}'.format(base_path, ext)
                cv2.imwrite(file_name, frame)
                n += 1
            elif key == ord('q'):
                break

        cv2.destroyAllWindows()
