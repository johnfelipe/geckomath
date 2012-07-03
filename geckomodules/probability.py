from __future__ import division

import collections
import fractions
import logging
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


def latex(fraction):
    if fraction.denominator == 1:
        texed = str(fraction)
    else:
        return r'\ensuremath{{\frac{{{N}}}{{{D}}}}}'.format(
            N=fraction.numerator, D=fraction.denominator
        )
    
    return texed

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

class NofMProb(Problem):
    '''A probability problem involving choices.

    There are M options, everyone must choose N of them or none at all.
    '''
    printable = True
    secname = 'P5-type'
    flavors = (
        {'statement':
         r'''An insurer offers a health plan to the employees of a large
         company.  As part of this plan, the individual employees may choose
         exactly two of the supplementary coverages A, B, and C, or they may
         choose no supplementary coverage.  The proportions of the company's
         employees that choose coverages A, B, and C are {PROPA}, {PROPB}, and
         {PROPC}, respectively.  Determine the probability that a randomly
         chosen employee will choose no supplementary coverage.
         ''',
         'solution': 
         r'''For simplicity, let's work with numbers of people, instead of
         proportions.  The g.c.d.~of the three proportions is {GCD}, so suppose
         there are {GCD} people.  Then {CHOOSEA} chose A, {CHOOSEB} chose B,
         and {CHOOSEC} chose C, and {CHOICES} choices were made in total.  But
         each person made 2 choices, so {PCHOSE} chose to take supplementary
         coverage.  This leaves {CHOOSEN} of {GCD} people who made no choice,
         or a proportion of {ANSWER}.  
         '''
        },
        {'statement':
         r'''An ice cream store sells single- and double-scoop ice cream cones
         in vanilla, chocolate, and strawberry flavors.  Customers who order a
         double-scoop must choose exactly two of these flavors.  {PROPA} of the
         customers choose a double-scoop with vanilla, {PROPB} choose a
         double-scoop with chocolate, and {PROPC} choose a double-scoop with
         strawberry.  Determine the probability that a randomly
         chosen customer will choose a single-scoop ice cream cone.
         ''',
         'solution': 
         r'''For simplicity, let's work with numbers of people, instead of
         proportions.  The g.c.d.~of the three proportions is {GCD}, so suppose
         there are {GCD} people.  Then {CHOOSEA} chose vanilla, {CHOOSEB} chose
         chocolate, and {CHOOSEC} chose strawberry, and {CHOICES} choices were
         made in total.  But each person made 2 choices, so {PCHOSE} chose to
         take a double-scoop.  This leaves {CHOOSEN} of {GCD} people
         who took a single-scoop, or a proportion of {ANSWER}.  
         '''
        }
    ,)

    def __init__(self, n=2, m=3, max_denominator=20):
        super(NofMProb, self).__init__()
        
        self.flavor = random.choice(self.flavors)
        choices = collections.defaultdict(int)
        choices['None'] = random.randrange(1,max_denominator)
        for person in xrange(max_denominator - choices['None']):
            for choice in random.sample(('A', 'B', 'C'), 2):
                choices[choice] += 1

        self.propA = fractions.Fraction(choices['A'],max_denominator)
        self.propB = fractions.Fraction(choices['B'],max_denominator)
        self.propC = fractions.Fraction(choices['C'],max_denominator)
        self.propNone = fractions.Fraction(choices['None'],max_denominator)

        self.statement = self.flavor['statement'].format(
            PROPA=latex(self.propA), PROPB=latex(self.propB),
            PROPC=latex(self.propC)
        )

        self.answer = latex(self.propNone)

    @property
    def solution(self):

        gcd = reduce(fractions.gcd, 
                     (self.propA, self.propB, self.propC)).denominator 
        choices = {}
        choices['A'] = self.propA * gcd
        choices['B'] = self.propB * gcd
        choices['C'] = self.propC * gcd
        total_choices = sum(choices.values())
        choices['None'] = self.propNone * gcd

        

        text = self.flavor['solution'].format(
            GCD=gcd, CHOOSEA=choices['A'], CHOOSEB=choices['B'],
            CHOOSEC=choices['C'], CHOICES=total_choices,
            PCHOSE=(total_choices/2), CHOOSEN=choices['None'],
            ANSWER=self.answer
        )

        return text

class ConditionalProb(Problem):
    '''A probability problem for DeMorgan's laws.'''
    printable = True
    secname = 'P7-type'
    def __init__(self):
        super(ConditionalProb, self).__init__()

        self.probs = {}
        self.probs['D'] = random.randrange(1, 30) / 100
        self.probs['S'] = random.randrange(1, self.probs['D']*100) / 100
        self.probs['T'] = random.randrange(1, 10) / 100

        self.statement = r'''An actuary is studying the prevalence of three
        health risk factors, denoted by A, B, and C, within a population of
        women.  For each of the three factors, the probability is {SPROB} that
        a woman in the population has only this risk factor (and no others).
        For any two of the three facts, the probability is {DPROB} that she has
        exactly these two risk factors (but not the other).  The probability
        that a woman has all three risk factors, given that she has A and B,
        is {PPROB:.2f}.  What is the probability that a woman has none of
        the three risk factors, given that she does not have risk factor A?
        '''.format(
            SPROB=self.probs['S'], DPROB=self.probs['D'],
            PPROB=(self.probs['T']/(self.probs['T'] + self.probs['D']))
        )
        self.answer = (
            (1-(3*self.probs['S'] + 3*self.probs['D'] + self.probs['T']))/
            (1 - (self.probs['S'] + 2*self.probs['D'] + self.probs['T']))
        )

    @property
    def solution(self):
        text = r'''This Venn Diagram describes the problem:
        \[
        \text{{not yet implemented}}
        \]
        We are given
        \[
        P(A \cap B' \cap C') = P(A' \cap B \cap C') = P(A' \cap B' \cap C) =
        {SPROB:.2f}
        \]
        (having exactly one risk factor means not having either of the other
        two).  We are also given
        \[
        P(A \cap B \cap C') = P(A \cap B' \cap C) = P(A' \cap B \cap C) =
        {DPROB:.2f}.
        \]
        Finally, we are given
        \[
        P(A \cap B \cap C \mid A \cap B) = {PPROB:.2f}.
        \]
        Then
        \[
        P(A \cap B \cap C \mid A \cap B) = \frac{{P(A \cap B \cap C)}}{{P(A \cap
        B)}} = {PPROB:.2f}
        \]
        so
        \[
        P(A \cap B \cap C) = {PPROB:.2f} \cdot P(A \cap B).
        \]
        Referring to the diagram, let $P(A \cap B \cap C) = x$, so that $P(A
        \cap B) = x + {DPROB:.2f}$.  Then
        \[
        x = P(A \cap B \cap C) = {PPROB:.2f} \cdot P(A \cap B) =
        {PPROB:.2f}(x+{DPROB:.2f})
        \]
        So $x = {TPROB:.2f}$.  The four regions of A then sum to $P(A) =
        {SPROB:.2f} + {DPROB:.2f}+ {DPROB:.2f} + {TPROB:.2f} = {APROB:.2f}$, so
        $P(A') = 1 - P(A) = {APPROB:.2f}$.  The problem asks for
        \[
        P(A' \cap B' \cap C' \mid A') = \frac{{P(A' \cap B' \cap C')}}{{P(A')}}
        = \frac{{P(A' \cap B' \cap C')}}{{{APPROB:.2f}}}
        \]
        And the numerator is just the complement of all the numbered regions:
        \[
        P(A' \cap B' \cap C' \mid A') = \frac{{1-(3 \times {SPROB:.2f} + 3
        \times {DPROB:.2f} + {TPROB:.2f})}}{{{APPROB:.2f}}} =
        \frac{{{NUM}}}{{{APPROB:.2f}}} = {ANS:.3f}
        \]
        '''.format(
            SPROB=self.probs['S'], DPROB=self.probs['D'],
            TPROB=self.probs['T'],
            PPROB=(self.probs['T']/(self.probs['T'] + self.probs['D'])),
            APROB=(self.probs['S'] + 2*self.probs['D'] + self.probs['T']),
            APPROB=(1 - 
                    (self.probs['S'] + 2*self.probs['D'] + self.probs['T'])),
            NUM=(1-(3*self.probs['S'] + 3*self.probs['D'] + self.probs['T'])),
            ANS=self.answer
        )
        return text

def percent(num):
    'A LaTeX-safe way of outputting a percentage'
    return ''.join([str(int(num * 100)), r'\%'])

class TwoVarProb(Problem):
    '''A two-variable probability problem.

    I am having the darndest time doing this synthetically, so I'm just going
    to have to do it analytically.  Hopefully this class will one day subsume
    TwoUrnProb.  Naming conventions: [ (L (M) R) ]
    '''
    printable = True
    secname = 'Two Variable Probability'
    ptypes = (
        {'statement': r'''The probability that a visit to a primary care
         physician's (PCP) office results in neither lab work nor referral to a
         specialist is {PPnLAnR}.  Of those coming to a PCP's office, {PPR} are
         referred to specialists and {PPL} require lab work.  Determine the
         probability that a visit to a PCP's office results in both lab work
         and referral to a specialist.
         ''',
         'answer': '{PLAR}',
         'solution': r'''Label the classes like so:
         \begin{{itemize}}
         \item[$L$:] lab work needed
         \item[$R$:] referral to a specialist given
         \end{{itemize}}
         We are given $P(L' \cap R') = {PnLAnR}$, $P(R) ={PR}$, and $P(L)={PL}$.
         It follws that $P(L \cup R) = 1 - P(L' \cap R') = {PLOR}$, and then
         \[
         P(L \cap R) = P(L) + P(R) - P(L \cup R) = {PL} + {PR} - {PLOR} =
         {PLAR}.
         \]
         So the probability of both is ${PLAR}$.
         ''',
         'ltest':  lambda: True if random.gauss(.3, .3) > .5 else False,
         'rtest':  lambda: True if random.gauss(.3, .3) > .5 else False,
        },
        {'statement': r'''You are given $P(A \cup B) = {PLOR}$ and $P(A \cup
         B') = {PLOnR}$.  Determine $P(A)$.
         ''',
         'answer': '{PL}',
         'solution': r'''$P(A \cup B) = P(A) + P(B) - P(A \cap B)$ and $P(A \cup
         B') = P(A) + P(B') - P(A \cap B')$.  We use the relationship $P(A) =
         P(A \cap B) + P(A \cap B')$.  Then
         \begin{{align*}}
         P(A \cup B) + P(A \cup B') 
         &= P(A) + P(B) - P(A \cap B) \\&\phantom{{=}}+ P(A) + P(B') - P(A \cap B')\\
         &= 2P(A) + 1 - P(A) = P(A) + 1
         \end{{align*}}
         Since $P(B) + P(B') = 1$.  Therefore, ${PLOR} + {PLOnR} = P(A) + 1$ so
         that $P(A) = {PL}$.
         ''',
         'ltest': lambda: True if random.gauss(.3, .3) > .5 else False, 
         'rtest': lambda: True if random.gauss(.3, .3) > .5 else False, 
        },
    )

    def __init__(self, U=100):

        self.ptype = random.choice(self.ptypes)

        self.L = set()
        self.R = set()
        self.U = set(xrange(U))
        for entry in self.U:
            ladd = self.ptype['ltest']()
            if ladd:
                self.L.add(entry)
            radd = self.ptype['rtest']()
            if radd:
                self.R.add(entry)

        values = {
            'PL': len(self.L)/len(self.U), 
            'PR': len(self.R)/len(self.U),
            'PnL': len(self.U - self.L)/len(self.U),
            'PnR': len(self.U - self.R)/len(self.U),
            'PLAR': len(self.L & self.R)/len(self.U),
            'PnLAR': len((self.U - self.L) & self.R)/len(self.U),
            'PLAnR': len(self.L & (self.U - self.R))/len(self.U),
            'PnLAnR': len((self.U - self.L) & (self.U - self.R))/len(self.U),
            'PLOR': len(self.L | self.R)/len(self.U),
            'PnLOR': len((self.U - self.L) | self.R)/len(self.U),
            'PLOnR': len(self.L | (self.U - self.R))/len(self.U),
            'PnLOnR': len((self.U - self.L) | (self.U - self.R))/len(self.U),
        }

        for key in values.keys():
            values['P'+key] = percent(values[key])

        self.statement = self.ptype['statement'].format(**values)

        self.answer = self.ptype['answer'].format(**values)

        self.solution = self.ptype['solution'].format(**values)

class ThreeVarProb(Problem):
    '''A three-variable probability problem.

    This ought to be combined with TwoVarProb into an Nvar prob.
    '''
    printable = True
    secname = 'Three Variable Probability'
    ptypes = (
        {'statement': r'''A survey of a group's viewing habits over the last
         year revealed the following information:
         \begin{{itemize}}
         \item {PPA} watched gymnastics
         \item {PPB} watched baseball
         \item {PPC} watched soccer
         \item {PPAAB} watched gymnastics and baseball
         \item {PPBAC} watched baseball and soccer
         \item {PPAAC} watched gymnastics and soccer
         \item {PPAABAC} watched all three sports
         \end{{itemize}}
         Calculate the percentage of the group that watched none of the three
         sports during the last year.
         ''',
         'answer': '{PPnAAnBAnC}',
         'solution': r'''Label the classes as follows:
         \begin{{itemize}}
         \item[$G$:] watched gymnastics
         \item[$B$:] watched baseball
         \item[$S$:] watched soccer
         \end{{itemize}}
         We need to find $P(G' \cap B' \cap S')$.  By DeMorgan's law we have
         \[
         P(G' \cap B' \cap S') = 1 - P(G \cup B \cup S).
         \]
         We use the relationship
         \begin{{align*}}
         P(G \cup B \cup S) &= P(G) + P(B) + P(S) \\&\phantom{{=}}- (P(G \cap B) + P(G \cap S) +
         P(B \cap S)) \\&\phantom{{=}}+ P(G \cap B \cap S)
         \end{{align*}}
         and the values from the statement:
         \begin{{itemize}}
         \item $P(G) = {PPA}$
         \item $P(B) = {PPB}$
         \item $P(S) = {PPC}$
         \item $P(G\cap B) = {PPAAB}$
         \item $P(B\cap S) = {PPBAC}$
         \item $P(G\cap S) = {PPAAC}$
         \item $P(G\cap B\cap S) = {PPAABAC}$
         \end{{itemize}}
         Then $P(G \cup B \cup S) = {PAOBOC}$ and $P(G' \cap B' \cap S') = 1 -
         {PAOBOC} = {PnAAnBAnC}$.
         ''',
         'ltest':  lambda: True if random.gauss(.3, .3) > .5 else False,
         'rtest':  lambda: True if random.gauss(.3, .3) > .5 else False,
        },
    )

    def __init__(self, U=100):

        self.ptype = random.choice(self.ptypes)

        self.A = set()
        self.B = set()
        self.C = set()
        self.U = set(xrange(U))
        for entry in self.U:
            for group in (self.A, self.B, self.C):
                if self.ptype['rtest']():
                    group.add(entry)

        values = {
            'PA': len(self.A)/len(self.U),
            'PB': len(self.B)/len(self.U),
            'PC': len(self.C)/len(self.U),
            'PnA': len((self.U - self.A))/len(self.U),
            'PnB': len((self.U - self.B))/len(self.U),
            'PnC': len((self.U - self.C))/len(self.U),
            'PAAB': len(self.A & self.B)/len(self.U),
            'PAAC': len(self.A & self.C)/len(self.U),
            'PAAnB': len(self.A & (self.U - self.B))/len(self.U),
            'PAAnC': len(self.A & (self.U - self.C))/len(self.U),
            'PBAC': len(self.B & self.C)/len(self.U),
            'PBAnA': len(self.B & (self.U - self.A))/len(self.U),
            'PBAnC': len(self.B & (self.U - self.C))/len(self.U),
            'PCAnA': len(self.C & (self.U - self.A))/len(self.U),
            'PCBnB': len(self.C & (self.U - self.B))/len(self.U),
            'PAABAC': len(self.A & self.B & self.C)/len(self.U),
            'PAABAnC': len(self.A & self.B & (self.U - self.C))/len(self.U),
            'PAAnBAC': len(self.A & (self.U - self.B) & self.C)/len(self.U),
            'PAAnBAnC': len(self.A & (self.U - self.B) & (self.U - self.C))/len(self.U),
            'PnAABAC': len((self.U - self.A) & self.B & self.C)/len(self.U),
            'PnAABAnC': len((self.U - self.A) & self.B & (self.U - self.C))/len(self.U),
            'PnAAnBAC': len((self.U - self.A) & (self.U - self.B) & self.C)/len(self.U),
            'PnAAnBAnC': len((self.U - self.A) & (self.U - self.B) & (self.U - self.C))/len(self.U),
            'PAOB': len(self.A | self.B)/len(self.U),
            'PAOC': len(self.A | self.C)/len(self.U),
            'PAOnB': len(self.A | (self.U - self.B))/len(self.U),
            'PAOnC': len(self.A | (self.U - self.C))/len(self.U),
            'PBOC': len(self.B | self.C)/len(self.U),
            'PBOnA': len(self.B | (self.U - self.A))/len(self.U),
            'PBOnC': len(self.B | (self.U - self.C))/len(self.U),
            'PCOnA': len(self.C | (self.U - self.A))/len(self.U),
            'PCOnB': len(self.C | (self.U - self.B))/len(self.U),
            'PAOBOC': len(self.A | self.B | self.C)/len(self.U),
            'PAOBOnC': len(self.A | self.B | (self.U - self.C))/len(self.U),
            'PAOnBOC': len(self.A | (self.U - self.B) | self.C)/len(self.U),
            'PAOnBOnC': len(self.A | (self.U - self.B) | (self.U - self.C))/len(self.U),
            'PnAABAC': len((self.U - self.A) & self.B & self.C)/len(self.U),
            'PnAABAnC': len((self.U - self.A) & self.B & (self.U - self.C))/len(self.U),
            'PnAAnBAC': len((self.U - self.A) & (self.U - self.B) & self.C)/len(self.U),
            'PnAAnBAnC': len((self.U - self.A) & (self.U - self.B) & (self.U - self.C))/len(self.U),
        }

        for key in values.keys():
            values['P'+key] = percent(values[key])

        self.statement = self.ptype['statement'].format(**values)

        self.answer = self.ptype['answer'].format(**values)

        self.solution = self.ptype['solution'].format(**values)

if __name__ == '__main__':
    # add something here!
    pass
