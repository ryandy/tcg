import sys

from dbz.card_power_defense import CardPowerEnergyDefense, CardPowerAnyDefense
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Combat'
NAME = 'Cutting the Tail'
SUBTYPE = 'Combat - Defense'
SAGA = 'Saiyan'
CARD_NUMBER = '200'
RARITY = 5
DECK_LIMIT = None
CHARACTER = None
STYLE = None
CARD_TEXT = ('Set your opponent\'s anger at 0. Remove from the game after use.')

CARD_POWER = CardPowerAnyDefense(
    NAME, CARD_TEXT, opp_anger=-5, remove_from_game=True,
    damage_modifier=DamageModifier.none())
