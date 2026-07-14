"""
課題: バトルロワイヤルを関数ベースで実装する
クラスは用いず、関数で実装することを身につける

注意: まずは基本実装のため、クリティカルダメージは戦闘に組み込んでいない

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
- ダメージが決まったら、防御側のHPからダメージ分を引く
- 攻撃者、防御者、ダメージ、残りHPを
  戦闘メッセージとして表示する

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

実装順と関数仕様:
1. モンスター生成: create_monsters()
   - 渡すもの: なし
   - 返すもの: monsters 辞書
   - 処理内容: 各モンスターに HP, MP, ATK, DEF, SPD, MAG を設定する

2. レベル設定: create_monsters() 内の lv 計算
   - 渡すもの: 各モンスターのステータス
   - 返すもの: なし
   - 処理内容: ステータス合計を10で割り、lv として保存する

3. オッズ用リスト作成: build_odds(monsters)
   - 渡すもの: monsters 辞書
   - 返すもの: odds リスト
   - 処理内容: (lv, モンスター名) のタプルを作り、lv の降順に並べる

4. オッズ設定: assign_odds(monsters, odds)
   - 渡すもの: monsters 辞書, odds リスト
   - 返すもの: なし
   - 処理内容: lv が高いほど低いオッズを付ける

5. 攻防判定: choose_attacker_and_defender(monsters)
   - 渡すもの: monsters 辞書
   - 返すもの: attacker, defender
   - 処理内容: 攻撃側と防御側をランダムに1体ずつ選ぶ

6. 回避判定: can_avoid(monsters, defender)
   - 渡すもの: monsters 辞書, defender
   - 返すもの: True または False
   - 処理内容: defender の SPD が45以上なら回避できると判定する

7. ダメージ計算: calculate_damage(monsters, attacker, defender)
   - 渡すもの: monsters 辞書, attacker, defender
   - 返すもの: damage
   - 処理内容: attacker の ATK と defender の DEF から通常ダメージを計算する

8. HP減算: apply_damage(monsters, defender, damage)
   - 渡すもの: monsters 辞書, defender, damage
   - 返すもの: remaining_hp
   - 処理内容: defender の HP から damage を引く

9. 戦闘メッセージ出力:
   print_battle_message(attacker, defender, damage, remaining_hp)
   - 渡すもの: attacker, defender, damage, remaining_hp
   - 返すもの: なし
   - 処理内容: 攻撃者、防御者、ダメージ、残りHPを表示する

10. バトルロワイヤル: battle_royale(monsters)
   - 渡すもの: monsters 辞書
   - 返すもの: なし
   - 処理内容: 最後の一体になるまで攻撃処理を繰り返し、勝者を表示する

11. メイン処理: main()
   - 渡すもの: なし
   - 返すもの: なし
   - 処理内容: モンスター生成、オッズ設定、初期状態表示、
     バトルロワイヤル開始までを順番に実行する
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


# 防御側のHPからダメージを引く
def apply_damage(monsters, defender, damage):
    # ダメージを引いた後、マイナスにならないようにする
    monsters[defender]["HP"] = max(0, monsters[defender]["HP"] - damage)
    return monsters[defender]["HP"]


# 1回分の戦闘結果を表示する
def print_battle_message(attacker, defender, damage, remaining_hp):
    print(f"{attacker} の攻撃")
    print(f"{defender} に {damage} ダメージ")
    print(f"{defender} の残りHP: {remaining_hp}")


# HPが0以下になったモンスターを戦闘不能として取り除く
def remove_defeated_monsters(monsters):
    defeated_monsters = []

    for monster_name in list(monsters.keys()):
        if monsters[monster_name]["HP"] <= 0:
            defeated_monsters.append(monster_name)

    for monster_name in defeated_monsters:
        del monsters[monster_name]
        print(f"{monster_name} はHPが0になり、戦闘不能になりました")


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


# 最後の一体になるまで、1回分の攻撃処理を繰り返す
def battle_royale(monsters):
    while len(monsters) > 1:
        attacker, defender = choose_attacker_and_defender(monsters)

        if can_avoid(monsters, defender):
            print(f"{attacker} の攻撃")
            print(f"{defender} は攻撃を回避しました")
        else:
            damage = calculate_damage(monsters, attacker, defender)
            remaining_hp = apply_damage(monsters, defender, damage)
            print_battle_message(attacker, defender, damage, remaining_hp)

        remove_defeated_monsters(monsters)
        print()

    winner = list(monsters.keys())[0]
    print(f"{winner} の勝利です")


def main():
    monsters = create_monsters()
    odds = build_odds(monsters)
    assign_odds(monsters, odds)

    print("参加モンスター")
    for monster_name, stats in monsters.items():
        print(
            f"{monster_name}: "
            f"HP={stats['HP']} "
            f"ATK={stats['ATK']} "
            f"DEF={stats['DEF']} "
            f"SPD={stats['SPD']} "
            f"lv={stats['lv']} "
            f"odds={stats['odds']}"
        )
    print()

    battle_royale(monsters)


if __name__ == "__main__":
    main()
