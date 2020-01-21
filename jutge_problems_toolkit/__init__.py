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
    """Compiles the solution in thw cwd."""

    if not util.file_exists("handler.yml"):
        raise Exception("handler.yml does not exist")
    handler = util.read_yml("handler.yml")

    if handler.get('compilers', '') == 'PRO2':
        make_executable_PRO2()
    elif handler.get('compilers', '') == 'MakePRO2':
        make_executable_MakePRO2()
    elif handler.get('compilers', '') == 'RunHaskell':
        make_executable_Haskell()
    elif handler.get('compilers', '') == 'RunPython':
        make_executable_RunPython()
    elif handler.get('solution', '') == 'GHC':
        make_executable_GHC()
    elif handler.get('solution', '') == 'Python3':
        make_executable_Python3()
    elif handler.get('solution', '') == 'R':
        make_executable_R()
    elif handler.get('solution', '') == 'Java':
        make_executable_Java()
    elif handler.get('solution', '') == 'C':
        make_executable_C()
    elif handler.get('solution', '') == 'C++':
        make_executable_CPP()
    else:
        make_executable_CPP()


def make_executable_CPP():

    handler = util.read_yml("handler.yml")

    if handler["handler"] != "std":
        raise Exception("unknown handler")

    if not util.file_exists("solution.cc"):
        raise Exception("solution.cc does not exist")

    util.del_file("solution.exe")
    if util.file_exists("main.cc"):
        if handler["source_modifier"] == "structs":
            util.system("cat solution.cc main.cc > temporal.cc ; %s %s temporal.cc -o solution.exe ; rm temporal.cc" % (cxx, cxxflags))
        else:
            util.system("%s %s solution.cc main.cc -o solution.exe" % (cxx, cxxflags))
    else:
        if util.file_exists("solution.fallback"):
            util.system("%s %s solution.cc -o solution.exe" % (cxx, cxxflags_fallback))
        else:
            util.system("%s %s solution.cc -o solution.exe" % (cxx, cxxflags))
    if not util.file_exists("solution.exe"):
        raise Exception("error in C++ compilation")


def make_executable_C():

    handler = util.read_yml("handler.yml")

    if handler["handler"] != "std":
        raise Exception("unknown handler")

    if not util.file_exists("solution.c"):
        raise Exception("solution.c does not exist")

    util.del_file("solution.exe")
    if util.file_exists("main.c"):
        if handler["source_modifier"] == "structs":
            util.system("cat solution.c main.c > temporal.c ; %s %s temporal.c -o solution.exe -lm ; rm temporal.cc" % (cc, ccflags))
        else:
            util.system("%s %s solution.c main.c -o solution.exe -lm" % (cc, ccflags))
    else:
        if util.file_exists("solution.fallback"):
            util.system("%s %s solution.c -o solution.exe -lm" % (cc, ccflags_fallback))
        else:
            util.system("%s %s solution.c -o solution.exe -lm" % (cc, ccflags))
    if not util.file_exists("solution.exe"):
        raise Exception("error in C compilation")


def make_executable_GHC():

    handler = util.read_yml("handler.yml")

    if handler["handler"] != "std":
        raise Exception("unknown handler")

    if not util.file_exists("solution.hs"):
        raise Exception("solution.hs does not exist")

    util.del_file("solution.exe")
    util.system("ghc solution.hs -o solution.exe")
    if not util.file_exists("solution.exe"):
        raise Exception("error in GHC compilation")


def make_executable_PRO2():
    util.del_file("solution.exe")
    util.del_dir('compilation')
    os.mkdir('compilation')
    if util.file_exists("solution.cc"):
        util.system('cp solution.cc compilation/program.cc')
    elif util.file_exists("solution.hh"):
        util.system('cp solution.hh compilation/program.hh')
    else:
        print("There is no solution.cc nor solution.hh")
    util.system('cp public/* compilation')
    util.system('cp private/* compilation')
    os.chdir('compilation')
    util.system("%s %s *.cc -o ../solution.exe" % (cxx, cxxflags))
    os.chdir('..')
    util.del_dir('compilation')
    if not util.file_exists("solution.exe"):
        raise Exception("solution.exe not created")
    util.system("(cd public && tar cf ../public.tar *)")
    util.system("(cd private && tar cf ../private.tar *)")


def make_executable_MakePRO2():
    if not util.file_exists("solution"):
        raise Exception("There is no solution directory")
    if not util.file_exists("public"):
        raise Exception("There is no public directory")
    if not util.file_exists("private"):
        raise Exception("There is no private directory")

    util.del_file("solution.exe")
    util.del_dir('compilation')
    os.mkdir('compilation')
    util.system('cp solution/*  public/* private/* compilation')
    os.chdir('compilation')
    util.system("make")
    util.system('cp program.exe ../solution.exe')
    os.chdir('..')
    util.del_dir('compilation')
    if not util.file_exists("solution.exe"):
        raise Exception("solution.exe not created")
    util.system("(cd public && tar cf ../public.tar *)")
    util.system("(cd private && tar cf ../private.tar *)")
    util.system("(cd solution && tar cf ../solution.tar *)")


def make_executable_Haskell():
    if not util.file_exists("solution.hs"):
        raise Exception("solution.hs does not exist")

    util.del_file("work")
    util.del_file("work.hi")
    util.del_file("work.o")
    util.copy_file("solution.hs", "work.hs")
    f = open("work.hs", "a")
    print("""main = do print "OK" """, file=f)
    f.close()

    util.system("ghc -O3 work.hs")
    if not util.file_exists("work"):
        raise Exception("error in haskell compilation")
    util.del_file("work")
    util.del_file("work.hi")
    util.del_file("work.o")


def make_executable_RunPython():
    if not util.file_exists("solution.py"):
        raise Exception("solution.py does not exist")


def make_executable_Python3():
    if not util.file_exists("solution.py"):
        raise Exception("solution.py does not exist")


def make_executable_R():
    if not util.file_exists("solution.R"):
        raise Exception("solution.R does not exist")


def make_executable_Java():
    if not util.file_exists("solution.java"):
        raise Exception("solution.java does not exist")
    util.del_file("Main.java")
    util.system("javac solution.java")
    if not util.file_exists("Main.class"):
        raise Exception("error in Java compilation")


# ----------------------------------------------------------------------------
# Make correct files
# ----------------------------------------------------------------------------

def make_corrects():
    """Makes all correct files in the cwd."""

    make_executable()

    handler = util.read_yml("handler.yml")
    if handler.get('compilers', '') == 'RunHaskell':
        make_corrects_RunHaskell()
    elif handler.get('compilers', '') == 'RunPython':
        make_corrects_RunPython()
    elif handler.get('solution', '') == 'Python3':
        make_corrects_Python3()
    elif handler.get('solution', '') == 'R':
        make_corrects_R()
    elif handler.get('solution', '') == 'Java':
        make_corrects_Java()
    else:
        if not util.file_exists("solution.exe"):
            raise Exception("solution.exe does not exist")
        for f in glob.glob("*.cor"):
            util.del_file(f)
        inps = sorted(glob.glob("*.inp"))
        for inp in inps:
            tst = os.path.splitext(inp)[0]
            util.system("./solution.exe < %s.inp > %s.cor" % (tst, tst))



def make_corrects_RunHaskell():
    for f in glob.glob("*.cor"):
        util.del_file(f)
    inps = sorted(glob.glob("*.inp"))
    for inp in inps:
        tst = os.path.splitext(inp)[0]
        util.copy_file("solution.hs", "work.hs")
        if util.file_exists("judge.hs"):
            os.system("cat judge.hs >> work.hs")
        f = open("work.hs", "a")
        print("main = do", file=f)
        for line in open(tst + ".inp").readlines():
            line = line.rstrip()
            if line.startswith("let "):
                print("    %s" % line, file=f)
#            elif line.startswith("deb "):
#                print >>f, '    hPutStrLn stderr "%s"' % line
            else:
                print("    print (%s)" % line, file=f)
        f.close()
        util.system("runhaskell work.hs >%s.cor" % (tst, ))


def make_corrects_RunPython():
    for f in glob.glob("*.cor"):
        util.del_file(f)
    inps = sorted(glob.glob("*.inp"))
    for inp in inps:
        tst = os.path.splitext(inp)[0]
        os.system("cat solution.py %s.inp > work.py" % tst)
        util.system("python3 work.py >%s.cor" % (tst, ))

        # additionally, create doctest-like session
        if tst == 'sample':
            python_doctest(tst)


def make_corrects_Python3():
    handler = util.read_yml("handler.yml")
    for f in glob.glob("*.cor"):
        util.del_file(f)
    inps = sorted(glob.glob("*.inp"))
    for inp in inps:
        tst = os.path.splitext(inp)[0]
        util.system("python3 solution.py <%s.inp >%s.cor" % (tst, tst))
        if handler["handler"] == "graphic":
            os.rename("output.png", "%s.cor" % tst)


def make_corrects_R():
    for f in glob.glob("*.cor"):
        util.del_file(f)
    inps = sorted(glob.glob("*.inp"))
    for inp in inps:
        tst = os.path.splitext(inp)[0]

        if util.file_exists("main.R"):
            util.system("cat solution.R main.R > work.R")
            util.system("Rscript work.R <%s.inp >%s.cor" % (tst, tst))
            util.system("rm work.R")
        else:
            util.system("Rscript solution.R <%s.inp >%s.cor" % (tst, tst))


def make_corrects_Java():
    for f in glob.glob("*.cor"):
        util.del_file(f)
    inps = sorted(glob.glob("*.inp"))
    for inp in inps:
        tst = os.path.splitext(inp)[0]
        util.system("java Main <%s.inp >%s.cor" % (tst, tst))


def python_doctest(tst):
    print("Generate %s.dt" % tst)
    inp = open("%s.inp" % tst).read()
    wrk = "import sys\n%s\nsys.exit()\n" % (inp)
    l = len(wrk.split("\n"))
    util.write_file("work.py", wrk)
    os.system("python3 -c 'import pty, sys; pty.spawn(sys.argv[1:])' python3 -i solution.py <work.py >%s.dt" % tst)
    dt = open("%s.dt" % tst).readlines()
    dt = dt[l:-2]
    f = open("%s.dt" % tst, 'w')
    for x in dt:
        x = x.rstrip()
        if x.startswith('>>> print(repr(') and x.endswith('))'):
            x = ">>> " + x[15:-2]
        elif x.startswith('>>> print(') and x.endswith(')'):
            x = ">>> " + x[10:-1]
        print(x, file=f)
    f.close()


# ----------------------------------------------------------------------------
# Verify program
# ----------------------------------------------------------------------------

def verify_program(program):
    """Verify that program compiles and gets AC for each test."""

    # This implementation is not yet very functional, but works well in basic cases

    if not util.file_exists("handler.yml"):
        raise Exception("handler.yml does not exist")
    handler = util.read_yml("handler.yml")
    if handler["handler"] != "std":
        raise Exception("unknown handler")

    # compile
    supported_list = []
    solution_list = sorted(glob.glob(program + ".*"))
    solution_list.remove(program + ".exe")
    for solution in solution_list:
        ext = solution.split('.')[-1]
        if ext == "cc" or ext == "c":
            supported_list.append(solution)
            if util.file_exists("main." + ext):
                if handler["source_modifier"] == "structs":
                    if ext == "cc": util.system("cat solution.cc main.cc > temp.cc ; %s %s temp.cc -o solution-cc.exe ; rm temp.cc" % (cxx, cxxflags))
                    else: util.system("cat solution.c main.c > temp.c ; %s %s temp.c -o solution-c.exe ; rm temp.c" % (cc, ccflags))
                else:
                    if ext == "cc": util.system("%s %s solution.cc main.cc -o solution-cc.exe" % (cxx, cxxflags))
                    else: util.system("%s %s solution.c main.c -o solution-c.exe" % (cc, ccflags))
            else:
                if util.file_exists("solution.fallback"):
                    if ext == 'cc': util.system("%s %s solution.cc -o solution-cc.exe" % (cxx, cxxflags_fallback))
                    else: util.system("%s %s solution.c -o solution-c.exe" % (cc, ccflags_fallback))
                else:
                    if ext == 'cc': util.system("%s %s %s.cc -o %s-cc.exe" % (cxx, cxxflags, program, program))
                    else: util.system("%s %s %s.c -o %s-c.exe" % (cxx, cxxflags, program, program))

            if not util.file_exists(program + "-" + ext + ".exe"):
                raise Exception(program + "-" + ext + ".exe not created")
        if ext == "py":
            supported_list.append(solution)

    '''print("Supported list:")
    for elem in supported_list:
        print(elem)

    print("Unsupported list:")
    for elem in [x for x in solution_list if x not in supported_list]:
        print(elem)'''

    # execute on tests
    tests = sorted(glob.glob("*.inp"))
    for solution in supported_list:
        print("Verifying " + solution + "...")
        for test in tests:
            ext = solution.split('.')[-1]
            if ext == 'cc' or ext == 'c':
                test = os.path.splitext(test)[0]
                os.system("./%s-%s.exe < %s.inp > %s.out" % (program, ext, test, test))
            if ext == 'py':
                test = os.path.splitext(test)[0]
                os.system("python3 ./%s < %s.inp > %s.out" % (solution, test, test))

            r = subprocess.call(["cmp", test + ".out", test + ".cor"])
            if r:
                msg = "WA"
            else:
                msg = "OK"
            print("%s:\t\t%s" % (test, msg))



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

    print("latex")
    r = os.system("latex -interaction scrollmode main > main.err")
    # r = os.system("latex main")
    if r != 0:
        os.system('cat main.err')
        raise Exception("LaTeX error, please make sure that LaTeX is installed on your computer.")

    print("dvips")
    r = os.system("dvips main -o 1> /dev/null 2>/dev/null")
    if r != 0:
        raise Exception("dvips error")

    print("ps2pdf")
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
    from glob import glob
    print(glob(os.path.dirname(os.path.abspath(__file__) + "/sty/*")))

    os.system("cp * %s/sty/* %s" % (os.path.dirname(os.path.abspath(__file__)), tmp))
    os.chdir(tmp)

    try:
        make_prints_3(lang, ori)
    except:
        raise
    finally:
        os.chdir(ori)
        #util.del_dir(tmp)


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
        for pbm in pbms:
            lang = pbm.replace("problem.", "").replace(".tex", "")
            make_prints2(lang)
    else:
        dirs = sorted(glob.glob("*"))
        for d in dirs:
            if os.path.isdir(d) and d in languages:
                os.chdir(d)
                print(os.getcwd())
                make_corrects()
                make_prints2(d)
                os.chdir("..")
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
        #version="1.0",
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
                      action='store', dest="verify", type=str, metavar="PROGRAM")
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
        verify_program(args.verify)
    if not done:
        make_all()


if __name__ == "__main__":
    main()
