import os

import pytest

if os.path.exists('solution.py'):
    from solution import Card, InvalidCardError
else:
    from main import Card, InvalidCardError  # type:ignore


class Suit:
    CLUBS = '♣'
    DIAMONDS = '◆'
    HEARTS = '❤'
    SPADES = '♠'


@pytest.fixture
def card1():
    return Card(1, Suit.HEARTS)


@pytest.fixture
def card2():
    return Card(7, Suit.SPADES)


@pytest.fixture
def card3():
    return Card(11, Suit.DIAMONDS)


@pytest.fixture
def card4():
    return Card(13, Suit.CLUBS)


@pytest.fixture
def card5():
    return Card(2, Suit.DIAMONDS)


@pytest.fixture
def card6():
    return Card(2, Suit.HEARTS)


def test_build_card(card1: Card):
    assert isinstance(card1, Card)
    assert card1.suit == Suit.HEARTS


@pytest.mark.parametrize('value', (0, 15))
def test_build_card_fails_when_not_supported_value_is_given(value: int):
    with pytest.raises(InvalidCardError) as err:
        Card(value, Suit.SPADES)
    assert str(err.value) == f'Invalid card: {repr(value)} is not a supported value'


@pytest.mark.parametrize('value', ('Z', 'F'))
def test_build_card_fails_when_not_supported_symbol_is_given(value: str):
    with pytest.raises(InvalidCardError) as err:
        Card(value, Suit.SPADES)
    assert str(err.value) == f'Invalid card: {repr(value)} is not a supported symbol'


@pytest.mark.parametrize('suit', ('✨', 'Z'))
def test_build_card_fails_when_not_supported_suit_is_given(suit: str):
    with pytest.raises(InvalidCardError) as err:
        Card(1, suit)
    assert str(err.value) == f'Invalid card: {repr(suit)} is not a supported suit'


def test_available_suits():
    assert Card.get_available_suits() == '♣◆❤♠'


# https://engineeringfordatascience.com/posts/pytest_fixtures_with_parameterize/
@pytest.mark.parametrize(
    'card_fixture,expected_repr',
    (('card1', '🂱'), ('card2', '🂧'), ('card3', '🃋'), ('card4', '🃞')),
)
def test_card_representation(card_fixture: str, expected_repr: str, request: pytest.FixtureRequest):
    card = request.getfixturevalue(card_fixture)
    assert repr(card) == expected_repr


def test_card_equality_with_same_values_and_suits(card1: Card):
    card2 = Card(card1.value, card1.suit)
    assert card1 == card2


def test_card_equality_with_same_values_and_different_suits(card1: Card, card4: Card):
    card = Card(card1.value, card4.suit)
    assert card1 != card


def test_card_equality_with_different_values_and_same_suits(card1: Card, card5: Card):
    card = Card(card5.value, card1.suit)
    assert card1 != card


def test_card_equality_with_different_values_and_different_suits(
    card1: Card, card5: Card, card4: Card
):
    card = Card(card5.value, card4.suit)
    assert card1 != card


def test_card_equality_with_different_type(card1: Card):
    assert card1 != 'not a card'


def test_card_is_less_than_other_card(card1: Card, card2: Card):
    assert card2 < card1


def test_card_is_greater_than_other_card(card1: Card, card2: Card):
    assert card1 > card2


def test_add_cards(card1: Card, card2: Card, card3: Card, card5: Card, card6: Card):
    card = card1 + card2
    assert card.value == 8
    assert card.suit == Suit.HEARTS

    card = card2 + card3
    assert card.value == 1
    assert card.suit == Suit.DIAMONDS

    card = card2 + card5
    assert card.value == 9
    assert card.suit == Suit.SPADES

    card = card5 + card6
    assert card.value == 4
    assert card.suit == Suit.DIAMONDS


def test_default_message_for_invalid_card_error():
    err = InvalidCardError()
    assert str(err) == 'Invalid card'


def test_cards_by_suit():
    assert ''.join(Card.get_cards_by_suit(Suit.CLUBS)) == '🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞'
    assert ''.join(Card.get_cards_by_suit(Suit.DIAMONDS)) == '🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎'
    assert ''.join(Card.get_cards_by_suit(Suit.HEARTS)) == '🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾'
    assert ''.join(Card.get_cards_by_suit(Suit.SPADES)) == '🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮'
