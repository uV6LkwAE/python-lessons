"""
課題: じゃんけんプログラムをwhileを使って実装する
ここでは関数化は行わない

要件:
- プレイヤーとコンピュータでじゃんけんを行い、先に3回勝った方を最終的な勝者とする。
- どちらかが3勝するまでじゃんけんする。
- あいこの場合は勝敗は決めずに、再度ジャンケンを行う。
- コンピュータの手はランダムで選択する。
"""

import random

hands = ["グー", "チョキ", "パー"]

player_win_count = 0
computer_win_count = 0

# player&computer側の勝利回数がともに3回未満までの間
# orにしてしまうと、どちらか一方がTrueであればTrueになってしまう
# つまり、プレイヤーが3回以上の勝利回数でも実行し続けてしまう
while player_win_count < 3 and computer_win_count < 3:
    player_hand = input("じゃんけんの手を入力してください>>")
    computer_hand = random.choice(hands)
    print(f"コンピューターの手は{computer_hand}です")

    if player_hand == computer_hand:
        print("あいこです")
    elif player_hand == "グー" and computer_hand == "チョキ":
        player_win_count += 1
        print("あなたの勝ちです")
    elif player_hand == "チョキ" and computer_hand == "パー":
        player_win_count += 1
        print("あなたの勝ちです")
    elif player_hand == "パー" and computer_hand == "グー":
        player_win_count += 1
        print("あなたの勝ちです")
    else:
        computer_win_count += 1
        print("あなたの負けです")

if player_win_count == 3:
    print("あなたが3回勝ったので終了します")
elif computer_win_count == 3:
    print("こちらが3回勝ったので終了します")
