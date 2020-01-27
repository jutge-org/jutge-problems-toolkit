#!/usr/bin/python


# ----------------------------------------------------------------------------
# Importations
# ----------------------------------------------------------------------------

import glob
import sys
import os
import os.path
import argparse
import subprocess
import re
import subprocess
from shutil import which

from . import util
from . import compilers

# ----------------------------------------------------------------------------
# Global variables
# ----------------------------------------------------------------------------

home = os.path.normpath(os.path.dirname(sys.argv[0]) + "/..")
languages = ["ca", "en", "es", "fr", "de"]

cxx = "g++"
cxxflags = " -std=c++11 -D_JUDGE_ -O2 -DNDEBUG -Wall -Wextra -Wno-sign-compare -Wshadow "
cxxflags_fallback = " -D_JUDGE_ -O2 -DNDEBUG "

cc = "gcc"
ccflags = " -D_JUDGE_ -O2 -DNDEBUG -Wall -Wextra -Wno-sign-compare "
ccflags_fallback = ""

errors = []


# ----------------------------------------------------------------------------
# Check for missing dependencies
# ----------------------------------------------------------------------------

def check_dependencies():
    check_list = ['g++', 'gcc', 'tex']
    missing_list = []

    for program in check_list:
        if which(program) is None:
            missing_list.append(program)

    if missing_list:
        print('The following dependencies are missing, please install them and try again: ', end='')
        for missing_dep in missing_list:
            if missing_dep == missing_list[-1]: print(missing_dep)
            else: print(missing_dep, end=', ')
        exit()


# ----------------------------------------------------------------------------
# Make executable file
# ----------------------------------------------------------------------------

def make_executable():
    """Compiles the solution in the cwd."""

    if not util.file_exists("handler.yml"):
        raise Exception("handler.yml does not exist")
    handler = util.read_yml("handler.yml")

    global com
    if 'compilers' in handler:
        com = compilers.compiler(handler.get('compilers', ''), handler, 'solution')
    elif 'solution' in handler:
        if handler.get('solution', '') == 'Java':
            sol = 'JDK'
        elif handler.get('solution', '') == 'C':
            sol = 'GCC'
        elif handler.get('solution', '') == 'C++':
            sol = 'GXX'
        else:
            sol = handler.get('solution', '')
        com = compilers.compiler(sol, handler, 'solution')
    else:   #if handler.get('solution', '') == 'C++' or not specified
        com = compilers.compiler('GXX', handler, 'solution')

    com.compile()
    return com

# ----------------------------------------------------------------------------
# Make correct files
# ----------------------------------------------------------------------------

def make_corrects():
    """Makes all correct files in the cwd."""
    print("Generating correct files...")

    com = make_executable()

    handler = util.read_yml("handler.yml")

    if not util.file_exists(com.executable()):
        raise Exception(com.executable() + " does not exist")
    for f in glob.glob("*.cor"):
        util.del_file(f)
    inps = sorted(glob.glob("*.inp"))
    for inp in inps:
        tst = os.path.splitext(inp)[0]
        com.execute(tst, True)

# ----------------------------------------------------------------------------
# Verify program
# ----------------------------------------------------------------------------

def verify_program(program):
    """Verify that program compiles and gets AC for each test."""

    if not util.file_exists("handler.yml"):
        raise Exception("handler.yml does not exist")
    handler = util.read_yml("handler.yml")
    if handler["handler"] != "std":
        raise Exception("unknown handler")

    # compile
    available_list = []
    supported_list = compilers.compiler_extensions(handler.get('compilers'))
    solution_list = sorted(glob.glob(program + ".*[!exe,dir]"))

    print("Compiling supported programs...")
    for solution in solution_list:
        name = os.path.splitext(solution)[0]
        ext = os.path.splitext(solution)[-1][1:]
        if ext in supported_list:
                com = compilers.compiler(supported_list[ext], handler, name)
                com.compile()
                available_list.append([solution, com])

    print()
    unsupported_list = [x for x in solution_list if x not in [y[0] for y in available_list]]
    if unsupported_list != []:
        print("NOTICE: The following solutions are still not supported and will NOT be verified: ", end='')
        for elem in unsupported_list:
            if elem != unsupported_list[-1]: print(elem, end=', ')
            else: print(elem + '\n')

    for f in glob.glob("*.out"):
        util.del_file(f)
    # execute on tests
    has_failed = False
    tests = sorted(glob.glob("*.inp"))
    for solution, compiler in available_list:
        print("Verifying " + solution + "...")
        ext = os.path.splitext(solution)[-1]
        for test in tests:
            tst = os.path.splitext(test)[0]
            compiler.execute(tst, False)

            r = subprocess.call(["cmp", tst + ext + ".out", tst + ".cor"])
            if r:
                has_failed = True
                msg = "WA"
            else:
                msg = "OK"
                util.del_file(tst + ext + ".out")
            print("%s.inp:\t\t%s" % (tst, msg))
        print()

    if has_failed:
        print("Some solutions are not correct! Please check them and try again.")
        sys.exit(0)



# ----------------------------------------------------------------------------
# Make printable files (ps & pdf)
# ----------------------------------------------------------------------------

def make_prints_3(lang, ori):

    ori = os.path.realpath(ori)
    dat = util.current_time()
    usr = util.get_username()
    hst = util.get_hostname()
    src = "%s@%s:%s" % (usr, hst, ori)

    sample2 = ""
    sample1 = ""
    tsts = sorted(glob.glob("*sample*.inp"))

    handler = util.read_yml("handler.yml")

    graphic = ""
    i = 0
    for j in tsts:
        i += 1
        jj = os.path.splitext(j)[0]
        if len(tsts) == 1:
            num = ""
        else:
            num = str(i)

        if handler["handler"] == "graphic":
            size = subprocess.getoutput("identify -format '(%%w$\\\\times$%%h)' %s.cor" % jj)
            graphic = "[%s]" % size
            os.system("convert %s.cor %s.cor.eps" % (jj, jj))

        sample2 += r"\SampleTwoColInputOutput%s{%s}{%s}" % (graphic, jj, num)
        sample1 += r"\SampleOneColInputOutput%s{%s}{%s}" % (graphic, jj, num)

    scores = ""
    if util.file_exists("scores.yml"):
        scores = "scores.yml: \\verbatimtabinput{scores.yml}"

    t = r"""
\documentclass[11pt]{article}

    \usepackage{jutge}
    \usepackage{lang.%s}
    \lstMakeShortInline@

\begin{document}
    \newcommand{\SampleTwoCol}{%s}
    \newcommand{\SampleOneCol}{%s}
    \DoProblem{%s}

\subsection*{Metadata}
\begin{verbatim}
language: %s
source: %s
generation-time: %s\end{verbatim}
problem.%s.yml: \verbatimtabinput{problem.%s.yml}
handler.yml: \verbatimtabinput{handler.yml}
%s
\end{document}
    """ % (lang, sample2, sample1, lang, lang, src, dat, lang, lang, scores)

    util.write_file("main.tex", t)

    print("Generating .ps and .pdf files...")
    r = os.system("latex -interaction scrollmode main > main.err")
    if r != 0:
        os.system('cat main.err')
        raise Exception("LaTeX error, please make sure that LaTeX is installed on your computer.")

    r = os.system("dvips main -o 1> /dev/null 2>/dev/null")
    if r != 0:
        raise Exception("dvips error")

    r = os.system("ps2pdf main.ps main.pdf 1> /dev/null 2>/dev/null")
    if r != 0:
        raise Exception("ps2pdf error")

    os.system("mv main.ps  %s/problem.%s.ps " % (ori, lang))
    os.system("mv main.pdf %s/problem.%s.pdf" % (ori, lang))


def make_prints2(lang):
    """Makes the problem*pdf and problem*ps file in the cwd for language lang."""

    ori = os.getcwd()
    tmp = util.tmp_dir()
    print(ori, lang, tmp)

    os.system("cp * %s/sty/* %s" % (os.path.dirname(os.path.abspath(__file__)), tmp))
    os.chdir(tmp)

    try:
        make_prints_3(lang, ori)
    except:
        raise
    finally:
        os.chdir(ori)


def make_prints():
    """Makes the pdf and ps files for the problem in the cwd"""

    pbms = sorted(glob.glob("problem.*.tex"))
    if pbms:
        for pbm in pbms:
            lang = pbm.replace("problem.", "").replace(".tex", "")
            make_prints2(lang)
    else:
        dirs = sorted(glob.glob("*"))
        for d in dirs:
            if os.path.isdir(d) and d in languages:
                os.chdir(d)
                make_prints2(d)
                os.chdir("..")
            else:
                print("skipping " + d)


# ----------------------------------------------------------------------------
# Make everything in a problem directory
# ----------------------------------------------------------------------------

def make_all():
    """Makes exe, cors, ps and pdf files for the problem in the cwd."""

    pbms = sorted(glob.glob("problem.*.tex"))
    if pbms:
        make_corrects()
        print()
        for pbm in pbms:
            lang = pbm.replace("problem.", "").replace(".tex", "")
            verify_program("solution")
            print()
            make_prints2(lang)
            print('----------------------------------------\n')
    else:
        dirs = sorted(glob.glob("*"))
        for d in dirs:
            if os.path.isdir(d) and d in languages:
                os.chdir(d)
                print("Working on " + os.getcwd() + "...")
                print()
                make_corrects()
                print()
                verify_program("solution")
                print()
                make_prints2(d)
                os.chdir("..")
                print('----------------------------------------\n')
            else:
                print("skipping " + d)


# ----------------------------------------------------------------------------
# Make everything recursively
# ----------------------------------------------------------------------------

def make_recursive_2():
    sys.stdout.flush()

    if util.file_exists("handler.yml"):
        print("------------------------------------------")
        print(os.getcwd())
        print("------------------------------------------")
        if util.file_exists("solution.cc") or util.file_exists("solution.hs"):
            try:
                if 1:
                    make_executable()
                    make_corrects()
                    make_prints()
            except Exception as e:
                print("\a")
                print(e)
                errors.append((e, os.getcwd()))

    else:
        cwd = os.getcwd()
        for path in sorted(glob.glob("*")):
            if os.path.isdir(path):
                os.chdir(path)
                make_recursive_2()
                os.chdir(cwd)


def make_recursive(paths):
    global errors
    errors = []
    cwd = os.getcwd()
    for path in sorted(paths):
        if os.path.isdir(path):
            os.chdir(path)
            make_recursive_2()
            os.chdir(cwd)
    if errors:
        print("------------------------------------------")
        print("Errors:")
        print("------------------------------------------")
        for e in errors:
            print(e)


# ----------------------------------------------------------------------------
# Make a list of problems recursively
# ----------------------------------------------------------------------------

def make_list_2():

    cwd = os.getcwd()
    ext = os.path.splitext(cwd)[1]
    if ext == ".pbm":
        pbms = glob.glob("problem.*.tex")
        if pbms:
            langs = []
            for p in pbms:
                langs.append(p.replace("problem.", "").replace(".tex", ""))
        else:
            langs = util.intersection(glob.glob("*"), languages)
        print(cwd + " " + " ".join(sorted(langs)))

    else:
        for path in sorted(glob.glob("*")):
            if os.path.isdir(path):
                os.chdir(path)
                make_list_2()
                os.chdir(cwd)


def make_list(paths):
    cwd = os.getcwd()
    for path in sorted(paths):
        if os.path.isdir(path):
            os.chdir(path)
            make_list_2()
            os.chdir(cwd)


# ----------------------------------------------------------------------------
# Make a sources list of problems recursively
# ----------------------------------------------------------------------------

ctr = 0

def make_srclst_2():
    global ctr

    cwd = os.getcwd()
    ext = os.path.splitext(cwd)[1]
    if ext == ".pbm":
        ctr += 1
        pbms = glob.glob("problem.*.tex")
        if pbms:
            langs = []
            for p in pbms:
                langs.append(p.replace("problem.", "").replace(".tex", ""))
        else:
            langs = util.intersection(glob.glob("*"), languages)
        for l in langs:
            print("P%04d_%s" % (ctr, l), cwd, l)
    else:
        for path in sorted(glob.glob("*")):
            if os.path.isdir(path):
                os.chdir(path)
                make_srclst_2()
                os.chdir(cwd)


def make_srclst(paths):
    cwd = os.getcwd()
    for path in sorted(paths):
        if os.path.isdir(path):
            os.chdir(path)
            make_srclst_2()
            os.chdir(cwd)


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    check_dependencies()

    # Create and configure the option parser
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options] [paths]",
        description="Make different tasks in problem directories.",
    )

    parser.add_argument("--executable", help="make executable in the cwd",
                        action="store_true")
    parser.add_argument("--corrects", help="make correct files in the cwd",
                        action="store_true")
    parser.add_argument("--prints", help="make printable files in the cwd",
                        action="store_true")
    parser.add_argument("--all", help="make executable, correct and printable files in the cwd (default)",
                        action="store_true")
    parser.add_argument("--recursive", help="make all recursively (cwd if ommitted)",
                        action="store_true")
    parser.add_argument("--list", help="list all recursively (cwd if ommitted)",
                        action="store_true")
    parser.add_argument("--srclst", help="list all recursively for sources (cwd if ommitted)",
                        action="store_true")
    parser.add_argument("--verify", help="verify correctness of a program",
                        action='store', dest="verify", type=str, default=None, nargs='?', metavar="PROGRAM")
    parser.add_argument("--verbose", help="set verbosity level (0-3) NOT YET IMPLEMENTED",
                        type=int, default=3, metavar="NUMBER")
    parser.add_argument("--stop-on-error", help="stop on first error (for --mk-rec) NOT YET IMPLEMENTED",
                        action="store_true", default=False)

    # Parse options with real arguments
    args, paths = parser.parse_known_args()

    # Do the work
    done = False
    if args.executable:
        done = True
        make_executable()
    if args.corrects:
        done = True
        make_corrects()
    if args.prints:
        done = True
        make_prints()
    if args.all:
        done = True
        make_all()
    if args.recursive:
        done = True
        if paths == []:
            paths = (".",)
        make_recursive(paths)
    if args.list:
        done = True
        if paths == []:
            paths = (".",)
        make_list(paths)
    if args.srclst:
        done = True
        if paths == []:
            paths = (".",)
        make_srclst(paths)
    if args.verify:
        done = True
        if args.verify == None: verify_program("solution")
        else: verify_program(args.verify)
    if not done:
        make_all()


if __name__ == "__main__":
    main()
