PROBTYPES = list()

class RegisteringClass(type):
    def __init__(cls, name, bases, dct):
        if cls.printable:
            PROBTYPES.append(cls)
        super(RegisteringClass, cls).__init__(name, bases, dct)


class Problem(object):
    '''A problem parent object.'''

    __metaclass__ = RegisteringClass
    printable = False

    def __init__(self):
        super(Problem, self).__init__()

    @classmethod
    def write_probs(cls, probtex, solntex, nprobs, solutions=False):
        if not nprobs:
            return

        print >>probtex, r'\subsection*{{{secname}}}'.format(
            secname=cls.secname)
        print >>solntex, r'\subsection*{{{secname}}}'.format(
            secname=cls.secname)
        print >>probtex, r'\begin{enumerate}'
        print >>solntex, r'\begin{enumerate}'

        for _ in xrange(nprobs):
            prob = cls()
            print >>probtex, r'\item', prob.statement
            print >>solntex, r'\item', prob.statement
            if solutions:
                print >>solntex, prob.solution
            else:
                print >>solntex, prob.answer

        print >>probtex, r'\end{enumerate}'
        print >>solntex, r'\end{enumerate}'
