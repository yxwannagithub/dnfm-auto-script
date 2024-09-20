from data_const.coordinate import *
from device_manager.scrcpy_adb import ScrcpyADB
from game.hero_control.hero_control_base import HeroControlBase
from utils.logger import logger
import time


class Asura(HeroControlBase):
    """
    阿修罗
    """
    wait = 0.1

    def __init__(self, adb: ScrcpyADB):
        super().__init__(adb)
        self.back_jump = back_jump
        self.skill_wheel = skill_wheel
        self.buff1 = skill_wheel_right
        self.buff2 = skill_wheel_down  # 杀意波动
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
        self.skills = {  # 全部技能
            "无双波": skill_bottom_a,
            "圆波": skill_bottom_b,
            "扎热": skill_middle_a,
            "火波": skill_middle_b,
            "邪光": skill_middle_c,
            "冰波combo": skill_middle_d,
            "觉醒": skill_top_a,
            "三段斩": skill_top_b,
            "裂波": skill_top_c,
            "怒气": skill_top_d,
            "不动冥王": skill_corner,
        }
        self.last_angle = 0

    def sleep_01(self):
        time.sleep(0.1)

    # 击杀怪物
    def killMonsters(self, angle, room_index, hero_pos, close_monster):
        self.last_angle = angle
        if self.useSkills.get(room_index, False) and room_index != 5:
            is_close_monster = self.move_to_monster(angle, hero_pos, close_monster)
            # 普通攻击
            if is_close_monster:
                self.normal_attack(1.5)
                time.sleep(0.3)
        elif self.useSkills.get(room_index, False) and room_index == 5:

            is_close_monster = self.move_to_monster(angle, hero_pos, close_monster)
            self.room_skill_combo.get(77)()
            # 普通攻击
            if is_close_monster:
                self.normal_attack(1.5)
        else:
            self.room_skill_combo.get((room_index + 1), self.skill_combo_77)()
            self.useSkills[room_index] = True

    def add_buff(self):
        """
        添加buff
        :return:
        """
        self.moveV2(270, 0.3)
        self.adb.swipe(self.skill_wheel, self.buff2)
        logger.info("杀意")
        time.sleep(1)
        pass

    def skill_combo_1(self):
        """
        技能连招1
        :return:
        """
        self.reset()
        logger.info("移动到0方向")
        self.moveV2(295)
        logger.info("移动到295方向")
        self.moveV2(0)
        self.add_buff()
        self.moveV2(340)
        logger.info("移动到340方向")
        self.adb.touch(self.skills['冰波combo'], 0.1)
        logger.info("冰波！")
        time.sleep(0.1)
        self.adb.touch(self.skills['冰波combo'], 0.1)
        logger.info("斜光！")
        time.sleep(0.2)
        logger.info("技能连招1")
        pass

    def skill_combo_2(self):
        """
        技能连招2
        :return:
        """
        self.sleep_01()
        self.moveV2(270)
        time.sleep(0.35)
        self.moveV2(1, 0.1)
        time.sleep(0.3)
        self.adb.touch(self.skills['圆波'], 0.1)
        time.sleep(0.3)
        self.adb.touch(self.skills['圆波'], 0.1)
        time.sleep(0.2)
        logger.info("技能连招2")
        pass

    def skill_combo_3(self):
        """
        技能连招3
        :return:
        """
        self.sleep_01()
        self.moveV2(340, 0.2)
        self.moveV2(1, 0.1)
        time.sleep(0.3)
        self.adb.touch(self.skills['火波'], 0.1)
        time.sleep(0.2)
        self.adb.touch(self.skills['怒气'], 0.1)
        time.sleep(0.2)
        logger.info("技能连招3")
        pass

    def skill_combo_4(self):
        """
        技能连招4
        :return:
        """
        self.moveV2(270)
        time.sleep(0.2)
        self.moveV2(1)
        time.sleep(0.3)
        self.adb.touch(self.skills['扎热'])
        time.sleep(0.2)
        self.adb.touch(self.skills['冰波combo'])
        time.sleep(0.1)
        self.adb.touch(self.skills['冰波combo'])
        time.sleep(0.1)
        logger.info("技能连招4")
        time.sleep(2)
        pass

    def skill_combo_5(self):
        """
        技能连招5
        :return:
        """
        time.sleep(1)
        self.moveV2(90)
        time.sleep(0.2)
        self.moveV2(0)
        self.adb.touch(self.skills['无双波'])
        time.sleep(0.4)
        self.adb.touch(self.skills['无双波'])
        self.adb.touch(self.skills['无双波'])
        time.sleep(0.2)
        self.moveV2(90)
        time.sleep(0.7)
        self.moveV2(0)
        self.adb.touch(self.awaken_skill)
        time.sleep(0.5)
        self.adb.touch(self.awaken_skill)
        time.sleep(1)
        self.moveV2(180)
        time.sleep(2)
        self.moveV2(90)
        time.sleep(0.2)
        logger.info("技能连招5")
        pass

    def skill_combo_6(self):
        """
        技能连招6
        :return:
        """
        self.sleep_01()
        self.moveV2(200)
        time.sleep(0.35)
        self.sleep_01()
        self.adb.touch(self.skills['冰波combo'], 0.1)
        self.adb.touch(self.skills['冰波combo'], 0.1)
        logger.info("技能连招6")
        pass

    def skill_combo_8(self):
        """
        技能连招8
        :return:
        """
        self.sleep_01()
        self.moveV2(335)
        time.sleep(0.3)
        self.sleep_01()
        self.adb.touch(self.skills['火波'])
        self.sleep_01()
        self.adb.touch(self.skills['圆波'])
        time.sleep(0.1)
        pass

    def skill_combo_9(self):
        """
        技能连招9
        :return:
        """
        self.sleep_01()
        self.moveV2(340)
        time.sleep(0.2)
        self.moveV2(0)
        time.sleep(0.5)
        self.adb.touch(self.skills['冰波combo'])
        time.sleep(0.1)
        self.adb.touch(self.skills['邪光'])
        time.sleep(0.1)
        pass

    def skill_combo_10(self):
        """
        技能连招10
        :return:
        """
        self.sleep_01()
        self.moveV2(360)
        time.sleep(0.4)
        self.adb.touch(self.skills['圆波'])
        self.adb.touch(self.skills['无双波'])
        time.sleep(0.1)
        self.adb.touch(self.skills['无双波'])
        time.sleep(0.2)
        self.adb.touch(self.skills['扎热'])
        time.sleep(0.2)
        self.adb.touch(self.skills['冰波combo'])
        time.sleep(0.1)
        self.adb.touch(self.skills['邪光'])
        pass

    def skill_combo_77(self):
        """
        小技能连招
        :return:
        """
        self.adb.touch(self.skills['圆波'])
        time.sleep(0.3)
        self.adb.touch(self.skills['怒气'])
        logger.info("小技能连招")
        pass
