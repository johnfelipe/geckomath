import random

from sympy import *
x = symbols('x')

from Problems import Problem

def nonzero_randrange(start, stop):
    retval = 0
    while retval == 0:
        retval = random.randrange(start, stop)

    return retval


def ordinal(value):
    """
    Converts zero or a *postive* integer (or their string 
    representations) to an ordinal value.

    >>> for i in range(1,13):
    ...     ordinal(i)
    ...     
    u'1st'
    u'2nd'
    u'3rd'
    u'4th'
    u'5th'
    u'6th'
    u'7th'
    u'8th'
    u'9th'
    u'10th'
    u'11th'
    u'12th'

    >>> for i in (100, '111', '112',1011):
    ...     ordinal(i)
    ...     
    u'100th'
    u'111th'
    u'112th'
    u'1011th'

    """
    try:
        value = int(value)
    except ValueError:
        return value

    if value % 100//10 != 1:
        if value % 10 == 1:
            ordval = u"%d%s" % (value, "st")
        elif value % 10 == 2:
            ordval = u"%d%s" % (value, "nd")
        elif value % 10 == 3:
            ordval = u"%d%s" % (value, "rd")
        else:
            ordval = u"%d%s" % (value, "th")
    else:
        ordval = u"%d%s" % (value, "th")

    return ordval


class BinomProb(Problem):
    '''A base class for binomial problems.
    
    In general, binomial problems deal with polynomials of the form (a + b)^c.'''

    def __init__(self):
        super(BinomProb, self).__init__()
        self.a = nonzero_randrange(-6,6)
        self.b = nonzero_randrange(-6,6)
        self.c = nonzero_randrange(2, 10)
        self.poly = Poly((self.a * x + self.b)**self.c, x)
        self.inner = Poly(self.a * x + self.b, x)

class BinomExpProb(BinomProb):
    '''A binomial expansion problem.

    Given a term of the form (a + b)^c, compute the expanded polynomial.
    '''

    printable = True
    secname = 'Binomial Expansion Problems'

    def __init__(self, variables=1):
        super(BinomExpProb, self).__init__()
        self.statement = r'''Expand $\left({inner}\right)^{{{c}}}$.'''.format(
            inner=latex(self.inner), c=self.c
        )
        self.answer = r'''${}$'''.format(latex(self.poly))

    @property
    def solution(self):

        terms = [ 
            r'''\binom{{{n}}}{{{k}}}({a}x)^{{{k}}}({b})^{{{m}}}'''.format(
                n=self.c, k=index, a=self.a, b=self.b, m=(self.c-index)
            ) for index in xrange(self.c + 1)] 

        expanded = r'''\\
        &\phantom{{=}} +'''.join([
            '+'.join(terms[3 * i:3*(i+1)])
            for i in xrange(self.c/3 + 1)
        ])

        terms2 = [ 
            r'''({binterm})({aterm})({bterm})'''.format(
                binterm=latex(binomial(self.c, index)), aterm =
                latex(Poly((self.a * x)**index, x)), bterm =
                latex(Poly(self.b**(self.c - index), x))) 
            for index in xrange(self.c + 1)]

        expanded2 = r'''\\
        &\phantom{{=}} +'''.join([
            '+'.join(terms2[3 * i:3*(i+1)])
            for i in xrange(self.c/3 + 1)
        ])

        terms3 = [latex(Poly(self.poly.nth(index) * x**index, x)) 
                  for index in xrange(self.c + 1)] 

        expanded3 = r'''\\
        &\phantom{{=}} +'''.join([
            '+'.join(terms3[4 * i:4*(i+1)])
            for i in xrange(self.c/4 + 1)
        ])

        ans = r'''Applying the binomial theorem:
            \begin{{align*}}
            \left({inner}\right)^{{{c}}} &= {expanded}\\
                                         &= {expanded2}\\
                                         &= {expanded3}
            \end{{align*}}
            '''.format(
                inner=latex(self.inner), c=self.c, expanded=expanded,
                expanded2=expanded2, expanded3=expanded3, 
            )

        return ans


class BinomNthTermProb(BinomProb):
    '''Find the nth term of a binomial expansion.

    Given a polynomial of the form (ax + b)^{c}, find the nth term in the fully
    expanded polynomial.'''

    printable = True
    secname = 'Binomial Expansion Problems'

    def __init__(self):
        super(BinomNthTermProb, self).__init__()
        self.n = random.randrange(self.c + 1)
        self.statement = r'''Find the coefficient of $x^{{{n}}}$ in the
        expansion of $({inner})^{{{c}}}$.
        '''.format(n=self.n, inner=latex(self.inner), c=self.c)
        self.answer = self.poly.nth(self.n)

    @property
    def solution(self):
        ans = r'''The {nth} term of a binomial expansion is given by
        \[
        \binom{{{c}}}{{{n}}}({a}x)^{n}({b})^{k} 
        = ({binterm})({aterm})({bterm})
        = {soln}
        \]
        '''.format(
            nth=ordinal(self.n), c=self.c, n=self.n, a=self.a, b=self.b,
            k=(self.c - self.n), binterm=latex(binomial(self.c, self.n)),
            aterm=latex(Poly((self.a * x)**self.n, x)),
            bterm=latex(Poly(self.b**(self.c - self.n), x)), soln=self.answer
        )

        return ans


class BinomContractProb(BinomProb):
    '''Find the nth term of a binomial expansion.

    Given a polynomial of the form (ax + b)^{c}, find the nth term in the fully
    expanded polynomial.'''

    printable = True
    secname = 'Binomial Expansion Problems'

    def __init__(self):
        super(BinomContractProb, self).__init__()
        self.a = nonzero_randrange(0, 6)
        self.statement = r'''Express ${poly}$ in the form $(ax + b)^{{n}}$.
            '''.format(poly=latex(self.poly))
        self.answer = r'''$({inner})^{{{c}}}$'''.format(
            inner=latex(self.inner), c=self.c)

    @property
    def solution(self):
        if self.b < 0:
            are = 'are'
            posneg = 'negative'
            absp = 'the absolute value of'
        else:
            are = "aren't any"
            posneg = 'positive'
            absp = ''
        deg = '' if self.c == 2 else r'[{c}]'.format(c=self.c)
        ans = r'''The leading term is ${LT}$, and the power on $x$ is {LPOW},
            so $n = {c}$.  There {ARE} minuses, so we know that $b$ is
            {POSNEG}.  To find $a$, we take the {ORD} root of ${ALC}$:
            \[
            a = \sqrt{DEG}{{{ALC}}} = {a}
            \]
            to find $b$, we take the {ORD} root of {ABSP} the constant term:
            \[
            b = \sqrt{DEG}{{{CONST}}} = {b}
            \]
            So the polynomial can be written as {ANS}.
            '''.format(
                LT='{LC}x^{{{c}}}'.format(LC=self.poly.LC(), c=self.c),
                LPOW=self.poly.degree(), c=self.c, ARE=are, POSNEG=posneg,
                ORD=ordinal(self.c), ALC=abs(self.poly.LC()), DEG=deg,
                a=abs(self.a), ABSP=absp, CONST=abs(self.poly.TC()),
                b=abs(self.b), ANS=self.answer
            ) 

        return ans

def main():
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read('geckomath.ini')
    print config.get('LaTeX', 'preamble')

    print r'\begin{enumerate}'

    for i in xrange(10):
        prob = BinomContractProb()
        print r'\item', prob.statement
        if config.getboolean('BinomContractProb', 'solutions'):
            print prob.solution
            print prob.answer

    print r'\end{enumerate}'

    print config.get('LaTeX', 'postamble')

if __name__ == '__main__':
    main()
