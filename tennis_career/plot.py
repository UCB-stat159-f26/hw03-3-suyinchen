"""Implementation of the plot function for career matches of a player."""

import matplotlib.pyplot as plt


def plot_career(career_data):
    """Make a scatter plot of the player's age vs. the age difference.
    Input: data frame from get_career_data().
    Output: the plot. Points are colored by win or loss.
    """
    player_name = career_data["player"].iloc[0]
    wins = career_data[career_data["outcome"] == "W"]
    losses = career_data[career_data["outcome"] == "L"]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.scatter(wins["player_age"], wins["age_diff"],
               color="#5BC0E8", s=12, label="Match won")
    ax.scatter(losses["player_age"], losses["age_diff"],
               color="#7B2D8E", s=12, label="Match lost")
    ax.axhline(0, color="gray", linewidth=1)
    ax.xaxis.tick_top()
    ax.grid(color="lightgray", linewidth=0.5)
    ax.set_xlabel(f"{player_name}'s age")
    ax.set_ylabel("Age difference (player minus opponent)")
    ax.set_title(f"{player_name}'s Professional Matches",
                 fontweight="bold", pad=50)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13),
              ncol=2, frameon=False)
    return ax