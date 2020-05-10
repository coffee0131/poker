import pytest
import random
from poker import suits, ranks, Card,PKCard,Deck,Hands


def test_Card_init():
    card = PKCard('AC')
    assert card.rank == 'A' and card.suit == 'C'
    assert card.card == 'AC'

def test_PKCard_repr():
    assert repr(PKCard('AC')) == 'AC'

@pytest.fixture
def all_faces():
    return [r+s for r in ranks for s in suits]

def test_PKCard_values(all_faces):
    for face in all_faces:
        card, expected = PKCard(face), PKCard.VALUES[face[0]]
        assert card.value() == expected

@pytest.fixture
def c9C():
    return PKCard("9C")

@pytest.fixture
def c9H():
    return PKCard("9H")

@pytest.fixture
def cTH():
    return PKCard("TH")

def test_PKCard_values(c9C, c9H, cTH):
    assert c9C == c9C and c9C == c9H
    assert c9H < cTH and c9C < cTH
    assert c9C <= c9H <= cTH
    assert cTH > c9H and cTH > c9C
    assert cTH >= c9H >= c9C
    assert c9C != cTH and c9H != cTH


@pytest.fixture
def deck():
    return Deck(PKCard)

def test_Deck_init(deck):
    assert len(deck) == 52

def test_Deck_str():
    assert str(PKCard('AC')) == 'AC'
    

@pytest.fixture

def test_Hands_tell_hand_ranking():
    #Test Straight Flush
    card = ['5C','6C', '7C', '8C', '9C']
    assert (Hands(card).tell_hand_ranking() == 'straight flush')
    #Test Straight
    card = ['5C', '6H', '7C', '8C', '9S']
    assert (Hands(card).tell_hand_ranking() == 'straight')
    #Test flush
    card = ['5C', 'AC', 'QC', 'AC', 'TC']
    assert (Hands(card).tell_hand_ranking() == 'flush')
    #Test Four card
    card = ['AC', 'AH', 'AS', 'AD', '9S']
    assert (Hands(card).tell_hand_ranking() == 'four of a kind')
    #Test Full House
    card = ['2C', '2H', '2S', 'KH', 'KS']
    assert (Hands(card).tell_hand_ranking() == 'full house')
    #Test Triple
    card = ['3C', '3H', '3D', 'QH', 'JD']
    assert (Hands(card).tell_hand_ranking() == 'triple')
    #Test Two Pair
    card = ['3C', '3H', 'QD', 'QH', 'JD']
    assert (Hands(card).tell_hand_ranking() == 'two pair')
    #Test One Pair
    card = ['AC', '7H', '3D', 'JH', 'JD']
    assert (Hands(card).tell_hand_ranking() == 'one pair')
    #Test One Pair
    card = ['8C', '9H', 'AD', 'TH', 'KD']
    assert (Hands(card).tell_hand_ranking() == 'high')

def test_Hands_tell_winner():
    #Test same rank but value is different in Straight flush
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7H', '8H', '9H'])
    assert (my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in flush
    my_hand = Hands(['5C','6C', '7C', '8C', 'TC'])
    your_hand = Hands(['TH','AH', '7H', '8H', '9H'])
    assert (my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in Straight
    my_hand = Hands(['5C','6H', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7D', '8H', '9H'])
    assert (my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in Four card
    my_hand = Hands(['5C','5S', '5D', '5H', '9C'])
    your_hand = Hands(['2C','2S', '2D', '2H', '9H'])
    assert (my_hand.tell_winner(your_hand) == True)
    #Test same rank but value is different in Full House
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7H', '8H', '9H'])
    assert (my_hand.tell_winner(your_hand) == False)
    #Test same rank but value is different in Triple
    my_hand = Hands(['5C','5H', '5D', '8C', '9C'])
    your_hand = Hands(['TH','TS', 'TD', '8H', '9H'])
    assert (my_hand.tell_winner(your_hand) == False)
    #Test same rank first value but second value is different in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '2H', '2D', '9H'])
    assert (my_hand.tell_winner(your_hand) == True)
    #Test same rank, first value and second value but last value is different in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '7D', 'TH'])
    assert (my_hand.tell_winner(your_hand) == False)
    #Test same rank, all value in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '7D', '9H'])
    assert (my_hand.tell_winner(your_hand) == None)
    #Test same rank, value is Difference in One Pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '6D', '9H'])
    assert (my_hand.tell_winner(your_hand) == True)
    #Test same rank, value is Difference in One Pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', 'QH', '6D', '9H'])
    assert (my_hand.tell_winner(your_hand) == True)
    #Test same rank in One pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', 'QH', '7D', '9H'])
    assert (my_hand.tell_winner(your_hand) == None)
    #Straight Flush vs High Card
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['8C', '9H', 'AD', 'TH', 'KD'])
    assert (my_hand.tell_winner(your_hand) == True)
    #if same rank and value, winner is None
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['5H','6H', '7H', '8H', '9H'])
    assert (my_hand.tell_winner(your_hand) == None)
