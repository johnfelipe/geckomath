Geckomath  version 0.1.2 (alpha)
===============================

0. Dependencies
---------------

Geckomath depends on a working LaTeX distribution at the moment (and probably
will forever).  For Windows, you just need to visit

    http://miktex.org/2.9/setup

to obtain the most recent release of MiKTeX.  The ONLY requirement is
`pdflatex`, so the most basic distribution is good enough; no need for TeX
editors or anything else.  Geckomath calls `pdflatex` from the command line.

1. Installation
---------------

LaTeX is the only dependency, and otherwise Geckomath is completely stand-alone:
no installation required.  Simply double-click `geckomath.exe` to run.

1. Use
------

Running `geckomath.exe` brings up a GUI configuation editor.  Choose the number
of problems of each type that you'd like, and the depth of solutions, and click
'generate PDFs' to create 2 PDFs: one with problems, and the other with
associate solutions.

2. Development
--------------

To create a new problem type "foo", create a module `foo.py` in `geckomodules`,
and add "foo" to the `__all__` variable in `geckomodules/__init__.py`.  In your
module, create a class that inherits from `Problems.Problem` that has at least
the following:

* a class attribute `secname` for the name of the section
* a boolean class attribute `printable` that marks whether this is a real problem type
* The following object properties:

    * `statement`
    * `answer` (The short answer)
    * `solution` (The full worked solution)

3. Questions?
-------------

john.e.dougherty.ii@gmail.com

