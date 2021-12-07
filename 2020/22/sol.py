import numpy as np
import sys

realprint = print
def print(*args, **kwargs):
    pass

hands = [[int(card) for card in hand.split('\n')[1:]]
                             for hand in sys.stdin.read().strip().split('\n\n')]

def hash_hands(hands):
    return ','.join(map(str, hands[0] + [-1] + hands[1]))

glob_game_num = 0
def play_game(hands):
    global glob_game_num
    glob_game_num += 1
    game_num = glob_game_num
    print(f'=== Game {game_num} ===\n')
    used_hands = set()
    round_num = 0
    game_winner = 0
    while True:
        round_num += 1
        # traditional winning
        if not hands[0]:
            game_winner = 1
            break
        if not hands[1]:
            break

        # p1 wins if it's a repeat sitch
        hashed = hash_hands(hands)
        if hashed in used_hands:
            break
        used_hands.add(hashed)

        # otherwise start play
        print(f'-- Round {round_num} (Game {game_num}) --')
        print(f"Player 1's deck: {', '.join(map(str, hands[0]))}")
        print(f"Player 2's deck: {', '.join(map(str, hands[1]))}")
        p0 = hands[0].pop(0)
        p1 = hands[1].pop(0)
        print(f'Plauer 1 plays: {p0}')
        print(f'Plauer 2 plays: {p1}')
        to_add = [p0, p1]
        # and determine who wins round
        winner = 0
        if (len(hands[0]) >= p0
            and len(hands[1]) >= p1):
            new_hands = [hands[0][:p0],
                         hands[1][:p1]]
            print('Playing a sub-game to determine the winner...\n')
            winner = play_game(new_hands)
            print('...anyway, back to game {game_num}.')
        else:
            winner = 0 if p0 > p1 else 1
        print(f'Player {winner + 1} wins round {round_num} of game {game_num}!\n')
        
        # then give the winner the cards
        if winner == 0:
            hands[0] += to_add
        else:
            hands[1] += to_add[::-1]
    print('The winner of game {game_num} is player {game_winner + 1}!')
    return game_winner
                
winner = play_game(hands)
print('== Post-game results ==')
print(f"Player 1's deck: {', '.join(map(str, hands[0]))}")
print(f"Player 2's deck: {', '.join(map(str, hands[1]))}")

def score(hand):
    mul = len(hand)
    res = 0
    for card in hand:
        res += card * mul
        mul -= 1
    return res

realprint(score(hands[winner]))

"""part 1
while all(hands):
    p1 = hands[0].popleft()
    p2 = hands[1].popleft()

    if p1 > p2:
        hands[0].append(p1)
        hands[0].append(p2)
    else:
        hands[1].append(p2)
        hands[1].append(p1)

print(max(map(score, hands)))
"""
