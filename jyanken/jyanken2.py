'''
じゃんけんプログラムの別解
生徒のコードを修正
'''

import random

hands = ["グー", "チョキ", "パー"]

player_win_count = 0
computer_win_count = 0

while player_win_count < 3 and computer_win_count < 3:
    result = 0
    player_hand = input("じゃんけんの手を入力してください")

    # 両者があいこの限り続ける
    while result == 0:
        if player_hand == "グー":
            player_hand_index = 0

        if player_hand == "チョキ":
            player_hand_index = 1

        if player_hand == "パー":
            player_hand_index = 2

        computer_hand_index = random.randint(0, 2)
        computer_hand = hands[computer_hand_index]

        print(computer_hand)

        # 手の番号の差を3で割った余りで、あいこ・勝ち・負けを判定する
        result = (computer_hand_index - player_hand_index + 3) % 3
        if result == 0:
            player_hand = input("あいこです、次の手を入力してください")

        elif result == 1:
            print("あなたの勝ちです")
            player_win_count += 1

        elif result == 2:
            print("あなたの負けです")
            computer_win_count += 1

if player_win_count == 3:
    print("あなたが3回勝ったので終了します")

elif computer_win_count == 3:
    print("こちらが3回勝ったので終了します")


