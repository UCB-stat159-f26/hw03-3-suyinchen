"""Implementation of functions for career matches of a player."""

import json
import re

import pandas as pd
import requests

DAYS_PER_YEAR = 365.25


def get_career_data(player_name):
    """Get the career matches of a player.
    Input: name of the player.
    Output: data frame with one row per match.
    """
    file_name = _format_name(player_name)
    player_js = _download_js(file_name)
    career_js = _download_js(file_name + "Career")
    if player_js is None or career_js is None:
        raise ValueError(
            f"Could not find player '{player_name}' on tennisabstract.com. "
            "Please check the spelling."
        )
    full_name, player_dob = _get_player_info(player_js)
    matches = _parse_matches(career_js)
    return _clean_matches(matches, player_dob, full_name)


def _format_name(player_name):
    """Change 'serena williams' to 'SerenaWilliams'.
    Input: name of the player.
    Output: name without spaces.
    """
    words = player_name.split()
    return "".join(word[0].upper() + word[1:] for word in words)


def _download_js(file_name):
    """Download a JS file from tennisabstract.
    Input: name of the file without .js.
    Output: text of the file, or None if the file does not exist.
    """
    url = f"https://www.tennisabstract.com/jsmatches/{file_name}.js"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.text


def _get_player_info(player_js):
    """Get player's full name and date of birth.
    Input: text of the player's JS file.
    Output: full name in string and date of birth in Timestamp.
    """
    full_name = re.search(r"var fullname\s*=\s*'(.*?)'", player_js).group(1)
    dob = re.search(r"var dob\s*=\s*(\d{8})", player_js).group(1)
    return full_name, pd.to_datetime(dob, format="%Y%m%d")


def _parse_matches(career_js):
    """Get the list of matches stored in morematchmx.
    Input: text of the player's career JS file.
    Output: list of matches.
    """
    found = re.search(r"var morematchmx = (\[\[.*?\]\])", career_js, re.DOTALL)
    return json.loads(found.group(1))


def _clean_matches(matches, player_dob, player_name):
    """Make a data frame with the player's age, opponent's age
    and their difference.
    Input: list of matches, player's date of birth, player's full name.
    Output: data frame with one row per match. If the opponent's age is
    missing, opponent_age and age_diff are empty.
    """
    df = pd.DataFrame({
        "player": player_name,
        "date": pd.to_datetime([m[0] for m in matches], format="%Y%m%d"),
        "tournament": [m[1] for m in matches],
        "outcome": [m[4] for m in matches],
        "opponent": [m[11] for m in matches],
    })
    df["player_age"] = (df["date"] - player_dob).dt.days / DAYS_PER_YEAR
    df["opponent_age"] = [_opponent_age(m[16], date) for m, date in zip(matches, df["date"])]
    df["age_diff"] = df["player_age"] - df["opponent_age"]
    return df


def _opponent_age(value, match_date):
    """Opponent's age at the match.
    Female files give the opponent's date of birth,
    male files give the opponent's age.
    Input: opponent's date of birth or age, date of the match.
    Output: opponent's age in years, or None if the value is missing.
    """
    if value == "":
        return None
    if len(value) == 8 and "." not in value:
        return (match_date - pd.to_datetime(value, format="%Y%m%d")).days / DAYS_PER_YEAR
    return float(value)
