import os
from pprint import pprint
from random import choice
from datetime import datetime
from art import logo

#Rules:
# The deck is unlimited in size.
# There are no jokers.
# The Jack/Queen/King all count as 10.
# The Ace can count as 11 or 1.
# Use the following list as the deck of cards:
# cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def deal_card() -> int:
    """Generate and return a random card for each player."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    card = choice(cards)
    return card


def count_scores(cards: list) -> int:
    """Count and return the sum of cards as the total score."""
    #return 0 if hit a blackjack
    if sum(cards) == 21 and len(cards) == 2:
        return 0

    #count 11 as 1 if sum is > 21
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)

    return sum(cards)


def compare_score(p_score: int, c_score: int) -> tuple:
    """Compare the score of player and computer and returns a tuple."""
    if p_score == 0:
        return True, "Congrats! You hit the blackjack."
    elif c_score == 0:
        return False, "You lose. Computer got the blackjack."
    elif p_score == c_score:
        return None, "Draw."
    elif p_score > 21:
        return False, "Your score is over 21. You lose."
    elif c_score > 21:
        return True, "Computer score is over 21. You win."
    elif p_score > c_score:
        return True, "You won!"
    else:
        return False, "You lose."


def clrscr():
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def gen_game_report(game_data: list, result: tuple, n: int) -> dict:
    """Generate and return game report as a dictionary."""
    user, computer = game_data #unpacking the list
    game_date = datetime.today()
    game_report = {
        f"Blackjack Game {n}": {
            "timestamp": game_date.strftime("%m-%d-%y - %H:%M:%S"),
            "player_card": user[0],
            "player_score": user[1],
            "opponent's_card": computer[0],
            "opponent's_score": computer[1],
            "blackjack": True if user[1] == 0 or computer[1] == 0 else False,
            "winner": "Player" if result is True else "Computer" if result is False else "Draw"
        }
    }
    return  game_report


report = {}
game_count = 0
def play_blackjack():
    p_cards = []
    c_cards = []
    #starting score for player and computer. As 0 would be considered as a blackjack.
    p_score = -1
    c_score = -1
    game_over = False

    print(logo)

    # deal 2 cards for each player
    for _ in range(2):
        p_cards.append(deal_card())
        c_cards.append(deal_card())

    while not game_over:
        p_score = count_scores(p_cards)
        c_score = count_scores(c_cards)

        print(f"You cards: {p_cards}, current_score: {p_score}")
        print(f"Computer first card: {c_cards[0]}")

        if p_score == 0 or c_score == 0 or p_score > 21:
            game_over = True
        else:
            deal_again = input("Do you want to deal another cards? Type 'y'. Otherwise, type 'n': ").lower()
            if deal_again == "y":
                p_cards.append(deal_card())
                clrscr()
            else:
                game_over = True

    while c_score != 0  and c_score < 17: #continue dealing cards if not blackjack or score < 17
        c_cards.append(deal_card())
        c_score = count_scores(c_cards)

    clrscr()
    print(f"Your cards: {p_cards}. Final score: {p_score}")
    print(f"Computer's cards: {c_cards}. Final score: {c_score}")
    result = compare_score(p_score, c_score)
    print(result[1])

    #merge player and computer data into a list
    game_data = [[[p_cards], p_score], [[c_cards], c_score]]
    #passing result[0] -> bool, passing it as the argument for result params
    report.update(gen_game_report(game_data, result[0], game_count))


#recursion
while input("Play blackjack? Type 'y' or 'no': ").lower() == 'y':
    clrscr()
    game_count += 1
    play_blackjack()

pprint(report, sort_dicts=False)

