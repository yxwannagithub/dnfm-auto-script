from data_const.coordinate import *
from device_manager.scrcpy_adb import ScrcpyADB
from game.hero_control.hero_control_base import HeroControlBase
from utils.logger import logger
import time


class DemonSlayer(HeroControlBase):
    """
    剑宗
    """
    wait = 0.1
    def __init__(self, adb: ScrcpyADB):
        super().__init__(adb)
        self.back_jump = back_jump
        self.skill_wheel = skill_wheel
        self.buff2 = skill_wheel_down  # buff
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
            77: self.skill_combo_77,
        }
        self.skills = { # 全部技能
            "觉醒": skill_top_a,
            "魔鬼": skill_top_b,
            "群魔": skill_top_c,
            "大鞭": skill_top_d,
            "乱舞": skill_middle_a,
            "上抽": skill_middle_b,
            "穿心地刺": skill_middle_c,
            "地抓": skill_middle_d,
            "哈哈哈": skill_bottom_a,
            "小鞭": skill_bottom_b,
            "后跳": back_jump,
        }  
        self.last_angle = 0
        
    def sleep_01(self): 
      time.sleep(0.1)

    # 击杀怪物
    def killMonsters(self, angle, room_index, hero_pos, close_monster):
        self.last_angle = angle
        print(self.useSkills, 'useSkills')
        if self.useSkills.get(room_index, False):
            is_close_monster = self.move_to_monster(angle, hero_pos, close_monster)
            # 普通攻击
            if is_close_monster:
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
        self.adb.swipe(self.skill_wheel, self.buff2)
        time.sleep(0.5)
        logger.info("加 buff")
        pass

    def skill_combo_1(self):
        """
        技能连招1
        :return:
        """
        self.reset()
        self.moveV2(295)
        time.sleep(0.3)
        self.moveV2(0)
        self.add_buff()
        self.adb.touch(self.skills['魔鬼'], 0.6)
        self.adb.touch(self.skills['穿心地刺'], 0.1)
        time.sleep(0.4)
        self.adb.touch(self.skills['穿心地刺'], 0.1)
        logger.info("技能连招1")
        pass

    def skill_combo_2(self):
        """
        技能连招2
        :return:
        """
        self.sleep_01()
        self.moveV2(275)
        time.sleep(0.5)
        self.moveV2(1,0.1)
        self.adb.touch(self.skills['大鞭'],0.1)
        time.sleep(0.3)
        logger.info("技能连招2")
        pass

    def skill_combo_3(self):
        """
        技能连招3
        :return:
        """
        self.sleep_01()
        self.moveV2(340)
        time.sleep(0.3)
        self.moveV2(0)
        time.sleep(0.3)
        self.adb.touch(self.skills['上抽'],0.1)
        time.sleep(0.1)
        logger.info("技能连招3")
        pass
    
    def skill_combo_4(self):
        """
        技能连招4
        :return:
        """
        self.sleep_01()
        self.moveV2(340)
        time.sleep(0.3)
        self.adb.touch(self.skills['哈哈哈'], 1.5)
        self.moveV2(0)
        time.sleep(2)
        logger.info("技能连招4")
        pass
    
    def skill_combo_5(self):
        """
        技能连招5
        :return:
        """
        self.sleep_01()
        self.moveV2(90, 0.7)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['乱舞'], 1.5)
        self.sleep_01()
        self.moveV2(180, 1)
        self.moveV2(90, 0.3)
        self.moveV2(180, 2)
        logger.info("技能连招5")
        pass
    
    def skill_combo_6(self):
        """
        技能连招6
        :return:
        """
        self.sleep_01()
        self.moveV2(245, 0.4)
        self.adb.touch(self.awaken_skill)
        logger.info("技能连招6")
        pass
    
    def skill_combo_8(self):
        """
        技能连招8
        :return:
        """
        self.sleep_01()
        self.moveV2(335)
        time.sleep(0.4)
        self.moveV2(1)
        time.sleep(0.1)
        self.moveV2(0)
        self.adb.touch(self.skills['哈哈哈'], 1.5)
        time.sleep(0.1)
        pass
    
    def skill_combo_9(self):
        """
        技能连招9
        :return:
        """
        self.sleep_01()
        self.moveV2(350)
        time.sleep(0.2)
        self.moveV2(0)
        self.adb.touch(self.skills['大鞭'])
        pass
    
    def skill_combo_10(self):
        """
        技能连招10
        :return:
        """
        self.sleep_01()
        self.moveV2(335)
        time.sleep(0.3)
        self.moveV2(1)
        self.adb.touch(self.skills['群魔'], 0.1)
        time.sleep(0.1)
        self.adb.touch(self.skills['穿心地刺'], 0.1)
        time.sleep(0.1)
        self.adb.touch(self.skills['穿心地刺'], 0.1)
        time.sleep(0.4)
        self.adb.touch(self.skills['穿心地刺'], 0.1)
        time.sleep(0.2)
        self.adb.touch(self.skills['上抽'], 0.1)
        time.sleep(0.2)
        self.adb.touch(self.skills['乱舞'], 1.5)
        time.sleep(0.1)
        pass
      
    def skill_combo_77(self):
        """
        小技能连招
        :return:
        """
        logger.info("小技能连招")
        pass
