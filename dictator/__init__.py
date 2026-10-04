
from otree.api import *
c = cu

doc = '\nOne player decides how to divide a certain amount between himself and the other\nplayer.\nSee: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness\nand the assumptions of economics." Journal of business (1986):\nS285-S300.\n'
class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    INSTRUCTIONS_TEMPLATE = 'dictator/instructions.html'
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    kept = models.CurrencyField(doc='Amount dictator decided to keep for himself', label='I will keep', max=C.ENDOWMENT, min=0)
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = C.ENDOWMENT - group.kept
class Player(BasePlayer):
    pass
class Introduction(Page):
    form_model = 'player'
class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(offer=C.ENDOWMENT - group.kept)
page_sequence = [Introduction, Offer, ResultsWaitPage, Results]