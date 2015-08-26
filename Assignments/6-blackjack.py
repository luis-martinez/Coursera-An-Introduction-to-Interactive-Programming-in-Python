# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user38_q71QDkUsJj5qAm7.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)

    def draw_back(self, canvas, pos):
        # only apply to first card in dealer hand when in_play = True
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        print_out = ""
        for card in self.cards:
            print_out += str(card) + " "

        return "Hand contains " + print_out

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        hand_value = 0
        no_A = True

        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                no_A = False

        if no_A:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value

    def draw(self, canvas, pos):
        card_pos = [0, 0]
        SPACE_BETWEEN_CARDS = 10

        for card_index in range(0, min(len(self.cards), 5)):
            card_pos[0] = pos[0] + card_index * (CARD_SIZE[0] + SPACE_BETWEEN_CARDS)
            card_pos[1] = pos[1]
            self.cards[card_index].draw(canvas, card_pos)

    def draw_first_back(self, canvas, pos):
        card_pos = [0, 0]
        SPACE_BETWEEN_CARDS = 10

        for card_index in range(0, min(len(self.cards), 5)):
            card_pos[0] = pos[0] + card_index * (CARD_SIZE[0] + SPACE_BETWEEN_CARDS)
            card_pos[1] = pos[1]
            if card_index == 0:
                self.cards[card_index].draw_back(canvas, card_pos)
            else:
                self.cards[card_index].draw(canvas, card_pos)


# define deck class
class Deck:
    def __init__(self):
        global SUITS, RANKS

        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                new_card = Card(suit, rank)
                self.cards.append(new_card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        s = "Deck contains "
        for card in self.cards:
            s += str(card) + " "

        return s


# define event handlers for buttons
def deal():
    global outcome, in_play, score

    if in_play:
        outcome = "Dealer wins!"
        print outcome
        score -= 1
    else:
        outcome = ""

    global new_deck
    new_deck = Deck()

    new_deck.shuffle()
    global player_hand
    player_hand = Hand()
    global dealer_hand
    dealer_hand = Hand()
    player_hand.add_card(new_deck.deal_card())
    player_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())

    print "Player " + str(player_hand)
    print "Player value: " + str(player_hand.get_value())
    print "Dealer " + str(dealer_hand)
    print "Dealer value: " + str(dealer_hand.get_value())

    in_play = True


def hit():
    global new_deck, in_play, score, outcome

    if not in_play:
        return

    if player_hand.get_value() <= 21:
        player_hand.add_card(new_deck.deal_card())
        print "Player " + str(player_hand)
        print "Player value: " + str(player_hand.get_value())

    if player_hand.get_value() > 21:
        print "Player value: " + str(player_hand.get_value())
        in_play = False
        outcome = "Player have busted. Dealer wins!"
        print outcome
        score -= 1


def stand():
    global new_deck, score, in_play, outcome

    if not in_play:
        return

    while dealer_hand.get_value() <= 17:
        dealer_hand.add_card(new_deck.deal_card())
        print "Dealer " + str(dealer_hand)
        print "Dealer value: " + str(dealer_hand.get_value())

    if dealer_hand.get_value() > 21:
        print "Dealer value: " + str(dealer_hand.get_value())
        in_play = False
        outcome = "Dealer have busted. Player wins!"
        print outcome
        score += 1
    else:
        print "Player value: " + str(player_hand.get_value())
        print "Dealer value: " + str(dealer_hand.get_value())
        if dealer_hand.get_value() >= player_hand.get_value():
            # dealer wins
            in_play = False
            outcome = "Dealer wins!"
            print outcome
            score -= 1
        else:
            in_play = False
            outcome = "Player wins!"
            print outcome
            score += 1


# draw handler
def draw(canvas):
    global player_hand, dealer_hand, in_play, score, outcome

    DEALER_HAND_POS = (60, 200)
    PLAYER_HAND_POS = (60, 390)

    TITLE_POS = (80, 100)
    DEALER_TITLE_POS = (60, 180)
    PLAYER_TITLE_POS = (60, 370)
    PLAYER_MSG_POS = (200, 370)
    SCORE_POS = (400, 100)
    OUTCOME_POS = (200, 180)

    canvas.draw_text('Blackjack', TITLE_POS, 48, 'Black')
    canvas.draw_text('Dealer', DEALER_TITLE_POS, 24, 'Black')
    canvas.draw_text('Player', PLAYER_TITLE_POS, 24, 'Black')
    canvas.draw_text('Score: ' + str(score), SCORE_POS, 24, 'Black')

    player_hand.draw(canvas, PLAYER_HAND_POS)

    if in_play:
        canvas.draw_text('Hit or Stand?', PLAYER_MSG_POS, 24, 'Black')
        dealer_hand.draw_first_back(canvas, DEALER_HAND_POS)
    else:
        canvas.draw_text('New deal?', PLAYER_MSG_POS, 24, 'Black')
        dealer_hand.draw(canvas, DEALER_HAND_POS)

    canvas.draw_text(outcome, OUTCOME_POS, 24, 'Black')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
