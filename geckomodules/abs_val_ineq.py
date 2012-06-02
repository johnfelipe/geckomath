import random

from sympy import *
# XXX: I am a terrible person for making this a global var
x = symbols('x')

from Problems import Problem

class AbsValProb(Problem):
    '''An absolute value problem.

    Given an inequality of the form |ax + b| > c, find the range of acceptable
    x's'''

    printable = True
    secname = 'Absolute-Value Inequalities'

    def __init__(self):
        super(AbsValProb, self).__init__()
        self.LHS = Poly(random.randrange(1,101)*x + random.randrange(101), x)
        self.RHS = Poly(random.randrange(-10,101), x)
        self.compop = random.choice(['>', r'\geq', '<', r'\leq'])

    @property
    def statement(self):
        eqn = r'''\abs{{{0}}} {1} {2}
        '''.format(latex(self.LHS), self.compop, latex(self.RHS))
        return 'Solve ${}$.'.format(eqn)

    @property
    def answer(self):
        if self.RHS.TC() < 0:
            if self.compop in ('>', r'\geq'):
                return 'All real numbers.'
            else:
                return 'No solution.'

        a = Poly(self.LHS.LC(), x)
        b = Poly(self.LHS.TC(), x)
        c = self.RHS
        zeros = [latex((-c-b)/a), latex((c-b)/a)]
        if self.compop in ('>', r'\geq'):
            opop = '<' if self.compop == '>' else r'\leq'
            ans = '${}$ or ${}$'.format(
                'x {} {}'.format(opop, zeros[0]), 
                'x {} {}'.format(self.compop, zeros[1]))

        elif self.compop in ('<', r'\leq'):
            ans = '${0} {1} x {1} {2}$'.format(
                zeros[0], self.compop, zeros[1])

        return ans

    @property
    def solution(self):
        if self.RHS.TC() < 0:
            return self.solve_trick_q()

        a = Poly(self.LHS.LC(), x)
        b = Poly(self.LHS.TC(), x)
        c = self.RHS
        zeros = [latex((-c-b)/a), latex((c-b)/a)]
        if self.compop in ('>', r'\geq'):
            return self.solve_geq_q(a, b, c)
        else:
            return self.solve_leq_q(a, b, c)

    def solve_trick_q(self):
        if self.compop in ('<', '\leq'):
            ans = r'''An absolute value can never be negative, so there is no
                solution to this inequality.'''
        else:
            ans = r''' 
            An absolute value is always positive or zero, so it will
                always be greater than a negative number.  Hence, this
                inequality is true for all real numbers.'''

        return ans

    def solve_geq_q(self, a, b, c):
        if self.compop == '>':
            opop = '<'
            openbrak, closebrak = '(', ')'
        else:
            opop = r'\leq'
            openbrak, closebrak = '[', ']'
        #XXX: make this a template.
        ans = r'''
        First, eliminate the absolute value bars by splitting the
            inequality into two inequalities:
            \[
            {LHS} {opop} {nRHS} \qquad \text{{or}} \qquad {LHS} {compop} {RHS}.
            \]
            Then solve each inequality normally.
            \begin{{align*}}
            {LHS1} {opop} {nRHS1} \qquad &\text{{or}} \qquad {LHS1} {compop}
            {RHS1} \\
            x {opop} {nRHS2} \qquad &\text{{or}} \qquad x {compop} {RHS2}.
            \end{{align*}}
            The solution to the inequality can be expressed in either of the
            following ways:
            \begin{{align*}}
            x {opop} {nRHS2} \qquad &\text{{or}} \qquad x {compop} {RHS2} \\
            \left(-\infty, {nRHS2}\right{closebrak} 
            &\cup 
            \left{openbrak}{RHS2}, \infty\right)
            \end{{align*}}
            '''.format( 
                LHS=latex(self.LHS), opop=opop, nRHS=latex(-self.RHS),
                compop=self.compop, RHS=latex(self.RHS), 
                LHS1=latex(self.LHS - b), nRHS1=latex(-c-b), RHS1=latex(c-b),
                nRHS2=latex((-c-b)/a), RHS2=latex((c-b)/a), openbrak=openbrak,
                closebrak=closebrak
            ) 
        return ans

    def solve_leq_q(self, a, b, c):
        openbrak, closebrak = ('(', ')') if self.compop == '<' else ('[', ']')
        ans = r'''First, eliminate the absolute value by transforming the
        inequality into a linear inequality:
        \[
        {LB} {compop} {LHS} {compop} {UB}.
        \]
        Then solve the linear inequality in the usual way
        \begin{{align*}}
        {LB1} &{compop}  {LHS1} {compop} {UB1} \\
        {LB2} &{compop}  x {compop} {UB2}
        \end{{align*}}
        So the solution can be expressed in either of the following ways:
        \begin{{align*}}
        &{LB2} {compop} x {compop} {UB2} \\
        &\left{openbrak}{LB2}, {UB2}\right{closebrak}
        \end{{align*}}
        '''.format(
            LB=latex(-c), compop=self.compop, LHS=latex(self.LHS), UB=latex(c),
            LB1=latex(-c-b), LHS1=latex(self.LHS - b), UB1=latex(c-b),
            LB2=latex((-c-b)/a), UB2=latex((c-b)/a), openbrak=openbrak,
            closebrak=closebrak
        )

        return ans

class RevAbsValProb(Problem):
    '''A find-the-absolute-value problem.

    Given an interval, provide the absolute value that characterizes it.
    '''

    printable = True
    secname = 'Reverse Absolute-Value Inequalities'
    
    def __init__(self, full_simplify=False):
        super(RevAbsValProb, self).__init__()
        self.full_simplify = full_simplify
        self.lower, self.upper = sorted([random.randrange(-10, 10),
                                         random.randrange(-10, 10)])
        self.inner = random.choice([True, False])
        self.endp = random.choice([True, False])

    @property
    def statement(self):
        if self.inner:
            comp = r'\leq' if self.endp else '<'
            statement = r''' Find the absolute-value inequality statement that
            corresponds to the following inequality
            \[
            {lower} {comp} x {comp} {upper}
            \]
            '''.format(
                lower=self.lower, comp=comp, upper=self.upper
            )
        else:
            lcomp, gcomp = (r'\leq', r'\geq') if self.endp else ('<', '>')
            statement = r'''Find the absolute-value inequality statement that
            corresponds to the inequalities
            \[
            x {lcomp} {lower} \qquad \text{{or}} \qquad  x {gcomp} {upper}
            \]
            '''.format(
                lcomp=lcomp, lower=self.lower, gcomp=gcomp, upper=self.upper
            )

        return statement

    @property
    def answer(self):
        if self.inner:
            comp = r'\leq' if self.endp else '<'

            LHS, mid, RHS = Poly(self.lower, x), Poly(x, x), Poly(self.upper, x)
            shift = LHS + (RHS - LHS)/2
            inside = mid - shift
            bound = RHS - shift

            if self.full_simplify:
                scale, inside = inside.clear_denoms(convert=True)
                bound = bound.mul_ground(scale)

            ans = r'''$\abs{{{inside}}} {comp} {bound}$'''.format(
                inside=latex(inside), comp=comp, bound=latex(bound)
            )

        else:
            comp = r'\geq' if self.endp else '>'

            low, mid, hi = Poly(self.lower, x), Poly(x, x), Poly(self.upper, x)
            shift = hi - (hi - low)/2
            inside = mid - shift
            bound = hi - shift

            if self.full_simplify:
                scale, inside = inside.clear_denoms(convert=True)
                bound = bound.mul_ground(scale)
            
            ans = r'''$\abs{{{inside}}} {comp} {bound}$'''.format(
                inside=latex(inside), comp=comp, bound=latex(bound)
            )

        return ans

    @property
    def solution(self):
        if self.inner:
            comp = r'\leq' if self.endp else '<'

            LHS, mid, RHS = Poly(self.lower, x), Poly(x, x), Poly(self.upper, x)
            shift = LHS + (RHS - LHS)/2
            inside = mid - shift
            diff = RHS - LHS
            bound = RHS - shift
            soln = r'''
            First look at the endpoints of the interval.  ${RHS}$
            and ${LHS}$ are ${diff}$ units apart, and half of ${diff}$ is
            ${bound}$. So you want to adjust the inequality so that it relates
            $-{bound}$ to ${bound}$, instead of ${LHS}$ to ${RHS}$.  To do
            this, subtract ${shift}$ from every term
            \begin{{align*}}
            &{LHS} {comp} x {comp} {RHS} \\
            &{LHS} - \left({shift}\right) {comp} x - \left({shift}\right)
            {comp} {RHS} - \left({shift}\right) \\
            &-{bound} {comp} {inside} {comp} {bound}.
            \end{{align*}}
            This gives the inequality
            \[
            \abs{{{inside}}} {comp} {bound}.
            \]'''.format(
                RHS=latex(RHS), LHS=latex(LHS), diff=latex(diff),
                bound=latex(bound), shift=latex(shift), comp=comp,
                inside=latex(inside)
            ) 

        else:
            low, mid, hi = Poly(self.lower, x), Poly(x, x), Poly(self.upper, x)
            shift = hi - (hi - low)/2
            inside = mid - shift
            bound = hi - shift
            lcomp, gcomp = (r'\leq', r'\geq') if self.endp else ('<', '>')
            comp = gcomp
            soln = r'''First look at the endpoints.  ${hi}$ and ${low}$ are
                ${diff}$ units apart, and half of ${diff}$ is ${bound}$.  So
                you want to adjust the inequality so that it relates $-{bound}$
                and ${bound}$.  To do this, subtract ${shift}$ from both sides
                of both inequalities:
                \begin{{align*}}
                x {lcomp} {low} \qquad &\text{{or}} \qquad x {gcomp} {hi} \\ 
                x - \left({shift}\right) {lcomp} {low} - \left({shift}\right)
                \qquad &\text{{or}} \qquad 
                x - \left({shift}\right) {gcomp} {hi} - \left({shift}\right)\\
                {inside} {lcomp} -{bound} 
                \qquad &\text{{or}} \qquad 
                {inside} {gcomp} {bound}.
                \end{{align*}}
                This gives the inequality
                \[
                \abs{{{inside}}} {gcomp} {bound}.
                \]
                '''.format(
                    hi=latex(hi), low=latex(low), diff=latex(hi-low),
                    bound=latex(bound), shift=latex(shift),
                    lcomp=lcomp,gcomp=gcomp, inside=latex(inside)
                )
            
        if self.full_simplify:
            scale, inside = inside.clear_denoms(convert=True)
            if scale != 1:
                bound = bound * scale
                simplify = r'''This can be simplified by multiplying
                through by the denominator of the right-hand side
                \[
                \abs{{{inside}}} {comp} {bound}.
                \]
                '''.format(
                    inside=latex(inside), comp=comp, bound=latex(bound))
                soln = ''.join([soln, simplify])

        return soln

def main():
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read('geckomath.ini')
    print config.get('LaTeX', 'preamble')

    print r'\begin{enumerate}'

    full_simplify = config.getboolean('RevAbsValProb', 'full_simplify')
    for i in xrange(10):
        prob = RevAbsValProb(full_simplify=full_simplify)
        print r'\item', prob.statement
        if config.getboolean('RevAbsValProb', 'solutions'):
            print prob.solution
        else:
            print prob.answer

    print r'\end{enumerate}'

    print config.get('LaTeX', 'postamble')

if __name__ == '__main__':
    main()
