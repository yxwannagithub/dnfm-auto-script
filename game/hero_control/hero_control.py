from device_manager.scrcpy_adb import ScrcpyADB
import time


def get_hero_control(name: str, scrcpy_adb: ScrcpyADB):
    """
    获取英雄控制的实例
    :param name:英雄名称
    :param scrcpy_adb:设备链接实例
    :return:
    """
    if name == 'asura':
        from game.hero_control.asura import Asura
        return Asura(scrcpy_adb)
    elif name == 'berserker':
        from game.hero_control.berserker import Berserker
        return Berserker(scrcpy_adb)
    elif name == 'paladin':
        from game.hero_control.paladin import Paladin
        return Paladin(scrcpy_adb)
    elif name == 'ranger':
        from game.hero_control.ranger import Ranger
        return Ranger(scrcpy_adb)
    elif name == 'launcher':
        from game.hero_control.launcher import Launcher
        return Launcher(scrcpy_adb)
    elif name == 'soul_bringer':
        from game.hero_control.soul_bringer import SoulBringer
        return SoulBringer(scrcpy_adb)
    elif name == 'sword_master':
        from game.hero_control.sword_master import SwordMaster
        return SwordMaster(scrcpy_adb)
    elif name == 'vagabond':
        from game.hero_control.vagabond import Vagabond
        return Vagabond(scrcpy_adb)
    elif name == 'demon_slayer':
        from game.hero_control.demon_slayer import DemonSlayer
        return DemonSlayer(scrcpy_adb)
    # elif name == 'axl':
    #   from game.hero_control.asura import AXL
    #   return AXL(scrcpy_adb)
    # elif name == 'jian_zong':
    #   from game.hero_control.jian_zong import JianZong
    #   return JianZong(scrcpy_adb)

    else:
        raise ValueError(f'{name} is not support')


if __name__ == '__main__':
    adb = ScrcpyADB()
    hero = get_hero_control('asura', adb)
    # hero.room_skill_combo.get(6)()
    hero.add_buff()
    # hero.move(30, 1)
    # time.sleep(2)
    # hero.move(60, 1)
    # time.sleep(2)

    # hero.move(400, 1)
    # hero.move(300, 1)
    # adb.touch([1018, 75])
    # adb.display_frames()
    # hero.move(0, 1) 右边
    # hero.move(90, 1) 上
    # hero.move(180, 1) 左
    # hero.move(270, 1) 下
