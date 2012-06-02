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

class TwoUrnProb(Problem):
    '''A probability problem involving two urns.

    There are two urns, each containing balls of two types.
    '''
    printable = True
    secname = 'P4-type'

    def __init__(self):
        super(TwoUrnProb, self).__init__()
        # XXX: is this a good limit? should we even /have/ a limit?
        limit = 20 
        red = (random.randrange(1,21), random.randrange(1,21))
        self.urns = [
            {'red' : red[0],
             'blue' : min(random.randrange(1,21), limit - red[0])},
            {'red' : red[1],
             'blue' : min(random.randrange(1,21), limit - red[1])}
        ]
        for i in (0,1):
            self.urns[i]['total'] = self.urns[i]['red'] + self.urns[i]['blue']

        self.answer = self.urns[1]['blue']
        self.pred = [
            self.urns[0]['red'] / self.urns[0]['total'],
            self.urns[1]['red'] / self.urns[1]['total']
        ]
        self.pblue = [
            self.urns[0]['blue'] / self.urns[0]['total'],
            self.urns[1]['blue'] / self.urns[1]['total']
        ]
        self.prob_both_red = self.pred[0] * self.pred[1]
        self.prob_both_blue = self.pblue[0] * self.pblue[1]
        self.prob_same = self.prob_both_red + self.prob_both_blue



    @property
    def statement(self):
        text = r'''An urn contains {LTOT} balls: {LRED} {RED} and {LBLUE}
        {BLUE}.  A second urn contains {RRED} {RED} balls and an unknown number
        of {BLUE} balls.  A single ball is drawn from each urn.  The
        probability that both balls are the same color is {SAMEPROB:.2f}.
        Calculate the number of {BLUE} balls in the second urn.
        '''.format(
            LTOT=(self.urns[0]['red'] + self.urns[0]['blue']),
            LRED=self.urns[0]['red'], RED='red', 
            LBLUE=self.urns[0]['blue'], BLUE='blue',
            RRED=self.urns[0]['red'], RBLUE=self.urns[0]['blue'],
            SAMEPROB=self.prob_same
        )

        return text

    @property
    def solution(self):
        text=r'''Since we're given all of the details of the first urn, we can
        calculate the probability of each color being drawn from the first urn:
        \[
        P_{{1}}(\text{{{RED}}}) = \frac{{\text{{{LRED} {RED} balls}}}}{{
                                   \text{{{LTOT} total balls}}}}
                          = {LPRED:.2f},
        \qquad
        P_{{1}}(\text{{{BLUE}}}) = \frac{{\text{{{LBLUE} {BLUE} balls}}}}{{
                                   \text{{{LTOT} total balls}}}}
                           = {LPBLUE:.2f}.
        \]
        We know that there are {RRED} {RED} balls in the second urn.  Suppose
        there are \(x\) {BLUE} balls in the second urn, so that there are
        \({RRED} + x\) balls total.  So
        \[
        P_{{2}}(\text{{{RED}}}) = \frac{{\text{{{RRED} {RED} balls}}}}{{
                                   {RRED} + x\text{{ total balls}}}},
        \qquad
        P_{{2}}(\text{{{BLUE}}}) = \frac{{x\text{{ {BLUE} balls}}}}{{
                                   {RRED} + x\text{{ total balls}}}}.
        \]

        Now, if we draw two balls from the urns, the outcome that they will
        both be {RED} is mutually exclusive with the outcome that they will both
        be {BLUE}.  So the probability that either will happen is
        \(P(\text{{both {RED}}}) + P(\text{{both {BLUE}}})\).  Since the two
        draws are independent, \(P(\text{{both {RED}}}) =
        P_{{1}}(\text{{{RED}}}) \times P_{{2}}(\text{{{RED}}})\), so
        \begin{{align*}}
        P(\text{{both {RED}}}) 
        &= P_{{1}}(\text{{{RED}}}) \times P_{{2}}(\text{{{RED}}}) 
        = {LPRED:.2f} \times \frac{{{RRED}}}{{{RRED} + x}}
        =\frac{{{REDSIMP:.2f}}}{{{RRED} + x}} \\
        P(\text{{both {BLUE}}}) 
        &= P_{{1}}(\text{{{BLUE}}}) \times P_{{2}}(\text{{{BLUE}}}) 
        = {LPBLUE:.2f} \times \frac{{x}}{{ {RRED} + x}}
        = \frac{{{LPBLUE:.2f}x}}{{ {RRED} + x}} \\
        \end{{align*}}
        and so
        \[
        P(\text{{same}}) 
        = {SAMEPROB:.2f} 
        = \frac{{{REDSIMP:.2f}}}{{{RRED} + x}} 
            + \frac{{{LPBLUE:.2f}x}}{{ {RRED} + x}}
        = \frac{{{REDSIMP:.2f} + {LPBLUE:.2f}x}}{{ {RRED} + x}}
        \]
        Now we just need to solve for \(x\):
        \begin{{align*}}
        {SAMEPROB:.2f} &= \frac{{{REDSIMP:.2f} + {LPBLUE:.2f}x}}{{ {RRED} + x}}
        \\
        {LHS1:.2f} + {SAMEPROB:.2f}x &= {REDSIMP:.2f} + {LPBLUE:.2f}x \\
        {LHS2:.2f} &= {RHS2:.2f}x \\
        x &= {RBLUE}
        \end{{align*}}
        '''.format(
            RED='red', LRED=self.urns[0]['red'], LPRED=self.pred[0],
            BLUE='blue', LBLUE=self.urns[0]['blue'], LPBLUE=self.pblue[0],
            REDSIMP=(self.pred[0] * self.urns[1]['red']),
            LTOT=self.urns[0]['total'],
            RRED=self.urns[1]['red'], SAMEPROB=self.prob_same,
            LHS1=(self.prob_same * self.urns[1]['red']),
            LHS2=((self.prob_same * self.urns[1]['red']) 
                  - (self.pred[0] * self.urns[1]['red'])),
            RHS2=(self.pblue[0] - self.prob_same),
            RBLUE=self.urns[1]['blue'],
        ) 
        return text



if __name__ == '__main__':
    # add something here!
    pass
