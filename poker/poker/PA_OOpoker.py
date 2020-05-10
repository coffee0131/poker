
# coding: utf-8

# # PA. Poker Hands in OOP
# 
# A deck of cards is 52 cards, divided into four suits, each containing 13 ranks. Each card is uniquely idedifieable by auit and rank.
# - Suits: spades, clubs, hearts, and diamonds  
# - Ranks: Ace, 2, ..., 10, Jack, Queen, King

# Shuffle the deck. Pick a card from the top of the deck and print the name of card. Repeat 5 times.

# ## Abstract `Card` class
# Q. Write a `Card` class. Class instances are created by passing `rank + suit` string, for instance:
# ```Python
# >>> card = Card('TD')
# >>> print(card)
# TD
# >>> card
# TD
# ```
# 한 장의 카드가 갖는 값(integer)은 카드 게임 종류에 따라 다르다. 보통 rank 종류에 따라 값이 결정된다. 예를 들어 King은 poker game에서는 13이지만, blackjack game에서는 10 또는 0으로 사용될 수 있다.
# value method를 implement하기 전에는 두 장의 card를 비교할 수 없다. 그러나, subclass에서 이 method만 implement한다면 비교가 가능하게 된다. 상속받을 class를 위해 정의하는 class를 'abstract class'라 한다. 
# 

# In[8]:


# Constants
suits = 'CDHS'
ranks = '23456789TJQKA'

from abc import ABCMeta, abstractmethod

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()


# ## Poker Card class
# 단, Poker game에서 두 카드를 비교할 때 suit과 무관하게 rank로만 결정한다. 오름차 순서로 나열하면 다음과 같다. 
# 
#     '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
# 
# Q. `Card` class를 상속받아 Poker game용 `PKCard` class를 정의하라. 
# >Hint: 위 순서대로 정수를 return하는 value() method를 implementation해야 한다.

# In[14]:


class PKCard(Card):
    """Card for Poker game
    """
    pass


if __name__ == '__main__':
    c1 = PKCard('QC')
    c2 = PKCard('9D')
    c3 = PKCard('9C')
    print(f'{c1} {c2} {c3}')

    # comparison
    print(c1 > c2 == c3)

    # sorting
    cards = [c1, c2, c3, PKCard('AS'), PKCard('2D')]
    sorted_cards = sorted(cards)
    print(sorted_cards)
    cards.sort()
    print(cards)


# ## Deck class
# Q. 다음 methods를 갖는 `Deck` class를 작성하라.
# 
# Methods:
# - `__init__(self, cls)`: `cls`는 card class name
# - shuffle
# - pop
# - `__str__`
# - `__len__(self)` to enable `len` builtin function
# - `__getitem__(self, index)` to enable indexing and slicing as well as iteration

# In[31]:


import random
class Deck:
    def __init__(self, cls):
        """Create a deck of 'cls' card class
        """
        pass

if __name__ == '__main__':
    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()
    c = deck[0]
    print('A deck of', c.__class__.__name__)
    print(deck)
    # testing __getitem__ method
    print(deck[-5:])

    while len(deck) >= 10:
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)


# 위의 예에서 my_hand와 your_hand는 단순히 rank value가 가장 큰 것이 이긴다는 'high card' 족보만으로 따졌을 때이다. Poker의 패는 [List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)에서 보듯이 다양한 족보가 있다.
# 
# ## Poker Hands
# 지난 Programming Assignement를 object-oriented로 설계 구현해 보자.
# 
# [List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)의 Hand rank category 표에 열거된 패의 rank 0..9 을 역순으로 9..0의 integer로 나열하면 hand ranking의 높고 낮음을 알수 있다. 이 수를 혼동하지 않도록 이라 하자.
# 
# Straight, flush, straight flush와 같이 rank가 다른 5장으로 패가 이뤄지는 경우, 
# hand ranking이 같으면
# 1. 5장끼리 rank value를 비교해서 판단해야 한다. 즉, reverse(decreading) order로 sorting하여 rank value를 비교하면 된다.
# 
# Hand ranking이 같다면, 예를 들어 둘 다 two pair로 동률 이루고 있다면
# 1. 높은 수 one pair의 rank value를 비교하고
# 2. 같으면, 낮은 one pair의 rank value를 비교하고
# 3. 같으면, 나머지 1장 끼리 value를 비교해서 승부를 가른다. 
# 
# 따라서, 패가 이뤄지는지 찾는 method들은 (hand_ranking, five_cards) tuple로 return한다면
# tuple 비교하는 Python rule에 따라 행하면 충분하게 된다.
# 이때, 이어지는 five_cards는 rank가 높은 순서로 sorting하거나, rank가 같은 것이 있다면(find_a_kind의 경우)
# tie-breaking이 먼저 일어날 카드들을 앞으로 배치해야 list간 비교로 간편히 비교 가능히다. (four cards, tripple cards, high pair)
# 
# Q. *PA. Find poker hands* 문제에서 function으로 구현한 것들을 OOP로 rewriting하라.
# 
# 중요: hand ranking 찾기, hand ranking이 같을 때 tie-break이 제대로 적용되는지를 검증하기 위한
# 가능한 모든 test case를 20개 이상을 작성함으로써, unit test가 *거의* 모든 경우를 포함하고 있음을
# 보여야 한다.

# In[ ]:


class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = sorted(cards, reverse=True)
    ...
    
if __name__ == '__main__':
    import sys
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    # your test cases here
    pass

