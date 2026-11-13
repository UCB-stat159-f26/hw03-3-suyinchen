# HW3) R/Python Package

**Author**

Monica Chen

**Date Started**

November 8, 2026

**Description**

The goal for this assignment is to turn the work of HW1 and HW2 into a Python package called `tennis_career`. The package gets the career matches of any player on Tennis Abstract (tennisabstract.com) and makes a plot like the New York Times graphic "Serena Williams's Professional Matches, Age 14 to 40".

It has a single source directory (tennis_career) with an __init__.py file and two implementation files `data.py` and `plot.py`, and tests in `tennis_career/tests`.
In addition to this README.md it includes some basic infrastructure: LICENSE, pyproject.toml and .gitignore files.

The package has two public functions:

* `get_career_data(player_name)` gets the career matches of a player and returns a data frame. If the player cannot be found, it gives an error message.
* `plot_career(career_data)` takes the data frame from `get_career_data()` and makes a scatter plot. The x-axis is the player's age, the y-axis is the player's age minus the opponent's age, and the points are colored by win or loss.

**Installation**

From the GitHub repository:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-3-suyinchen.git
```

This project can currently only be installed from source, via

```bash
pip install .
```

or for a development installation via

```bash
pip install -e .
```

**Tests**

The tests use a few example matches from the instructions, so they do not download anything from the website. You can run the project test suite via

```bash
pytest tennis_career
```

**Important details:**

Inputs

* Two JavaScript files from Tennis Abstract for a given player's name. For example, for Serena Williams:
  * https://www.tennisabstract.com/jsmatches/SerenaWilliams.js gives her full name and date of birth.
  * https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js gives all of her career matches.

Outputs

* A data frame with one row per match. If the opponent's age is missing, `opponent_age` and `age_diff` will be NaN, and the matches will not appear in the plot.
* A scatter plot of the player's age against the age difference with each opponent.

Where to Find Files

* The `tennis_career/` folder is the package.
  * `__init__.py` gives the version number and imports the two public functions.
  * `data.py` includes `get_career_data()` and the private functions for data processing.
  * `plot.py` includes `plot_career()` to do the plotting.
  * The `tests/` folder includes the tests `test_data.py` and `test_plot.py` for testing.
* The `pyproject.toml` includes the information needed to install the package.
* The `LICENSE` file includes the MIT License for the code.
* The `ai_documentation.txt` includes a summary of prompts and outputs from AI tools used during the assignment.

**Reflections**

- The career JS file does not include the player's own date of birth, but Tennis Abstract has a second JS file for each player, which includes the player's full name and date of birth. So the package downloads both files for each player.

- The men's and women's data are structured differently. For female players, the raw data provides the opponent's date of birth, while for male players, it already provides the opponent's age. Because of this, my code checks the format of each value.

- I learned how a Python package is organized, including the difference between public and private functions. One important thing I realized is that the license for my code doesn't cover the data itself, since the data belongs to Tennis Abstract.


**License**

* The code is released under the MIT License. See the `LICENSE` file. Copyright (c) 2026 Monica Chen.
* The match data is not included in this repository and can be downloaded from Tennis Abstract https://www.tennisabstract.com