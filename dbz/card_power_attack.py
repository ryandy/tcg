import copy
import sys

from dbz.card_power import CardPower
from dbz.cost import Cost
from dbz.damage import Damage
from dbz.dragon_ball_card import DragonBallCard
from dbz.state import State
from dbz.util import dprint


# TODO CardPowerCombat class that this, ..Defense, and ..DefenseShield inherit from
class CardPowerAttack(CardPower):
    def __init__(self, name, description, is_physical=None,
                 heroes_only=False, villains_only=False, saiyan_only=False, namekian_only=False,
                 cost=None, damage=None, damage_modifier=None,
                 rejuvenate_count=None, rejuvenate_bottom_count=None, rejuvenate_choice_count=None,
                 own_anger=None, opp_anger=None,
                 main_power=None, any_power=None, opp_power=None,
                 force_end_combat=None,
                 exhaust=True, exhaust_until_next_turn=False,
                 discard=True, remove_from_game=False,
                 is_floating=None, card=None):
        if cost is None:
            cost = Cost.energy_attack() if (is_physical is False) else Cost.none()
        super().__init__(name, description, cost,
                         exhaust=exhaust, exhaust_until_next_turn=exhaust_until_next_turn,
                         discard=discard, remove_from_game=remove_from_game,
                         heroes_only=heroes_only, villains_only=villains_only,
                         saiyan_only=saiyan_only, namekian_only=namekian_only,
                         card=card, is_floating=is_floating)
        if damage is None:
            if is_physical is None:
                damage = Damage.none()
            elif is_physical:
                damage = Damage.physical_attack()
            else:
                damage = Damage.energy_attack()
        damage = damage.copy()
        if damage_modifier:
            damage.modify(damage_modifier)
        self.damage = damage

        self.is_physical = is_physical
        self.rejuvenate_count = rejuvenate_count
        self.rejuvenate_bottom_count = rejuvenate_bottom_count
        self.rejuvenate_choice_count = rejuvenate_choice_count
        self.own_anger = own_anger
        self.opp_anger = opp_anger
        self.main_power = main_power
        self.any_power = any_power
        self.opp_power = opp_power
        self.force_end_combat = force_end_combat

    def copy(self):
        # Note: do not deep copy self.card
        card_power_copy = copy.copy(self)
        card_power_copy.cost = self.cost.copy()
        card_power_copy.damage = self.damage.copy()
        return card_power_copy

    def on_attack(self, player, phase):
        self.on_pay_cost(player, phase)

        self.on_secondary_effects(player, phase)

        if self.is_physical is None:  # Non-combat attacks
            success = True
        elif self.is_physical:
            success = phase.physical_attack(self.damage.copy())
        else:
            success = phase.energy_attack(self.damage.copy())

        if success:
            self.on_success(player, phase)

        self.on_resolved()

        if self.force_end_combat:
            phase.set_force_end_combat()

    def on_secondary_effects(self, player, phase):
        if self.own_anger:
            player.adjust_anger(self.own_anger)
        if self.opp_anger:
            player.opponent.adjust_anger(self.opp_anger)

        if self.main_power:
            player.main_personality.adjust_power_stage(self.main_power)
        if self.any_power:
            personality = player.choose_power_stage_target(self.any_power)
            personality.adjust_power_stage(self.any_power)
        if self.opp_power:
            player.opponent.main_personality.adjust_power_stage(self.opp_power)

        if self.rejuvenate_count:
            for _ in range(self.rejuvenate_count):
                player.rejuvenate()

        if self.rejuvenate_bottom_count:
            for _ in range(self.rejuvenate_bottom_count):
                player.rejuvenate(from_bottom=True)

        if self.rejuvenate_choice_count:
            for _ in range(self.rejuvenate_choice_count):
                player.rejuvenate_with_choice()

    def on_success(self, player, phase):
        pass


class CardPowerPhysicalAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=True)


class CardPowerEnergyAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=False)


class CardPowerNonCombatAttack(CardPowerAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, is_physical=None)


class CardPowerFinalPhysicalAttack(CardPowerPhysicalAttack):
    def __init__(self):
        super().__init__(
            'Final Physical Attack',
            ('Discard a card to perform a physical attack.'
             ' You must pass for the rest of this combat.'),
            cost=Cost(discard=1),
            exhaust=False)

    def on_secondary_effects(self, player, phase):
        super().on_secondary_effects(player, phase)
        player.must_pass_until_next_turn()


# Physical attack used by Piccolo and Tien personalities
class CardPowerPhysicalAttackMultiForm(CardPowerPhysicalAttack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolved_turn = -1
        self.resolved_count = 0

    def on_resolved(self):
        # Reset each turn the power is used
        if self.resolved_turn != State.TURN:
            self.resolved_turn = State.TURN
            self.resolved_count = 0

        self.resolved_count += 1
        if self.resolved_count > 2:
            assert False
        elif self.resolved_count == 2:
            self.player.exhaust_card_until_next_turn(self.card)
        else:
            State.PHASE.set_skip_next_attack_phase()
            State.PHASE.set_next_attack_power(self)
