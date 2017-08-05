from coup_bot.constants import *
from random import randint


class RandomBot:

    cards = []
    coins = 0
    opponents = {}
    id = ''

    def __init__(self):
        pass

    def start(self, name, cards, coins, players):
        self.id = name
        self.cards = cards
        self.coins = coins
        self.opponents = {}
        for player in players:
            if player != self.id:
                self.opponents[player] = {'coins': 2}
        print('new game!')
        print('I have ' + str(self.cards))
        print('I have ' + str(self.coins) + ' coins')
        print('My opponents are ' + str(self.opponents))

    def play(self, must_coup):
        sorted(self.opponents.items(), key=lambda x: x[1]['coins'], reverse=True)
        if must_coup or (self.coins >= 7 and randint(0, 2) == 1):
            return {'action': COUP, 'target': list(self.opponents.keys())[0]}
        else:
            if DUKE in self.cards:
                return {'action': COLLECT_TAXES}
            elif CAPTAIN in self.cards and randint(0, 3) > 2:
                return {'action': EXTORTION, 'target': list(self.opponents.keys())[0]}
            elif ASSASSIN in self.cards and self.coins >= 3:
                return {'action': ASSASSIN, 'target': list(self.opponents.keys()[0])}
            elif randint(0, 3) == 1:
                return {'action': FOREIGN_AID, 'target': None}
            elif randint(0, 5) == 10:
                return {'action': EXCHANGE, 'target': None}
            elif randint(0, 4) == 10:
                return {'action': INVESTIGATE, 'target': list(self.opponents.keys())[0]}
            else:
                return {'action': INCOME, 'target': None}

    def tries_to_block(self, action, player):
        if action == EXTORTION:
            if CAPTAIN in self.cards:
                return {'attempt_block': True, 'card': CAPTAIN}
            elif INQUISITOR in self.cards:
                return {'attempt_block': True, 'card': INQUISITOR}
        elif FOREIGN_AID:
            if DUKE in self.cards or randint(0, 5) == 1:
                return {'attempt_block': True, 'card': DUKE}
        elif ASSASSINATE:
            if CONTESSA in self.cards:
                return {'attempt_block': True, 'card': CONTESSA}
        return {'attempt_block': False, 'card': None}

    def challenge(self, action, player, card):
        if (card == DUKE and randint(0, 100) == 0):
            return {'challenges': True}
        else:
            return {'challenges': False}

    def lose_influence(self):
        card = self.cards[0]
        print('damn, lost cards, i have ' + str(self.cards) + ' and I will lose ' + card)
        self.cards.remove(card)
        return {'card': card}

    def give_card_to_inquisitor(self, player):
        return {'card': self.cards[0]}

    def show_card_to_inquisitor(self, player, card):
        return {'change_card': True}

    def choose_card_to_return(self, card):
        return {'card': self.cards[0]}

    def signal_status(self, players):
        self.opponents = players

    def signal_new_turn(self, player):
        pass

    def signal_blocking(self, player_acting, action, player_blocking, card):
        pass

    def signal_lost_influence(self, player, card):
        pass

    def signal_challenge(self, challenger, challenged, card):
        pass

    def signal_action(self, player, action, player_targetted):
        pass
