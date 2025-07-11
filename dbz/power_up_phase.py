import sys

from dbz.card_power_on_end_of_power_up_phase import CardPowerOnEndOfPowerUpPhase
from dbz.card_power_on_entering_power_up_phase import CardPowerOnEnteringPowerUpPhase
from dbz.phase import Phase
from dbz.state import State


class PowerUpPhase(Phase):
    def __init__(self, player):
        self.player = player
        self.force_skip_combat = False

    def set_force_skip_combat(self):
        self.force_skip_combat = True

    def execute(self):
        State.PHASE = self

        for player in State.gen_players():
            card_powers = player.get_valid_card_powers(CardPowerOnEnteringPowerUpPhase)
            for card_power in card_powers:
                card_power.on_entering_power_up_phase(self)

        self.player.main_personality.power_up(tokui_waza=self.player.tokui_waza)
        for ally in self.player.allies:
            ally.power_up(is_ally=True)

        for player in State.gen_players():
            card_powers = player.get_valid_card_powers(CardPowerOnEndOfPowerUpPhase)
            for card_power in card_powers:
                card_power.on_end_of_power_up_phase(self)
