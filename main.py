import time
import cv2 as cv
from device_manager.scrcpy_adb import ScrcpyADB
from game.dengeon.game_action import GameAction
from data_const.coordinate import *
from utils.logger import logger
import threading
from functools import partial

# 移动到布万加
def move_to_bwj(adb) :
  """
  移动到布万加
  :param:
  :return:
  """
  # 委托
  print(contracts)
  adb.touch(contracts, 0.5)
  time.sleep(3)
  # 特产
  adb.touch(contracts_sidebar, 0.5)
  time.sleep(3)
  # 山脊
  adb.touch(contracts_tan, 0.5)
  time.sleep(3)
  # 自动寻路
  adb.touch(auto_move_to_sj, 0.5)
  time.sleep(20)
  # 关闭选择地下城弹窗
  adb.touch(close_select_dungeon, 0.5)
  time.sleep(1)
  # 选择布万家
  adb.touch(bwj, 0.5)
  time.sleep(1)

class Main:
    """
    主程序
    """

    def __init__(self, hero_name: str):
      self.adb = ScrcpyADB()
      self.roles = {
        '阿修罗':  {'name': 'asura', 'point': role_asura, 'next_role': '狂战士', 'map': 'bwj', 'position': 'up'},
        '狂战士': {'name': 'berserker', 'point': role_berserker, 'next_role': '圣骑士', 'map': 'bwj', 'position': 'up'},
        '圣骑士': {'name': 'paladin', 'point': role_paladin, 'next_role': '漫游枪手', 'map': 'bwj', 'position': 'up'},
        '漫游枪手': {'name': 'ranger', 'point': role_ranger, 'next_role': '枪炮师', 'map': 'bwj', 'position': 'up'},
        '枪炮师': {'name': 'launcher', 'point': role_launcher, 'next_role': '剑魔', 'map': 'bwj', 'position': 'up'},
        '剑魔': {'name': 'demon_slayer', 'point': role_demon_slayer, 'next_role': '剑豪', 'map': 'bwj', 'position': 'down'},
        '剑豪': {'name': 'vagabond', 'point': role_vagabond, 'next_role': '剑宗', 'map': 'bwj', 'position': 'down'},
        '剑宗': {'name': 'sword_master', 'point': role_sword_master, 'next_role': None, 'map': 'bwj', 'position': 'down'},



      }
      self.role = self.roles[hero_name]
      self.thread = threading.Thread(target=self.view)  # 创建线程，并指定目标函数
      self.thread.daemon = True  # 设置为守护线程（可选）
      self.thread.start()
      
    def start(self):
      next = partial(self.select_next_role)
      # 初始化游戏脚本
      self.action = GameAction(self.role['name'], self.adb, next)
      # 开始战斗
      self.adb.touch(battle_start)
      
    def select_next_role(self):
      if not self.role['next_role']:
        return
      self.adb.touch(setting, 0.5)
      time.sleep(1)
      # 进入选择角色面板
      self.adb.touch(change_role, 0.5)
      time.sleep(10)
      next_role_name = self.role['next_role']
      self.role = self.roles[next_role_name]
      self.select_role()
      time.sleep(5)
      self.start()
    
    def select_role(self):
      if self.role:
        # 如果角色位置为上排，直接点击选中
        if self.role['position'] == 'up':
            self.adb.touch(self.role['point'])
            logger.info('选中角色 %s', str(self.role['name']))
            time.sleep(1)
        # 如果角色位置为下排，先从角色坐标往上滑动，再点击角色坐标选中
        elif self.role['position'] == 'down':
            self.adb.touch([self.role['point'][0], self.role['point'][1] + 220])
            logger.info('选中角色 %s', str(self.role['name']))
            time.sleep(2)
        # 开始游戏
        self.adb.touch(start_game, 1)
        logger.info('开始游戏')
        time.sleep(20)
        # 自动寻路 TODO 不同角色不同地图
        logger.info('准备移动到布万加')
        move_to_bwj(self.adb)
      
    # 播放游戏画面  
    def view(self):
        while True:
          if self.adb.show_queue.empty():
              time.sleep(0.001)
              continue
          image, result = self.adb.show_queue.get()
          for boxs in result:
              # 把坐标从 float 类型转换为 int 类型
              det_x1, det_y1, det_x2, det_y2, conf, labelIndex = boxs
              # 裁剪目标框对应的图像640*img1/img0
              x1 = int(det_x1 * image.shape[1])
              y1 = int(det_y1 * image.shape[0])
              x2 = int(det_x2 * image.shape[1])
              y2 = int(det_y2 * image.shape[0])
              # 绘制矩形边界框
              cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
              cv.putText(
                  image,
                  "{:.2f}".format(conf),
                  (int(x1), int(y1 - 10)),
                  cv.FONT_HERSHEY_SIMPLEX,
                  0.5,
                  (0, 0, 255),
                  2,
              )
              cv.putText(
                  image,
                  self.adb.yolo.labels[int(labelIndex)],
                  (int(x1), int(y1 - 30)),
                  cv.FONT_HERSHEY_SIMPLEX,
                  0.5,
                  (0, 0, 255),
                  2,
              )
          # image = cv.resize(image, (1168, int(image.shape[0] * 1168 / image.shape[1])))
          image = cv.resize(image, (1168, int(image.shape[0] * 1168 / image.shape[1])))
          cv.imshow("Image", image)
          cv.waitKey(1)

if __name__ == "__main__":
    main = Main('枪炮师')
    main.select_role()
    time.sleep(1)
    main.start()

    # main.select_next_role()
    # 测试代码
    # adb = ScrcpyADB()
    # adb.touch(start_game)
    # move_to_bwj(adb)
    