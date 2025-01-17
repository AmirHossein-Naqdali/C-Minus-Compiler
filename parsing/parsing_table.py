from .grammar import productions, first
from .nonterminals import NonTerminals
from .terminals import Terminals

ll1_table = {}
for nonterminal in NonTerminals:
    ll1_table[nonterminal.name] = {}
    row = {}
    for terminal in Terminals:
        row[terminal.name] = None
    ll1_table[nonterminal.name] = row


def create_parsing_table():
    for nonterminal in NonTerminals:
        action_leading_to_epsilon = None
        for production in productions[nonterminal]:
            for terminal in first(production):
                if terminal != Terminals.EPSILON:
                    ll1_table[nonterminal.name][terminal.name] = production
                else:
                    action_leading_to_epsilon = production
        default_value = action_leading_to_epsilon if action_leading_to_epsilon else 'synch'
        for terminal in nonterminal.follow:
            if ll1_table[nonterminal.name][terminal.name] is None:
                ll1_table[nonterminal.name][terminal.name] = default_value
