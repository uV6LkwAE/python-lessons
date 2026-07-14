"""
課題: バトルロワイヤルを関数ベースで実装する
クラスは用いず、関数で実装することを身につける

注意: 現段階では実際にレベルが引かれておらず、最後の一体になるまでモンスターを倒せない
まずはここまで実装している

要件:
- 任意のモンスターを用意し、それぞれHPなどの属性を持つ
- バトルロワイヤル = 最後の一体になるまで戦い続ける
- 1回の攻撃では、攻撃する側 attacker と
  攻撃を受ける側 defender を1体ずつ選ぶ
- attacker と defender は毎回ランダムに選び直す
- attacker を選んだ後、そのモンスターを候補から外して
  defender を選ぶ
- これにより、同じモンスターが攻撃側と防御側を
  同時に担当しないようにする

攻撃仕様:
- 通常攻撃の基準ダメージは、攻撃側の ATK と
  防御側の DEF から計算する
- 基準ダメージが小さい場合は、0から1のランダムダメージにする
- 基準ダメージが中程度の場合は、基準値付近でランダムにする
- 基準ダメージが大きい場合は、計算式にランダム要素を加える
- 会心ダメージとは、まれに発生する強い攻撃のダメージを表す
  このプログラムでは、防御側の DEF を使わず、
  攻撃側の ATK をもとに計算する
- 防御側の SPD が45以上なら、回避可能なモンスターとして扱う

オッズ仕様:
- オッズは、勝ったときにどれくらいの倍率になるかを表す
- 考え方は競馬のオッズと同じ
- 強い馬は勝つ可能性が高いため、当たっても倍率は低くなる
- 弱い馬は勝つ可能性が低いため、当たったときの倍率は高くなる
- このプログラムでは、馬の代わりにモンスターへオッズを付ける
- 各モンスターの強さは、ステータス合計を10で割った lv で判断する
- lv が高いモンスターほど勝ちやすいとみなし、低いオッズを付ける
- lv が低いモンスターほど勝ちにくいとみなし、高いオッズを付ける
- 最も強いグループのオッズは2から始める
- 同じ lv のモンスターが複数いる場合は、同じオッズを付ける
- 同じ lv のグループには、その順位範囲の平均値をオッズとして使う
"""

import random

MONSTER_NAMES = ["スライム", "ゾンビ", "ゴースト", "ドラゴン", "デーモン"]
STAT_NAMES = ["HP", "MP", "ATK", "DEF", "SPD", "MAG"]


def choose_attacker_and_defender(monsters):
    monster_names = list(monsters.keys())
    attacker = random.choice(monster_names)
    # 攻撃側と防御側が同じにならないようにする
    monster_names.remove(attacker)

    defender = random.choice(monster_names)
    return attacker, defender


# 通常ダメージ計算
def calculate_damage(monsters, attacker, defender):
    attack = monsters[attacker]["ATK"]
    defense = monsters[defender]["DEF"]
    # ATKからDEFの半分を引き、さらに半分にする
    # DEFが高いほど下がり、ATKが高いほど上がる基準値になる
    damage_base = int((attack - defense / 2) / 2)

    if damage_base < 2:
        # 基準値が小さい場合も、最低限のランダム性を持たせる
        damage = random.randint(0, 1)
    elif damage_base < 9:
        # 中程度のダメージは、基準値付近で少しだけブレさせる
        damage = random.randint(damage_base - 2, damage_base)
    else:
        # 大きいダメージは、乱数を混ぜて単調さを避ける
        damage = (
            damage_base * 7 / 8 + ((damage_base / 4 + 1) * random.randint(0, 255)) / 256
        )

    return int(damage)


# 会心ダメージ（強めの攻撃）計算
# 相手のDEFに関係なく、攻撃側のATKからダメージを計算する
def calculate_critical_damage(monsters, attacker):
    attack = monsters[attacker]["ATK"]
    # 会心ダメージはDEFを使わず、ATKに近い値を少しブレさせる
    return int(attack * random.randint(55, 65) / 64)


# 防御側のモンスターが回避できるかを判定する
def can_avoid(monsters, defender):
    speed = monsters[defender]["SPD"]
    return speed >= 45


def create_monsters():
    monsters = {}

    for monster_name in MONSTER_NAMES:
        stats = {}

        for stat_name in STAT_NAMES:
            stats[stat_name] = random.randint(10, 50)

        # 各statのkey: valueの格納が終わったら、lvを計算する
        stats["lv"] = sum(stats.values()) // 10
        # モンスターの名前をキー、statsをvalueにして登録する
        monsters[monster_name] = stats

    return monsters


def build_odds(monsters):
    # レベルとモンスター名をタプルにして追加する（下処理用）
    odds = []

    for monster_name, stats in monsters.items():
        # リストの中にタプルで追加
        odds.append((stats["lv"], monster_name))

    # レベルの降順に並び替える
    odds.sort(reverse=True)
    print(odds)
    return odds


def assign_odds(monsters, odds):
    # 一番強いモンスターのオッズは2
    # レベルが低くなるほど、オッズが高くなる
    odds_rank = 2
    index = 0

    # 全てのodds分、ループで回す
    while index < len(odds):
        # タプルのレベルだけ取り出す
        current_level = odds[index][0]
        same_level_names = []

        next_index = index
        # 最初は同じモンスターのレベルを比較している
        # next_indexがoddsの範囲内で、
        # 次のレベルが今見ているレベルと同じか確認する
        # 両方満たしていればTrue
        # 前半はnext_indexがoddsの範囲を超えないようにするため必要

        # 今見ているレベルと同じレベルが続いている間、同じグループとして集める
        while next_index < len(odds) and odds[next_index][0] == current_level:
            same_level_names.append(odds[next_index][1])
            next_index += 1

        # レベルが変わったらwhileを抜ける
        # 集めたグループに対して平均を計算する
        # same_level_namesが1体だけでも、同じ式で計算する

        """
        len(same_level_names) - 1 で、
        同じレベルのグループの中で何個進んだかを出す。
        [2, 3, 4]のように3体いる場合、
        開始地点から最後までは2個進むため、1を引く。
        次に/2するのはリストの平均地点つまり、3を出すため
        さらに今の順位を基準にするため、odds_rankを足す
        """
        odds_average = odds_rank + (len(same_level_names) - 1) / 2

        # 整数にしても値が変わらないなら、整数として保存する
        # 2.5のような場合はFalseになるためそのままになる
        if odds_average == int(odds_average):
            odds_average = int(odds_average)

        # oddsをmonstersに追加
        for monster_name in same_level_names:
            monsters[monster_name]["odds"] = odds_average

        # 次のランクに更新
        odds_rank += len(same_level_names)
        # 次のインデックスをindexとして再代入しているだけ
        index = next_index


def main():
    # 関数内部からモンスター生成関数を呼び出しても良い
    monsters = create_monsters()
    odds = build_odds(monsters)
    assign_odds(monsters, odds)

    for name, stats in monsters.items():
        print(name, stats)

    attacker, defender = choose_attacker_and_defender(monsters)

    print("attacker =", attacker, "defender =", defender)
    print("damage =", calculate_damage(monsters, attacker, defender))
    print("critical_dmg =", calculate_critical_damage(monsters, attacker))

    defender_speed = monsters[defender]["SPD"]
    can_defender_avoid = can_avoid(monsters, defender)
    print(defender, "SPD = ", defender_speed)
    print("can_avoid =", can_defender_avoid)


if __name__ == "__main__":
    main()
