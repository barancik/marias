'''
Created on Feb 22, 2015

@author: Radoslav Klic
'''
import random
import deck
from deck import Deck
from gameType import StdGameType

ROLE_LEADER = "Leader"
ROLE_COOP1 = "Cooperator 1"
ROLE_COOP2 = "Cooperator 2"

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = Deck([])
        self.role = None

    def __str__(self, rules = None):
        if not rules:
            sortKey = deck.germanDefaultSortingKey
        else:
            sortKey = rules.cardSortingKey
        return "name: {name}, hand: {hand}".format(name=self.name, hand=sorted(self.hand, key=sortKey))
    
    def pickTrumpCard(self):
        return self.hand[0]
    
    def selectGameType(self):
        trumpCard = self.pickTrumpCard()
        self.selectedGameType = StdGameType(trumpCard, False, False)
        return self.selectedGameType

    def specifyStdGame(self):
        return self.selectedGameType
    
    def selectTalon(self, rules):
        print("I have: ", rules.sortedCards(self.hand))
        allowedCards = rules.allowedTalonCards(self.hand)
        if isinstance(rules.gameType, StdGameType):
            allowedCards = list(filter(lambda c: c.suit != rules.gameType.trump, allowedCards))
        
        nonMarriageAllowedCards = [c for c in allowedCards if not rules.isMarriage(c, self)]
        if len(nonMarriageAllowedCards) >= 2:
            allowedCards = nonMarriageAllowedCards
            
        print("Talon candidates: ", rules.sortedCards(allowedCards))
        talon = allowedCards[:2]

        return talon
    
    def play(self, table, rules):
        allowedTurns = rules.allowedTurns(self.hand, table)
        print(self.__str__(rules))
        print("Allowed turns", rules.sortedCards(allowedTurns))
        selCardList = random.sample(allowedTurns, 1)
        self.hand.removeCards(selCardList)
        
        return selCardList[0]
    