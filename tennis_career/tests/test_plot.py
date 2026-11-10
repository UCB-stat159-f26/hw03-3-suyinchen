"""Tests for the plot function."""

import pandas as pd
from tennis_career import plot_career


def test_plot_career():
    df = pd.DataFrame({
        "player": ["Serena Williams"] * 3,
        "outcome": ["W", "L", "W"],
        "player_age": [18.0, 25.0, 30.0],
        "age_diff": [-2.0, 3.0, 8.0],
    })
    ax = plot_career(df)
    assert len(ax.collections[0].get_offsets()) == 2
    assert len(ax.collections[1].get_offsets()) == 1
    assert "Serena Williams" in ax.get_title()