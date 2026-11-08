"""Tests for cleaning the JS files."""

import pandas as pd
import pytest

from tennis_career import data

# A few entries from a female player career's JS file
FEMALE_JS = """
var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"],
  ["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", "19700503", "", "FRA", "0", "", "", "", "", "", "", "1997-W-WT-USA-02A-1997-006"],
  ["19970804", "Manhattan Beach", "Hard", "W", "L", "", "", "WC", "Q3", "7-6 4-6 6-3", "3", "Magui Serna", "54", "6", "", "L", "19790301", "167", "ESP", "0", "", "", "", "", "", "", "1997-W-WT-USA-07A-1997-026"]]
"""

# A few entries from a male player career's JS file
MALE_JS = """
var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-M-FU-ESP-10A-2001-002", "", "1", "1"],
  ["20010917", "Seville CH", "Clay", "C", "L", "", "", "WC", "R16", "3-6 6-1 6-3", "3", "Stefano Galvani", "161", "2", "", "R", "24.2902121834", "178", "ITA", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2", "", "", "", "2001-784-024", "", "2", "2"],
  ["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", "6-4 6-4", "3", "Israel Matos Gil", "751", "", "Q", "U", "18.7597535934", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-784-015", "", "1", "1"]]
"""

SERENA_DOB = pd.Timestamp("1981-09-26")
NADAL_DOB = pd.Timestamp("1986-06-03")


def test_format_name():
    assert data._format_name("serena williams") == "SerenaWilliams"
    assert data._format_name("Serena Williams") == "SerenaWilliams"
    assert data._format_name("SerenaWilliams") == "SerenaWilliams"


def test_get_player_info():
    player_js = "var fullname = 'Serena Williams';\nvar dob=19810926;"
    full_name, dob = data._get_player_info(player_js)
    assert full_name == "Serena Williams"
    assert dob == SERENA_DOB


def test_parse_matches():
    assert len(data._parse_matches(FEMALE_JS)) == 3
    assert len(data._parse_matches(MALE_JS)) == 3


def test_female_opponent_age():
    # female files give the opponent's date of birth
    matches = data._parse_matches(FEMALE_JS)
    df = data._clean_matches(matches, SERENA_DOB, "Serena Williams")
    expected = (pd.Timestamp("1995-10-30") - pd.Timestamp("1977-01-19")).days / 365.25
    assert df["opponent_age"].iloc[0] == pytest.approx(expected)


def test_male_opponent_age():
    # male files already give the opponent's age
    matches = data._parse_matches(MALE_JS)
    df = data._clean_matches(matches, NADAL_DOB, "Rafael Nadal")
    assert df["opponent_age"].iloc[0] == pytest.approx(22.264202601)


def test_age_diff():
    matches = data._parse_matches(MALE_JS)
    df = data._clean_matches(matches, NADAL_DOB, "Rafael Nadal")
    nadal_age = (pd.Timestamp("2001-09-10") - NADAL_DOB).days / 365.25
    assert df["age_diff"].iloc[0] == pytest.approx(nadal_age - 22.264202601)


def test_outcome():
    matches = data._parse_matches(MALE_JS)
    df = data._clean_matches(matches, NADAL_DOB, "Rafael Nadal")
    assert list(df["outcome"]) == ["L", "L", "W"]


def test_unknown_player(monkeypatch):
    monkeypatch.setattr(data, "_download_js", lambda file_name: None)
    with pytest.raises(ValueError):
        data.get_career_data("Gaston Sanchez")