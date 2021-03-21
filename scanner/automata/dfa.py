import json
import string

from .exceptions import get_exception_by_name
from .state import State


class DFA:
    def __init__(self):
        self.states = dict()
        self.start_state = None
        self.current_state = None

    def reset(self):
        self.current_state = self.start_state

    def can_scan(self, char):
        return self.current_state.transit(char) is not None

    def scan(self, char):
        new_state = self.current_state.transit(char)
        if new_state is None:
            raise get_exception_by_name('INVALID_INPUT')()
        self.current_state = new_state
        new_state.raise_exception()

    @staticmethod
    def from_json_file(json_file):
        dfa = DFA()
        with open(json_file, 'r') as jf:
            data = json.load(jf)
        for state_data in data:
            exception = state_data.get('exception', None)
            if exception:
                exception_class = get_exception_by_name(exception)
            else:
                exception_class = None

            dfa.states[state_data['id']] = State(
                unread=state_data.get('unread', False),
                token_type=state_data.get('type'),
                exception_class=exception_class,
            )

        for state_data in data:
            source = dfa.states.get(state_data['id'])
            for transition in state_data.get('transitions', []):
                chars = DFA.parse_transition_chars(transition[0])
                dest = dfa.states.get(transition[1])
                source.add_transition(chars, dest)

        dfa.start_state = dfa.states.get(0)
        dfa.reset()
        return dfa

    @staticmethod
    def parse_transition_chars(chars):
        if type(chars) == list:
            return list(map(
                lambda x: chr(x) if type(x) == int else x,
                chars,
            ))
        if chars == '@digit':
            return list(string.digits)
        if chars == '@letter':
            return list(string.ascii_letters)
        if chars == '@default':
            return [chr(i) for i in range(128)] + ['']
        return list(chars)
