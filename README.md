# The `jutge-problems-toolkit` package
![Logo](logo.png)

This toolkit is a CLI interface that will help you generate all necessary files to prepare problems for Jutge.org.

   * [Requirements](#requirements)
   * [Installation](#installation)
   * [Usage](#usage)
   * [Problem structure](#problem-structure)
   * [Problem files](#problem-files)
      * [Problem statement](#problem-statement)
      * [Problem metadata](#problem-metadata)
      * [Handler](#handler)
      * [Tags](#tags)
      * [Test cases](#test-cases)
      * [Solutions](#solutions)
      * [Scores](#scores)
      * [Awards](#awards)
   * [Credits](#credits)
   * [License](#license)



# Requirements

In order to use the Jutge.org problems toolkit, install first its dependencies: various compilers, Python, YAML for Python,
LaTeX and various packages of LaTeX. If you intend to use other compilers (e.g. Haskell), you must also install them.


## Ubuntu

```bash
sudo apt-get install build-essential ghc python3 python3-yaml texlive-full
```

## Mac

```bash
brew install ...
```

[`brew`](https://brew.sh) is a package manager for Mac.



# Installation

If you are using Python3, just install it with `pip3 install jutge-problems-toolkit`. You can update to the latest version with `pip3 install --upgrade jutge-problems-toolkit`. If you want to uninstall it, just type `pip3 uninstall jutge-problems-toolkit`.

In case you are using Anaconda, install with `python3 -m pip install jutge-problems-toolkit`.



# Usage

`jutge-problems-toolkit` is a command line utility that currently supports following arguments:

- `--executable`: If specified, it will make the executables of the problems.
- `--corrects `: If specified, it will generate the solution files of the problems.
- `--prints`: if specified, it will create the printable files in `.pdf` and `.ps`.
- `--all` : If specified, it will do everything mentioned above.
- `--recursive`: If specified, the toolkit will search recursively for problems.
- `--list`: If specified, it will list all the problems found recursively.
- `--srclst`: If specified, it will list all the problem sources found recursively.
- `--verify`: If specified, it will verify the correctness of a program.
- `--help` or `-h` : if specified, it will show a help message with available arguments.

To run the toolkit, just type `jutge-problems-toolkit` in the command line.



# Problem structure

A problem can be structured in two ways:

### Method 1: test cases are the same for all languages

```
└── problem_folder
	├── handler.yml
	├── problem.ca.tex
	├── problem.ca.yml
	├── problem.en.tex
	├── problem.en.yml
	├── sample.inp
	├── sample.cor
	├── tags.yml
	└── ...
```

### Method 2: different test cases for every language

```
└── problem_folder
	├── ca
	|	├── handler.yml
	|	├── problem.ca.tex
	|	├── problem.ca.yml
	|	├── sample.inp
	|	├── sample.cor
	|	├── solution.cc
	|	└── ...
	├── en
	|	├── handler.yml
	|	├── problem.en.tex
	|	├── problem.en.yml
	|	├── sample.inp
	|	├── sample.cor
	|	├── solution.cc
	|	└── ...
	└── tags.yml
```

Note: the above structures are just an example of the structure that a basic problem can have and therefore should only be considered as a guideline. The purpose of all the files is explained later on this file.



# Problem files

A problem should contain the following files:

- `solution.*`: One or more solutions to the problem in different languages. See [Solutions](#solutions) for more information.
- `handler.yml`: Contains the information of how to handle the problem. See [Handler](#handler) for more information.
- `tags.yml`: Contains all the tags associated to the problem as a YAML list of words. Currently ignored, can be left empty. See [Tags](#tags) for more information.
- `*.inp`: All the input test sets. See [Test cases](#test-cases) for more information.
- `*.cor`: All the correct files. Those are generated automatically by the toolkit.  See [Test cases](#test-cases) for more information.
- `problem.lang.tex`: Statement LaTeX file for language `lang`. See [Problem statement](#problem-statement) for more information.
- `problem.lang.yml`: Contains the problem information in language `lang`. See [Problem metadata](#problem-metadata) for more information.
- `problem.lang.pdf`: Formatted PDF statement for language `lang`. These are generated automatically by the toolkit.
- `problem.lang.ps`: Fomatted PS statement for language `lang`. These are generated automatically by the toolkit.

Additionally, the problem can contain the following optional files:

- `award.png`: Image of the award you will obtain when you get the problem accepted for the first time. See [Awards](#awards) for more information.
- `award.html`: HTML description of the award you will obtain when you get the problem accepted for the first time. See [Awards](#awards) for more information.
- `distiller.yml`:  File used to specify the parameters of the distillation process. See [Distilled test cases](#distilled-test-cases) for more information.
- `scores.yml`: File that describes the scoring of a problem. See [Scoring](#scoring) for more information.
- `test.ops`: File used to specify some limits for the correction of the problem. See [Test options](#test-options) for more information.



## Problem statement

The problem statement is stored using LaTeX in files named `problem.lang.tex`, where `lang` denotes the ISO 639-1 code of the language for which the metadata is given (`ca`,`en`, `es`, ...). Problem statements make use of certain macros defined by Jutge.org (see TDB).

### Structure

The typical structure of a problem statement is the following:

```latex
\Problem{The title of the problem using LaTeX}

\Statement

This section provides the statement of the problem.

\medskip

Different paragraphs should be separated by the \medskip command.

\Input

This section describes the input of the problem.

\Output

This section describes the output of the problem.

\Sample

```

The `\Sample` section will be automatically replaced to contain the sample test cases. Alternatively, one can use the `\SampleOneCol` or the `\SampleTwoCol` macros to better adjust the column formatting of the the
sample test cases. RunPython users should use `\SampleSession` to get their sample test cases properly formatted as interactive Python sessions.

The title inside the `\Problem{}` macro should match the title in the metadata given in the `problem.lang.yml` file, but here it can contain maths or LaTeX macros.


### Figures

Figures can be inserted using the `\FigureL`, `\FigureC` and `\FigureR` macros, which stand for _left_, _center_ and _right_ respectively. These macros have two parameters:

1. The formatting of the figure (as in `\includegraphics[...]`).
2. The filename of the figure, with no extension. The figure should exists in EPS and PNG formats.

For instance, `\FigureR{width=4.5cm}{towerbell}` will place figure `towerbell` to the right with a width of 4.5 cm.


### Quotes

In order to enclose texts between quotes, please use the `\q{...}` (single quotes), `\qq{...}` (double quotes) or `\uq{...}` (no quotes, but same style) macros.


### Code

The `lstlisting` macros may be used in order to include code. Short snippets of code can be written between `@` signs.

By default, C++ style is used. It may be changed using standard `lstlisting` definitions. The `\UseHaskell` and `\UsePython` macros are shortcuts to use Haskell or Python styling.


### Scoring

In case the problem scores submissions if a test case is passed, we can use `\Scoring` followed by a sentence to explain the scoring method (how many points is worth a case, for example).


### Other sectioning macros

There exist a few other macros that may be used in various situations. Their effect should be straightforward:

- `\Precondition`
- `\Observation`
- `\Observations`
- `\Specification`
- `\Interface`
- `\Hint`
- `\Scores`
- `\Tuples`
- `\ObservationElastic`
- `\ObservationElasticII`
- `\ObservationNoMain`
- `\ObservationNoMainPlural`
- `\ObservationNoMainTuples`
- `\ObservationNoMainTuplesPlural`
- `\ObservationNoMainClasses`


### Other macros

The `\CPP` macro prints C++ in a beautiful way. The `\Link{...}` macro provides an hyperlink to another problem (without specified language), e.g., `\Link{P68688}`.



## Problem metadata

Problem metadata is stored using YML syntax in files named `problem.lang.yml`, where `lang` denotes the ISO 639-1 code of the language for which the metadata is given (`en`, `es`, `ca`, ...).

In the case that `lang` denotes the original language of the problem, `problem.lang.yml` should contain the following fields:

- `title`: Title of the problem in the original language.
- `author`: Full name of the problem setter.
- `email`: Email of the problem setter.

If `lang` denotes a translation, `problem.lang.yml` should contain the following fields:

- `translator`: Full name of the problem translator.
- `title`: Title of the problem in the translated language.
- `translator_email`: Email of the problem translator.
- `original_language`: Code for the original language of the problem.

A problem should have one unique original language and may have several translations. All translations should refer to the same original language. The system will find the original author through it.

All the values for the metadata fields should be given as Unicode based plain text.

### Examples

`problem.ca.yml`

```yml
title: Suma de dos enters
author: Jordi Petit
email: jpetit@somewhere.mail.com
```

`problem.en.yml`

```yml
title: Sum of two integer numbers
translator: Carlos Molina
translator_email: cmolina@somewhere.mail.com
original_language: ca
```



## Handler

The file `handler.yml` contains the information of how to handle the problem using YML syntax. These options will tell the toolkit how to compile the problem. The handler must have two options:

- `handler`: `std` (default option) and `graphic` (used by some Python3 problems).
- `source_modifier`: `none` (default option), `structs` (C++ problems that use structs), `no_main` (problems where only a function is requested, in that case you will need to use the optional option `func_name`).

However, there are also optional arguments that may be used:

- `func_name`: Name of the function requested in case the problem only asks for a function (this must be used along with `source_modifier: no_main`)

By default, the content of `handler.yml`should be like this:

````
handler: std
source_modifier: none
````



## Tags

A list of problem tags are stored using YML syntax in the file `tags.yml`. Each tag is a short string that specifies a particular aspect of the problem, such as `backtracking` or `interval tree`. Unfortunately, there is no comprehensive list of problem tags, but you can get a feeling of it at [https://jutge.org/instructor/tags/list]. Problem tags are only visible by instructor users.

### Examples

`tags.yml`

```yml
- backtracking
- recursion
- event upc contest
- year 2017
```



## Test cases

Each `test` case is described through two files: `test.inp` and `test.cor`.

`test.inp` contains the input of the test case and `test.cor` contains the correct output of the case. In addition, `test` can also make use of a `test.ops` file to describe some options for its correction.

Test case names should be made of letters, digits, dashes and underscores. Do not use special characters in them. Test cases whose name starts with `sample`, `public`, `hint` or `distilled` have an special meaning and will be explained later on. In the case several of these must be present, they often get names such as `sample-1`, `sample-2`, or `sample-short`.

At correction time, public test cases are corrected before the private ones. The cases are processed sequentially, ordered by their name.

As correcting each single test case causes some overhead, it is not advisable to have many different test cases. 20 different test cases may be a reasonable limit.

Input and output test cases should follow these rules:

- They only contain common characters: digits, uppercase and lowercase letters, punctuation ... (specifically those with ASCII codes between 32 and 126, plus the newline). So, no accents such as `À` or `ü`, no characters such as `ç`, `Δ`, `市` or `😊`, and no tabs.

- All lines should end with a newline character (`\n`), including the last line.

In addition, these rules should be taken into account in the output files:

- There must be no spaces before a line break. In particular, there must be no lines with only one or more spaces before the line break.



### Sample test cases

Sample test cases start with `sample` and will be shown to users in the problem statement and provided in the problem zip file. As such, they should make clear the format of the input and the output for the problem and should be reasonably short.

#### Public test cases

Public test cases start with `public` and will be provided in the problem zip file. Usage of public test cases should be rare, but can be useful in situations where long input/output samples must be delivered.


#### Hint test cases

Hint test cases start with `hint` and will be revealed to users if the submission is not accepted (unless some sample test case also fails).



### Distilled test cases

Distilled test cases start with `distilled` and will be shown to users whose submission fails on them (unless some sample or hint test case also fails). Distilled test cases are created by the system using the [Distiller Algorithm](http://upcommons.upc.edu/handle/2117/28174) and are added automatically to the problem directory, they are not mean to be created or modified by hand.

File `distiller.yml` is used to specify the parameters of the distillation process. `distillation.yml` is used to get some statistics form the distillation process.



### Test options

The `test.ops` file can be used to specify some limits for the correction of the problem. The options should be written as if they were arguments of a program, with a space between each other. The following options are available:

- `--maxcore`: Set the maximum size of a core file.
- `--maxfiles`: set the maximum number of files that can be opened simultaneously.
- `--maxoutput`: Set the maximum size that a file created by the program can have.
- `--maxprocs`: set the maximum number of processes that the program can create.
- `--maxtime`: Set the maximum execution time. If the time is exceeded, the program will not be accepted and the verdict will be "Execution Error" (EE).



## Solutions

Each problem must have, at least, one solution file. Solution files are the reference solutions for the problem statement in various programming languages that will be used to compute the correct outputs for each input test case. Solution files are named `solution.ext`, where `ext` is the standard extension that corresponds to the selected programming language.

For instance, a problem may contain `solution.cc` and `solution.py` in order to provide reference solutions in C++ and Python3.

Independently of the available solutions, users can submit their solutions in any supported programming language. The system will match the programming language of the submission and the programming languages available for the solution and select the most appropriate one.

By default, `problems.py` uses `solution.cc` to generate the correct output test cases. An alternate programming language can be selected using the `solution` field in the `handler.yml` file. Currently, `jutge-problems-toolkit` only uses C++, Java and Python (this should be improved in the future).



## Scores

In order to score submissions according to the correct test cases it passes, `scores.yml` must exist. `scores.yml` describes the scoring of a problem using YML syntax. The scores are given through a list of partial scores. Each partial score contains the following fields:

- `part`: Identifier of the partial score.
- `prefix`: Prefix of the test cases that must be passed in this partial score.
- `points`: Number of points assigned to this partial score.

The total number of points is usually 100, but other (integer) values can be used.
A submission that receives the totality of points is considered accepted.

### Example

Consider a problem that has the following test cases:

- `sample-1`
- `sample-2`
- `easy-A`
- `easy-B`
- `hard-A`
- `hard-B`
- `hard-C`

The following file gives 10 points to submissions passing all sample test cases, 30 points to submissions passing all easy test cases, and 60 points to submissions passing all hard test cases:

`scores.yml`

```yml
-   part: Samples
    prefix: sample
    points: 10
-   part: Easy
    prefix: easy
    points: 30
-   part: Hard
    prefix: hard
    points: 60
```



## Awards

Jutge.org offers awards to users in specific circumstances. Awards are images with a caption and a short description. In the case that a problem contains an image file `award.png` and (optionally) a text file `award.html`, users who get the problem accepted for the first time will receive the award.

The `award.png` image file should be a 200x200 pixels image in PNG format with a transparent background (preferably). Clip art and colorful images are preferred, no offensive images should be used.

The `award.html` file should contain a description of the award using simple HTML code. If `award.html` is missing but `award.png` exists, a default description will be provided by the system.



# Credits

- Jordi Petit https://github.com/jordi-petit 



# License

[Apache License 2.0](https://raw.githubusercontent.com/jutge-org/jutge-python/master/LICENSE.txt)