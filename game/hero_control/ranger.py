from data_const.coordinate import *
from device_manager.scrcpy_adb import ScrcpyADB
from game.hero_control.hero_control_base import HeroControlBase
from utils.logger import logger
import time

class Ranger(HeroControlBase):
    """
    漫游枪手
    """
    wait = 0.1
    def __init__(self, adb: ScrcpyADB):
        super().__init__(adb)
        self.back_jump = back_jump  # 后跳
        self.skill_wheel = skill_wheel
        self.buff1 = skill_wheel_right  # 死亡左轮
        self.buff2 = skill_wheel_down  # 银弹
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
            "横扫": skill_bottom_a,
            "强踢combo": skill_bottom_b,
            "BBQ": skill_middle_a,
            "乱射": skill_middle_b,
            "回头一击combo": skill_middle_c,
            "回旋踢combo": skill_middle_d,
            "疯狂屠戮": skill_top_a,
            "双鹰回旋": skill_top_b,
            "多重爆头": skill_top_c,
            "移动射击": skill_top_d,
            "踏射": skill_corner,
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
            # self.room_skill_combo.get(77)()
            is_close_monster = self.move_to_monster(angle, hero_pos, close_monster)
            # 普通攻击
            if is_close_monster:
                self.adb.touch(self.back_jump)
                self.normal_attack(1)
                time.sleep(0.3)
        else:
            self.room_skill_combo.get((room_index + 1), self.skill_combo_77)()
            self.useSkills[room_index] = True

    def add_buff(self):
        """
        添加buff
        :return:
        """
        self.adb.swipe(self.skill_wheel, self.buff1, 0.3)
        logger.info("死亡左轮")
        self.adb.swipe(self.skill_wheel, self.buff2, 0.3)
        logger.info("银弹")
        pass

    def skill_combo_1(self):
        """
        技能连招1
        :return:
        """
        self.reset()
        self.moveV2(285, 0.25)
        self.moveV2(180, 0.1)
        self.add_buff()
        time.sleep(0.2)
        self.adb.touch(self.skills['回头一击combo'])
        logger.info("回头一击")
        pass

    def skill_combo_2(self):
        """
        技能连招2
        :return:
        """
        self.sleep_01()
        self.moveV2(270, 0.3)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['回头一击combo'])
        logger.info("爆头一击")
        pass

    def skill_combo_3(self):
        """
        技能连招3
        :return:
        """
        self.sleep_01()
        self.moveV2(315, 0.4)
        time.sleep(0.5)
        self.adb.touch(self.skills['横扫'])
        logger.info("横扫")
        pass
    
    def skill_combo_4(self):
        """
        技能连招4
        :return:
        """
        self.moveV2(275, 0.2)
        self.sleep_01()
        self.adb.touch(self.skills['强踢combo'], 0.3)
        self.adb.touch(self.skills['强踢combo'], 0.3)
        self.adb.touch(self.skills['强踢combo'], 0.3)
        self.adb.touch(self.skills['强踢combo'], 0.3)
        logger.info("强踢combo")
        time.sleep(1)
        pass
    
    def skill_combo_5(self):
        """
        技能连招5
        :return:
        """
        time.sleep(0.5)
        self.moveV2(90, 0.5)
        self.moveV2(180, 0.8)
        self.adb.touch(self.skills['回头一击combo'], 0.3)
        logger.info("回头一击")
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
        self.moveV2(260, 0.5)
        self.adb.touch(self.skills['多重爆头'])
        time.sleep(1)
        self.adb.touch(self.skills['双鹰回旋'], 0.1)
        self.adb.touch(self.attack, 3)
        time.sleep(1)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        time.sleep(0.1)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        time.sleep(0.1)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        time.sleep(2)
        self.adb.touch(self.skills['乱射'], 2)
        self.moveV2(340, 0.3)
        time.sleep(1)
        logger.info("技能连招6")
        pass
    
    def skill_combo_8(self):
        """
        技能连招8
        :return:
        """
        self.sleep_01()
        self.moveV2(315, 0.3)
        self.moveV2(180, 0.1)
        self.adb.touch(self.skills['回头一击combo'])
        pass
    
    def skill_combo_9(self):
        """
        技能连招9
        :return:
        """
        self.sleep_01()
        self.moveV2(340, 0.2)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        pass
    
    def skill_combo_10(self):
        """
        技能连招10
        :return:
        """
        self.sleep_01()
        self.moveV2(330, 0.3)
        self.moveV2(180, 0.1)
        self.adb.touch(self.skills['回头一击combo'], 0.1)
        self.adb.touch(self.skills['回头一击combo'], 0.1)
        self.adb.touch(self.skills['强踢combo'], 0.1)
        self.adb.touch(self.skills['强踢combo'], 0.1)
        self.adb.touch(self.skills['强踢combo'], 0.1)
        self.adb.touch(self.skills['强踢combo'], 0.1)
        self.moveV2(1, 0.2)
        self.sleep_01()
        self.adb.touch(self.skills['乱射'], 2)
        pass
    
    def skill_combo_11(self):
        """
        技能连招11
        :return:
        """
        logger.info("技能连招11 开始")
        self.adb.touch(self.skills['乱射'])
        time.sleep(3)
        logger.info("技能连招11 结束")
        pass
      
    def skill_combo_77(self):
        """
        小技能连招
        :return:
        """
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        time.sleep(0.1)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        time.sleep(0.1)
        self.adb.touch(self.skills['回旋踢combo'], 0.1)
        time.sleep(1)
        self.adb.touch(self.skills['乱射'], 2)
        logger.info("小技能连招")
        pass
