import ConfigParser
import logging
import os
import StringIO
import subprocess

from geckomodules import *


def write_to_files(probtex, solntex, config):
    '''Print TeX to files'''
    print >>probtex, config.get('LaTeX', 'preamble')
    print >>solntex, config.get('LaTeX', 'preamble')

    for probtype in Problems.PROBTYPES:

        nprobs = config.getint(probtype.__name__, 'nprobs')
        solutions = config.getboolean(probtype.__name__, 'solutions')
        probtype.write_probs(probtex, solntex, nprobs, solutions)

    print >>probtex, config.get('LaTeX', 'postamble')
    print >>solntex, config.get('LaTeX', 'postamble')


def compile_to_TeX(ptex, stex, prob_path, soln_path):
    '''Compile the given TeX files and clean up'''
    logging.debug("compiling the TeX files")

    latex_call = subprocess.Popen(('pdflatex',),
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE)

    texout, texerr = latex_call.communicate(ptex.getvalue())

    logging.debug('texout: \n %s', texout)
    logging.debug('texerr: \n %s', texerr)
    
    os.rename('texput.pdf', prob_path)


    latex_call = subprocess.Popen(('pdflatex',),
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE)

    texout, texerr = latex_call.communicate(stex.getvalue())

    logging.debug('texout: \n %s', texout)
    logging.debug('texerr: \n %s', texerr)

    os.rename('texput.pdf', soln_path)

    os.remove('texput.aux')
    os.remove('texput.log')


def main(config):
    prob_path = config.get('output', 'problems')
    logging.debug("prob_path: %s" % prob_path)
    soln_path = config.get('output', 'solutions')
    logging.debug("soln_path: %s" % soln_path)

    ptex = StringIO.StringIO()
    stex = StringIO.StringIO()

    write_to_files(ptex, stex, config)

    prob_path = prob_path.rstrip('.tex')
    soln_path = soln_path.rstrip('.tex')

    compile_to_TeX(ptex, stex, prob_path, soln_path)


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('geckomath.ini')

    logging.basicConfig(level=logging.DEBUG)
    main(config)
