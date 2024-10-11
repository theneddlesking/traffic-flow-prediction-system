from matplotlib import pyplot as plt
import pandas as pd
import matplotlib as mpl


class DataVisualiser:
    """Class to visualise dataframes as plots."""

    # TODO refactor this out a better way
    @staticmethod
    def plot_results(y_true: list, y_preds: list, names: list, save_path: str):
        """Plot the true data and predicted data.

        # Arguments
        y_true: List/ndarray, true data.
        y_pred: List/ndarray, predicted data.
        names: List, Method names.
        location: String, Location name.
        """
        d = "2016-3-4 00:00"
        x = pd.date_range(d, periods=96, freq="15min")

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(x, y_true, label="True Data")
        for name, y_pred in zip(names, y_preds):
            ax.plot(x, y_pred, label=name)

        plt.legend()
        plt.grid(True)
        plt.xlabel("Time of Day")
        plt.ylabel("Flow")

        date_format = mpl.dates.DateFormatter("%H:%M")
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

        # save plot
        plt.savefig(save_path)
