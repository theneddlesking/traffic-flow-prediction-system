from matplotlib import pyplot as plt
import pandas as pd
import matplotlib as mpl

from model.model_result import ModelResult


class DataVisualiser:
    """Class to visualise dataframes as plots."""

    @staticmethod
    def plot_results(
        results: list[ModelResult],
        y_true: list,
        minutes_per_period: int = 15,
    ):
        """Plot the true data and predicted data.

        # Arguments
        y_true: List/ndarray, true data.
        y_pred: List/ndarray, predicted data.
        names: List, Method names.
        location: String, Location name.
        """

        number_of_periods = 24 * 60 // minutes_per_period

        freq = f"{minutes_per_period}min"

        d = "2016-3-4 00:00"
        x = pd.date_range(d, periods=number_of_periods, freq=freq)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(x, y_true, label="True Data")
        for result in results:
            y_pred = result.y_preds
            name = result.model.name
            ax.plot(x, y_pred, label=name)

        plt.legend()
        plt.grid(True)
        plt.xlabel("Time of Day")
        plt.ylabel("Flow")

        date_format = mpl.dates.DateFormatter("%H:%M")
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

    @staticmethod
    def save_plot(path: str):
        """Save the plot to disk."""
        plt.savefig(path)

    @staticmethod
    def show_plot():
        """Show the plot."""
        plt.show()
