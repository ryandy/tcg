import sys

from dbz.card_power_dragon_ball import CardPowerDragonBall
from dbz.character import Character
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.damage_modifier import DamageModifier


TYPE = 'Dragon Ball'
NAME = 'Earth Dragon Ball 5'
DB_SET = 'Earth'
DB_NUMBER = 5
SAGA = 'Saiyan'
CARD_NUMBER = '77'
RARITY = 3
DECK_LIMIT = 1
CHARACTER = None
STYLE = None
CARD_TEXT = ('Raise any one of your personalities to their highest power stage. Raise your anger'
             ' 2 levels. Draw 2 cards. Place the top 2 cards of your discard pile at the bottom of'
             ' your Life Deck.')


class CardPowerDragonBallEDB5(CardPowerDragonBall):
    def on_play(self, player, phase):
        personality = player.choose_power_stage_target(10)
        personality.adjust_power_stage(10)

        player.adjust_anger(2)

        for _ in range(2):
            player.draw()

        for _ in range(2):
            player.rejuvenate()


CARD_POWER = CardPowerDragonBallEDB5(NAME, CARD_TEXT)
