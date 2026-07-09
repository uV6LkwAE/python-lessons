"""
monster.pyをベースに要件をさらに追加したバージョン
生徒により仕様が異なるため参考程度に
"""

import random

MONSTER_NAMES = ["スライム", "ゾンビ", "ゴースト", "ドラゴン", "デーモン"]
STAT_NAMES = ["HP", "MP", "ATK", "DEF", "SPD", "MAG"]

monsters = {}
monster_max_hp = {}
heal_count = 2
poison_count = 2

selected_monster = ""
selected_monster_max_hp = 0
bet_amount = 0


def choose_attacker_and_defender():
    monster_names = list(monsters.keys())
    attacker = random.choice(monster_names)
    monster_names.remove(attacker)
    defender = random.choice(monster_names)
    return attacker, defender


def apply_defense_debuff_temporarily(defender, show_message=False):
    base_defense = monsters[defender]["DEF"]

    if "debuff" in monsters[defender]:
        for _ in range(monsters[defender]["debuff"]):
            monsters[defender]["DEF"] = int(monsters[defender]["DEF"] * 0.8)

        if show_message:
            print(defender, "の防御力 : ", monsters[defender]["DEF"])

    return base_defense


def calculate_damage(attacker, defender):
    base_defense = apply_defense_debuff_temporarily(defender, show_message=True)
    attack = monsters[attacker]["ATK"]
    defense = monsters[defender]["DEF"]
    damage_base = int((attack - defense / 2) / 2)

    if damage_base < 2:
        damage = random.randint(0, 1)
    elif damage_base < 9:
        damage = random.randint(damage_base - 2, damage_base)
    else:
        damage = (
            damage_base * 7 / 8 + ((damage_base / 4 + 1) * random.randint(0, 255)) / 256
        )

    monsters[defender]["DEF"] = base_defense
    return int(damage)


def calculate_critical_damage(attacker):
    attack = monsters[attacker]["ATK"]
    return int(attack * random.randint(55, 65) / 64)


def is_critical_hit():
    return random.randint(1, 50) == 1


def calculate_magic_damage(attacker, defender):
    base_defense = apply_defense_debuff_temporarily(defender)
    magic = monsters[attacker]["MAG"]
    defense = monsters[defender]["DEF"]
    damage_base = int((magic - defense / 3) / 2)

    if damage_base < 2:
        damage = random.randint(2, 3)
    elif damage_base < 9:
        damage = random.randint(damage_base, damage_base + 2)
    else:
        damage = (
            damage_base * 7 / 8 + ((damage_base / 4 + 1) * random.randint(0, 255)) / 256
        )

    monsters[defender]["DEF"] = base_defense
    return int(damage)


def can_avoid(defender):
    speed = monsters[defender]["SPD"]
    return speed >= 45 and random.randint(1, 3) == 1


def create_monsters():
    for monster_name in MONSTER_NAMES:
        stats = {}

        for stat_name in STAT_NAMES:
            stats[stat_name] = random.randint(10, 50)

        monsters[monster_name] = stats
        monster_max_hp[monster_name] = stats["HP"]


def calculate_levels():
    for monster_name in monsters:
        level = sum(monsters[monster_name].values()) // 10
        monsters[monster_name]["LV"] = level


def assign_odds():
    odds = []

    for monster_name in monsters:
        odds.append((monsters[monster_name]["LV"], monster_name))

    odds.sort(reverse=True)
    odds_rank = 2
    index = 0

    while index < len(odds):
        current_level = odds[index][0]
        same_level_names = []

        next_index = index
        while next_index < len(odds) and odds[next_index][0] == current_level:
            same_level_names.append(odds[next_index][1])
            next_index += 1

        odds_average = odds_rank + (len(same_level_names) - 1) / 2

        if odds_average == int(odds_average):
            odds_average = int(odds_average)

        for monster_name in same_level_names:
            monsters[monster_name]["odds"] = odds_average

        odds_rank += len(same_level_names)
        index = next_index


def initialize_conditions():
    for monster_name in monsters:
        monsters[monster_name]["condition"] = []
        monsters[monster_name]["condition_count"] = {}


def remove_sleep_by_attack(defender):
    if "眠り" in monsters[defender]["condition"]:
        monsters[defender]["condition"].remove("眠り")
        del monsters[defender]["condition_count"]["眠り"]
        print(f"攻撃によって{defender}の目が覚めた")


def remove_debuff(defender):
    if "debuff" in monsters[defender]:
        del monsters[defender]["debuff"]


def normal_attack(attacker, defender, damage, critical_damage):
    if is_critical_hit():
        print(
            defender,
            f"に会心ダメージが{critical_damage}ダメージ入りました",
        )
        monsters[defender]["HP"] -= critical_damage
    else:
        print(defender, f"に{damage}ダメージ入りました")
        monsters[defender]["HP"] -= damage


def special_attack(attacker, defender, avoided, damage, critical_damage):
    if "POWER_UP" in monsters[attacker]:
        damage = int(damage * 1.5)
        critical_damage = int(critical_damage * 1.5)
        monsters[attacker]["POWER_UP"] -= 1

        if monsters[attacker]["POWER_UP"] == 0:
            del monsters[attacker]["POWER_UP"]

    if "眠り" not in monsters[defender]["condition"] and avoided:
        print(defender, "が回避に成功しました")
        return

    if random.randint(1, 2) == 1:
        print(defender, f"に{damage * 2}ダメージ入りました")
        monsters[defender]["HP"] -= damage * 2
        remove_debuff(defender)
        remove_sleep_by_attack(defender)
    else:
        print("攻撃に失敗しました")


def magic_attack(attacker, defender, avoided, magic_damage):
    if monsters[attacker]["MP"] < 10:
        print("マナが足りません")
        print()
        return False

    if "眠り" not in monsters[defender]["condition"] and avoided:
        print(defender, "が回避に成功しました")
        return True

    print(defender, f"に{magic_damage}ダメージ入りました")
    monsters[defender]["HP"] -= magic_damage
    monsters[attacker]["MP"] -= 10
    remove_debuff(defender)
    remove_sleep_by_attack(defender)
    return True


def remove_defeated_monsters():
    defeated = []

    for monster_name in list(monsters.keys()):
        if monsters[monster_name]["HP"] <= 0:
            defeated.append(monster_name)

    for monster_name in defeated:
        del monsters[monster_name]
        print(f"{monster_name} が戦闘不能になりました")

    return len(monsters) == 1


def choose_command(attacker, defender, damage, avoided, critical_damage, magic_damage):
    print("1:通常攻撃")
    print(f"2:HPを10回復(残り{heal_count}回)")
    print("3:必殺技(ダメージが倍になるが1/2の確率で外れる)")
    print("4:魔法の選択")
    print(f"5:毒攻撃(残り{poison_count}回)")

    command = int(input("行動を選択してください:"))

    if command == 1:
        normal_attack(attacker, defender, damage, critical_damage)
    elif command == 2:
        heal(attacker)
    elif command == 3:
        special_attack(attacker, defender, avoided, damage, critical_damage)
    elif command == 4:
        choose_magic(attacker, defender, avoided, magic_damage)
    elif command == 5:
        poison(defender)


def heal(attacker):
    global heal_count

    if heal_count <= 0:
        print("回復はもうありません")
        print()
        return

    recovered = 0
    while recovered < 10:
        if selected_monster_max_hp <= monsters[attacker]["HP"]:
            break

        monsters[attacker]["HP"] += 1
        recovered += 1

    heal_count -= 1
    print(f"{attacker} はHPを10回復した。残り回復回数: {heal_count}")


def poison(defender):
    global poison_count

    if poison_count <= 0:
        print("毒攻撃はもうできません")
        print()
        return

    poison_count -= 1

    if random.random() < 0.7:
        monsters[defender]["condition"].append("毒")
        monsters[defender]["condition_count"]["毒"] = 0
        print("毒状態にしました")
    else:
        print("毒状態にできませんでした")

    print(f"残り回数: {poison_count}")


def sleep(attacker):
    if monsters[attacker]["MP"] < 20:
        print("マナが足りません")
        print()
        return

    monsters[attacker]["MP"] -= 20

    for monster_name in monsters:
        if monster_name == attacker:
            continue

        if random.random() < 0.4:
            if "眠り" not in monsters[monster_name]["condition"]:
                monsters[monster_name]["condition"].append("眠り")

            monsters[monster_name]["condition_count"]["眠り"] = 0
            print(f"{monster_name}が眠り状態になった")


def process_conditions(monster_name):
    if "毒" in monsters[monster_name]["condition"]:
        process_poison(monster_name)

    if "眠り" in monsters[monster_name]["condition"]:
        process_sleep(monster_name)


def process_poison(monster_name):
    monsters[monster_name]["condition_count"]["毒"] += 1
    poison_turns = monsters[monster_name]["condition_count"]["毒"]
    poison_damage = int(monster_max_hp[monster_name] * 0.1)
    monsters[monster_name]["HP"] -= poison_damage
    print(f"{monster_name} は毒のダメージを {poison_damage} 受けた")

    coin = random.random()

    if poison_turns > 5:
        if coin < 0.5:
            cure_poison(monster_name)
    elif coin < poison_turns * 0.1:
        cure_poison(monster_name)


def cure_poison(monster_name):
    print(f"{monster_name} の毒が自然に解除された")
    del monsters[monster_name]["condition_count"]["毒"]
    monsters[monster_name]["condition"].remove("毒")


def process_sleep(monster_name):
    monsters[monster_name]["condition_count"]["眠り"] += 1
    sleep_turns = monsters[monster_name]["condition_count"]["眠り"]
    coin = random.random()

    if sleep_turns > 3:
        if coin < 0.5:
            cure_sleep(monster_name)
    elif coin < (sleep_turns + 2) * 0.1:
        cure_sleep(monster_name)


def cure_sleep(monster_name):
    print(f"{monster_name} の目が覚めた")
    del monsters[monster_name]["condition_count"]["眠り"]
    monsters[monster_name]["condition"].remove("眠り")


def magic_heal(attacker, mp_cost):
    if selected_monster_max_hp < monsters[attacker]["HP"] + mp_cost:
        print("モンスターの最大HPを超えてしまうので実行できません")
        return

    monsters[attacker]["HP"] += mp_cost
    monsters[attacker]["MP"] -= mp_cost


def power_up(attacker):
    if monsters[attacker]["MP"] < 15:
        print("MPが足りません")
        return

    monsters[attacker]["MP"] -= 15
    monsters[attacker]["POWER_UP"] = 2
    print(f"{attacker} の次の2回分の攻撃が1.5倍")


def defense_down(attacker):
    if monsters[attacker]["MP"] < 15:
        print("MPが足りません")
        return

    monsters[attacker]["MP"] -= 15

    for monster_name in monsters:
        if monster_name == attacker:
            continue

        if "debuff" in monsters[monster_name]:
            if monsters[monster_name]["debuff"] < 2:
                monsters[monster_name]["debuff"] += 1
        else:
            monsters[monster_name]["debuff"] = 1

    print("敵にデバフを付与しました（攻撃を受けると解除）")


def choose_magic(attacker, defender, avoided, magic_damage):
    print()
    print("1:魔法攻撃(MPを10消費)")
    print("2:回復魔法(MP1消費につきHP1を回復)")
    print("3:自身が2回攻撃するまで攻撃力1.5倍(MPを15消費)")
    print("4:自分以外のモンスターの防御力ダウン" "(攻撃をくらったら解除)(MPを15消費)")
    print("5:眠り攻撃(MP20消費)")

    choice = int(input("→"))

    if choice == 1:
        magic_attack(attacker, defender, avoided, magic_damage)
    elif choice == 2:
        mp_cost = int(input("消費MPを入力してください"))
        magic_heal(attacker, mp_cost)
    elif choice == 3:
        power_up(attacker)
    elif choice == 4:
        defense_down(attacker)
    elif choice == 5:
        sleep(attacker)


def print_monsters():
    for name, stats in monsters.items():
        print(name, stats)


def print_result():
    winner = list(monsters.keys())[0]
    print(f"{winner} が勝利しました！")

    if winner == selected_monster:
        print("賭けに成功しました！")
        print("賞金 : ", monsters[winner]["odds"] * bet_amount)
    else:
        print("賭けに失敗しました")


def setup_game():
    global selected_monster
    global selected_monster_max_hp
    global bet_amount

    create_monsters()
    calculate_levels()
    assign_odds()
    initialize_conditions()
    print_monsters()

    selected_monster = input("モンスター名を入力してください:")
    bet_amount = int(input("賭ける額を決めてください:"))
    selected_monster_max_hp = monsters[selected_monster]["HP"]
    print()


def play_turn():
    for monster_name in list(monsters.keys()):
        if (
            "毒" in monsters[monster_name]["condition"]
            or "眠り" in monsters[monster_name]["condition"]
        ):
            process_conditions(monster_name)

    if remove_defeated_monsters():
        return True

    print_monsters()

    attacker, defender = choose_attacker_and_defender()
    damage = calculate_damage(attacker, defender)
    critical_damage = calculate_critical_damage(attacker)
    magic_damage = calculate_magic_damage(attacker, defender)
    avoided = can_avoid(defender)

    print("attacker =", attacker, "defender =", defender)

    if attacker == selected_monster:
        choose_command(
            attacker,
            defender,
            damage,
            avoided,
            critical_damage,
            magic_damage,
        )
    else:
        normal_attack(attacker, defender, damage, critical_damage)

    return remove_defeated_monsters()


def main():
    setup_game()

    while True:
        if play_turn():
            print_result()
            break

        input("もう一度プレイ(エンターを押してください)")
        print()


if __name__ == "__main__":
    main()
