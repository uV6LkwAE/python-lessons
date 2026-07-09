"""
課題: じゃんけんプログラムのコードを関数化する

プレイヤーとコンピュータでじゃんけんを行い、先に3回勝った方を最終的な勝者とする。

関数ごとの責務:

play_janken()
- じゃんけん1回分の処理を担当する。
- プレイヤーの手を入力で受け取る。
- コンピュータの手をランダムに決めて表示する。
- あいこの場合は勝敗を決めず、もう一度じゃんけんを行う。
- 勝敗が決まったら、プレイヤーが勝った場合は True、
  コンピュータが勝った場合は False を返す。
- 勝利数の管理や、ゲーム終了の判定は行わない。

play_game()
- ゲーム全体の進行を担当する。
- プレイヤーとコンピュータの勝利数を管理する。
- play_janken() の戻り値を使って、どちらの勝利数を増やすか判断する。
- どちらかが3勝するまで、じゃんけんを繰り返す。
- 3勝した側に応じて、最終結果のメッセージを表示する。
"""

import random

hands = ["グー", "チョキ", "パー"]


def play_janken():
    while True:
        player_hand = input("じゃんけんの手を入力してください")
        print(f"あなたは{player_hand}を選びました")
        computer_hand = random.choice(hands)

        print(f"コンピューターの手は{computer_hand}です")

        # あいこの場合は何もreturnしないので、whileループを継続
        if player_hand == computer_hand:
            print("あいこです")
        elif player_hand == "グー" and computer_hand == "チョキ":
            return True
        elif player_hand == "チョキ" and computer_hand == "パー":
            return True
        elif player_hand == "パー" and computer_hand == "グー":
            return True
        else:
            return False


def play_game():
    player_win_count = 0
    computer_win_count = 0

    # player&computer側の勝利回数がともに3回未満までの間
    # orにしてしまうと、どちらか一方がTrueであればTrueになってしまう
    # つまり、プレイヤーが3回以上の勝利回数でも実行し続けてしまう
    while player_win_count < 3 and computer_win_count < 3:
        player_win = play_janken()

        if player_win:
            print("あなたの勝ちです")
            player_win_count += 1
        else:
            print("あなたの負けです")
            computer_win_count += 1

    # whileの条件式がFalseになったら実行される
    if player_win_count == 3:
        print("あなたが3回勝ったので終了します")
    elif computer_win_count == 3:
        print("こちらが3回勝ったので終了します")


play_game()
