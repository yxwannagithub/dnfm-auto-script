from data_const.coordinate import *
from device_manager.scrcpy_adb import ScrcpyADB
from game.hero_control.hero_control_base import HeroControlBase
from utils.logger import logger
import time


class Berserker(HeroControlBase):
    """
    红眼
    """
    wait = 0.1
    def __init__(self, adb: ScrcpyADB):
        super().__init__(adb)
        self.back_jump = back_jump  # 后跳
        self.skill_wheel = skill_wheel
        self.buff1 = skill_wheel_down  # 暴走
        self.buff2 = skill_wheel_right  # 血气唤醒
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
            "乱斩": skill_bottom_a,
            "怒气": skill_bottom_b,
            "大崩": skill_middle_a,
            "大吸": skill_middle_b,
            "小崩combo": skill_middle_c,
            "抓头combo": skill_middle_d,
            "觉醒": skill_top_a,
            "三段斩": skill_top_b,
            "裂波": skill_top_c,
            "血剑": skill_top_d,
            "鬼斩": skill_corner,
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
                self.normal_attack(1)
                time.sleep(0.3)
        elif self.useSkills.get(room_index, False) and room_index == 5:
            is_close_monster = self.move_to_monster(angle, hero_pos, close_monster)
            # 普通攻击
            if is_close_monster:
                self.adb.touch(back_jump)
                self.normal_attack(1.5)
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
        logger.info("暴走")
        time.sleep(0.3)
        self.adb.swipe(self.skill_wheel, self.buff2, 0.3)
        logger.info("血气")
        pass

    def skill_combo_1(self):
        """
        技能连招1
        :return:
        """
        self.reset()
        self.moveV2(295, 0.2)
        self.add_buff()
        time.sleep(0.2)
        self.moveV2(340, 0.1)
        self.adb.touch(self.skills['小崩combo'])
        self.adb.touch(self.attack,2)
        logger.info("小崩combo")
        pass

    def skill_combo_2(self):
        """
        技能连招2
        :return:
        """
        self.sleep_01()
        self.moveV2(295, 0.4)
        self.adb.touch(self.skills['血剑'])
        logger.info("血剑")
        pass

    def skill_combo_3(self):
        """
        技能连招3
        :return:
        """
        self.sleep_01()
        self.moveV2(340, 0.8)
        time.sleep(0.4)
        self.adb.touch(self.skills['怒气'])
        logger.info("怒气")
        pass
    
    def skill_combo_4(self):
        """
        技能连招4
        :return:
        """
        self.sleep_01()
        self.moveV2(340, 0.3)
        self.adb.touch(self.skills['乱斩'])
        logger.info("乱斩")
        time.sleep(2)
        pass
    
    def skill_combo_5(self):
        """
        技能连招5
        :return:
        """
        self.moveV2(140, 0.8)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['大吸'],2)
        time.sleep(0.2)
        logger.info("大吸")
        self.moveV2(90, 0.1)
        self.moveV2(180, 1.5)
        pass
    
    def skill_combo_6(self):
        """
        技能连招6
        :return:
        """
        self.sleep_01()
        self.moveV2(265, 0.4)
        self.adb.touch(self.skills['大崩'])
        self.moveV2(340, 0.3)
        time.sleep(1)
        logger.info("大崩")
        pass
    
    def skill_combo_8(self):
        """
        技能连招8
        :return:
        """
        self.sleep_01()
        self.moveV2(335, 0.6)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['乱斩'])
        pass
    
    def skill_combo_9(self):
        """
        技能连招9
        :return:
        """
        self.sleep_01()
        self.moveV2(340, 0.4)
        self.adb.touch(self.skills['大吸'],2)
        pass
    
    def skill_combo_10(self):
        """
        技能连招10
        :return:
        """
        self.sleep_01()
        self.moveV2(330, 0.3)
        self.moveV2(1, 0.1)
        self.adb.touch(self.skills['小崩combo'])
        self.sleep_01()
        self.adb.touch(self.skills['血剑'])
        pass
    
    def skill_combo_11(self):
        """
        技能连招11
        :return:
        """
        logger.info("技能连招11 开始")
        self.adb.touch(self.skills['大吸'])
        time.sleep(3)
        logger.info("技能连招11 结束")
        pass
      
    def skill_combo_77(self):
        """
        小技能连招
        :return:
        """
        self.adb.touch(self.skills['怒气'])
        time.sleep(0.3)
        self.adb.touch(self.skills['抓头combo'])
        logger.info("小技能连招")
        pass
