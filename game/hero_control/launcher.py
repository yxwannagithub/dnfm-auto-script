from data_const.coordinate import *
from device_manager.scrcpy_adb import ScrcpyADB
from game.hero_control.hero_control_base import HeroControlBase
from utils.logger import logger
import time

class Launcher(HeroControlBase):
    """
    大枪
    """
    wait = 0.1
    def __init__(self, adb: ScrcpyADB):
        super().__init__(adb)
        self.back_jump = back_jump  # 后跳
        self.skill_wheel = skill_wheel
        self.buff1 = skill_wheel_right  # 潜能爆发
        self.buff2 = skill_wheel_down  # 火力全开
        self.awaken_skill = skill_top_a  # 觉醒
        self.attack = attack  # 普通攻击
        self.useSkills = {}  # 存放已经释放技能的房间下标
        self.room_skill_combo = {
            1: self.skill_combo_1,
            2: self.skill_combo_2,
            3: self.skill_combo_3,
            4: self.skill_combo_4,
            5: self.skill_combo_5,
            6: self.skill_combo_6,
            8: self.skill_combo_8,
            9: self.skill_combo_9,
            10: self.skill_combo_10,
            11: self.skill_combo_11,
            77: self.skill_combo_77,
        }
        self.skills = { # 全部技能
            "坦克炮": skill_bottom_a,
            "加农炮": skill_bottom_b,
            "碉堡轰炸": skill_middle_a,
            "细火": skill_middle_b,
            "激光": skill_middle_c,
            "榴弹": skill_middle_d,
            "卫星射线": skill_top_a,
            "压缩炮": skill_top_b,
            "刺弹": skill_top_c,
            "量子爆弹": skill_top_d,
            "滑铲": skill_corner,
        }  
        self.last_angle = 0
        
    def sleep_01(self): 
      time.sleep(0.1)

    # 击杀怪物
    def killMonsters(self, angle, room_index, hero_pos, close_monster):
        self.last_angle = angle
        print(self.useSkills, 'useSkills')
        if self.useSkills.get(room_index, False) and room_index != 5:
            is_close_monster = self.move_to_monster(angle, hero_pos, close_monster)
            # 普通攻击
            if is_close_monster:
              self.adb.touch(self.back_jump)
              self.normal_attack(1)
              time.sleep(0.3)
        elif self.useSkills.get(room_index, False) and room_index == 5:
            is_close_monster = self.move_to_monster(angle, hero_pos, close_monster)
            self.room_skill_combo.get(77)()
            # 普通攻击
            if is_close_monster:
                self.adb.touch(self.back_jump)
                self.normal_attack(1)
                time.sleep(2)
        else:
            self.room_skill_combo.get((room_index + 1), self.skill_combo_77)()
            self.useSkills[room_index] = True

    def add_buff(self):
        """
        添加buff
        :return:
        """
        self.adb.swipe(self.skill_wheel, self.buff1, 0.3)
        logger.info("潜能爆发")
        time.sleep(0.1)
        self.adb.swipe(self.skill_wheel, self.buff2, 0.3)
        logger.info("火力全开")
        pass

    def skill_combo_1(self):
        """
        技能连招1
        :return:
        """
        self.reset()
        self.moveV2(285, 0.25)
        self.moveV2(1, 0.1)
        self.add_buff()
        time.sleep(0.2)
        self.adb.touch(self.skills['榴弹'])
        logger.info("榴弹")
        pass

    def skill_combo_2(self):
        """
        技能连招2
        :return:
        """
        self.sleep_01()
        self.moveV2(245, 0.3)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['激光'])
        logger.info("激光")
        pass

    def skill_combo_3(self):
        """
        技能连招3
        :return:
        """
        self.sleep_01()
        self.moveV2(315, 0.2)
        self.adb.touch(self.skills['加农炮'])
        logger.info("加农炮")
        pass
    
    def skill_combo_4(self):
        """
        技能连招4
        :return:
        """
        self.moveV2(275, 0.2)
        self.sleep_01()
        self.adb.touch(self.skills['刺弹'], 0.6)
        logger.info("刺弹")
        time.sleep(1)
        pass
    
    def skill_combo_5(self):
        """
        技能连招5
        :return:
        """
        self.moveV2(90, 0.5)
        self.moveV2(180, 1.3)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['激光'])
        logger.info("激光")
        self.moveV2(90, 0.25)
        self.moveV2(180, 0.6)
        pass
    
    def skill_combo_6(self):
        """
        技能连招6
        :return:
        """
        ## todo 优化调试
        self.sleep_01()
        self.moveV2(260, 0.3)
        self.adb.touch(self.skills['压缩炮'],1)
        self.sleep_01()
        self.adb.touch(self.skills['坦克炮'])
        self.sleep_01()
        self.adb.touch(self.skills['加农炮'])
        self.sleep_01()
        self.adb.touch(self.skills['榴弹'])
        self.moveV2(340, 0.3)
        time.sleep(1)
        logger.info("压缩炮！榴弹！")
        pass
    
    def skill_combo_8(self):
        """
        技能连招8
        :return:
        """
        self.sleep_01()
        self.moveV2(280, 0.3)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['细火'], 2)
        pass
    
    def skill_combo_9(self):
        """
        技能连招9
        :return:
        """
        self.sleep_01()
        self.moveV2(340, 0.2)
        self.adb.touch(self.skills['刺弹'], 0.4)
        pass
    
    def skill_combo_10(self):
        """
        技能连招10
        :return:
        """
        self.sleep_01()
        self.moveV2(330, 0.3)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['碉堡轰炸'])
        self.sleep_01()
        pass
    
    def skill_combo_11(self):
        """
        技能连招11
        :return:
        """
        logger.info("技能连招11 开始")
        self.adb.touch(self.skills['量子爆弹'])
        time.sleep(3)
        logger.info("技能连招11 结束")
        pass
      
    def skill_combo_77(self):
        """
        小技能连招
        :return:
        """
        self.adb.touch(self.skills['量子爆弹'], 0.5)
        self.adb.touch(back_jump)
        self.adb.touch(attack, 1)
        time.sleep(0.2)
        logger.info("小技能连招")
        pass
