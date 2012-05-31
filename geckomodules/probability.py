from __future__ import division

import collections
import fractions
import random


from Problems import Problem

Condition = collections.namedtuple('Condition', ['sing', 'plural'])

# a scenario is a dictionary of survey subjects,
SCENARIOS = [
    {
        'scale': 1000,
        'ptype': 'Canadian hockey fans',
        'conditions': [
            Condition('a Canucks fan', 'Canucks fans'),
            Condition('an Oilers fan', 'Oilers fans'),
            Condition('a Flames fan', 'Flames fans'),
            Condition('a Jets fan', 'Jets fans'),
            Condition('a Maple Leafs fan', 'Maple Leafs fans'),
            Condition('a Senators fan', 'Senators fans'),
            Condition('a Canadiens fan', 'Canadiens fans'),
        ],
    }
]


class TwoVarChanceProb(Problem):
    '''A probability problem of two variables.

    Three variables characterize the probability space, assuming that there are
    100 events:
        A - the number of events that are A
        B - the number of events that are B
        AB - the number of events that are both A and B

    The information provided and requested will be randomly selected from
    Boolean combinations of A and B.
    '''
    printable = True
    secname = 'Basic Probability'

    # probtypes are tuples of the form (givens, find).  U is the total number.
    # -A is \lnot A
    probtypes = [
        (['U', 'A', 'B', 'AB'], 'A-B')
    ]

    def __init__(self):
        super(TwoVarChanceProb, self).__init__()
        self.scenario = random.choice(SCENARIOS)
        self.U = self.scenario['scale']
        onlyA = random.randrange(self.U)
        onlyB = random.randrange(self.U - onlyA)
        both = random.randrange(self.U - onlyA - onlyB)
        self.A = onlyA + both
        self.B = onlyB + both
        self.AB = both

        self.givens, self.to_find = random.choice(self.probtypes)

        self.condA, self.condB = random.sample(self.scenario['conditions'], 2)

    @property
    def statement(self):
        givens = [
            ' are '.join([
                given.replace(
                    '-AB', str(self.U - self.AB)
                ).replace(
                    '-A', str(self.U - self.A)
                ).replace(
                    '-B', str(self.U - self.B)
                ).replace(
                    'AB', str(self.AB)
                ).replace(
                    'A', str(self.A)
                ).replace(
                    'B', str(self.B)
                ),
                given.replace(
                    '-', 'not '
                ).replace(
                    'AB', 'both {0} and {1}'.format(self.condA.plural,
                                                    self.condB.plural)
                ).replace(
                    'A', self.condA.plural
                ).replace(
                    'B', self.condB.plural
                )
            ])
            for given in self.givens if given != 'U'
        ]

        if len(givens) > 1:
            results = ' and '.join([', '.join(givens[:-1]), givens[-1]])
        else:
            results = givens[-1]

        find_cond = self.to_find.replace(
                'A-B', 'is {0} but is not {1}'.format(self.condA.sing,
                                                      self.condB.sing)
            ).replace(
                'B-A', 'is {0} but is not {1}'.format(self.condB.sing,
                                                      self.condA.sing)
            ).replace(
                '-', 'is not '
            ).replace(
                'AB', 'is both {0} and {1}'.format(self.condA.sing,
                                                   self.condB.sing)
            ).replace(
                'A', ' '.join(['is', self.condA.sing])
            ).replace(
                'B', ' '.join(['is', self.condB.sing])
            )

        npeople = ' '.join([str(self.U), self.scenario['ptype']])
        statement = '''
        A survey of {npeople} shows that {results}.  What is the probability
        that a randomly chosen person from this survey {find_cond}?
        '''.format(npeople=npeople, results=results, find_cond=find_cond)

        return statement

    @property
    def answer(self):
        return '{}\%'.format(
            self.to_find.replace(
                '-AB', str((1 - (self.AB / self.U))*100)
            ).replace(
                'A-B', str(((self.A - self.AB) / self.U)*100)
            ).replace(
                '-A', str((1 - (self.A / self.U))*100)
            ).replace(
                '-B', str((1 - (self.B / self.U))*100)
            ).replace(
                'AB', str((self.AB / self.U)*100)
            ).replace(
                'A', str((self.A / self.U)*100)
            ).replace(
                'B', str((self.B / self.U)*100)
            )
        )

    @property
    def solution(self):
        return ''


if __name__ == '__main__':
    # add something here!
    pass
