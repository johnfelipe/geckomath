import fractions
import itertools
import random

import texutils

FRACTIONS = list(set(fractions.Fraction(a, b) for a, b in 
                     itertools.product(xrange(11), xrange(1,6)) 
                     if a/b < 5))

class CircleProblem(object):
    """Find the circle determined by the equation.
    
    Given a 4th degree polynomial, find the center and radius of the circle
    it describes.

    """
    def __init__(self):
        self.statement = 'Find the center and radius of the circle having the following equation:'
        self.center = (random.choice(FRACTIONS), random.choice(FRACTIONS))
        self.radius = random.choice(FRACTIONS)
        self.scale = random.choice([x for x in xrange(-3, 3) if x != 0])
        self.coefficients = (self.scale, self.scale, 
                             -2 * self.scale * self.center[0],
                             -2 * self.scale * self.center[1],
                             self.scale * (self.center[0]**2 
                                           + self.center[1]**2 
                                           - self.radius**2))

    @property
    def polynomial(self):
        const = self.coefficients[4]

        if self.scale > 0:
            poly = '{0}x^{{2}} + {1}y^{{2}} - {2}x - {3}y'
        else:
            poly = '-{0}x^{{2}} - {1}y^{{2}} + {2}x + {3}y'

        if const > 0:
            poly += ' + {4} = 0'
        else:
            poly += ' - {4} = 0'

        rescale = const.denominator
        
        return poly.format(
            *map(texutils.tex_print, 
                 map(lambda x: rescale * x,
                     map(abs, self.coefficients))))

    @property
    def solution(self):
        step1 = r'''Here is the equation you begin with
            \[
            {0}.
            \]
            '''.format(self.polynomial)

        terms = self.polynomial.split()
        const = terms[-3]
        if terms[-4] == '-':
            sign = ''
        else:
            sign = '-'
        step2 = r'''Move the constant term to the other side
            \[
            {0} = {1}{2}
            \]

            '''.format(''.join(terms[:-4]), sign, const)

        step3 = r'''and divide through by the coefficient on the squared terms:
            \[
            \]

            '''

        soln = ''.join([step1, step2, step3])
        return soln

def main():
    prob = CircleProblem()
    print prob.statement
    print r'\begin{enumerate}'
    for n in xrange(10):
        prob = CircleProblem()
        print r'\item',
        print '$', prob.polynomial,
        print r'\qquad',
        print '({0}, {1})'.format(*map(texutils.tex_print, [prob.center[0],
                                                       prob.center[1]]))
        print texutils.tex_print(prob.radius), '$\n\n'
        print prob.solution
    print r'\end{enumerate}'

if __name__ == '__main__':
    print r'\input{/Users/jdougherty/.latex/preamble}'
    print r'\begin{document}'
    main()
    print r'\end{document}'
