![Grade Estimate](../../actions/workflows/cc-grade_estimate.yml/badge.svg)
![Header](../../actions/workflows/cc-header.yml/badge.svg)

# Instructions

Each sub-directory has an exercise for you to complete. Each exercise subdirectory is prefixed with the string `part-`. The subdirectory contains a README.md which explains the requirements for the exercise.

Start with `part-1` and move through the problems in numerical order. Only move on to the next part when you have completed the current part you are working on.

Every file that you submit must have a header. Please follow the [guidelines provided for this course](https://docs.google.com/document/d/17WkDlxO92zpb26pYM1NIACPcMWtCOlKO7WCrWC6YxRo/edit?usp=sharing).

Please adhere to the [Google C++ coding style](https://google.github.io/styleguide/cppguide.html).

When writing git log comments, please make them descriptive and meaningful. For example, "Fixed my typo that stopped it from compiling." or "Smashed the bug in my main function." are descriptive. Log comments such as "Done" or "upload" are of poor quality.

Each exercise subdirectory has its own [Makefile](https://en.wikipedia.org/wiki/Makefile) which you may use to build and test your progress. Each Makefile has the following targets:

* all: builds the project
* clean: removes object and dependency files
* spotless: removes everything the clean target removes and all binaries
* format: outputs a [`diff`](https://en.wikipedia.org/wiki/Diff) showing where your formatting differes from the [Google C++ style guide](https://google.github.io/styleguide/cppguide.html)
* lint: output of the [linter](https://en.wikipedia.org/wiki/Lint_(software)) to give you tips on how to improve your code
* header: check to make sure your files have the appropriate header
* unittest: run unit tests to help you verify that the units (such as functions) are meeting the assignment's requirements. This does not grade your assignment.
* test: run tests to help you verify your program is meeting the assignment's requirements. This does not grade your assignment.

To build the program use the `make` command. The Makefile's default target is to build `all`.

# Rubric

Each exercise is worth 15 points. There are 2 parts so there is a total of 30 points possible. Each program must compile before it is graded. _Submissions that do not compile shall be assigned a zero grade._

For each problem:

* Functionality (9 points): Your submission shall be assessed for the appropriate constructs and strategies to address the exercise. A program the passes the instructor's tests completely receives full marks. A program that partially passes the instructors tests receives partial-marks. A program that fails the majority or all the tests receives no marks.

* Format & Readability (6 points): Your submission shall be assessed by checking whether your code passess the style and format check, as well as how well it follows the proper naming conventions, and internal documentation guidelines. Git log messages are an integral part of how readable your project is. _Failure to include a header forfeits all marks._

A detailed rubric is assigned to each lab in Canvas.
