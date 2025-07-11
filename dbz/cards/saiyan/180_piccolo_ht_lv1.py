import sys

from dbz.card_power_attack import CardPowerEnergyAttack, CardPowerPhysicalAttack
from dbz.card_power_on_draw import CardPowerOnDraw
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Personality'
NAME = 'Piccolo HT Lv1'
LEVEL = 1
SAGA = 'Saiyan'
CARD_NUMBER = '180'
RARITY = 4
DECK_LIMIT = 1
CHARACTER = 'Piccolo'
IS_HERO = True
POWER_UP_RATING = 1
POWER_STAGES = range(500, 1400+1, 100)
CARD_TEXT = ('When defending in combat, take the bottom discard card as well in your three'
             ' card draw.')

CARD_POWER = CardPowerOnDraw(
    NAME, CARD_TEXT, exhaust=False, discard=False,
    own_defend_draw_from_discard_add=1)
