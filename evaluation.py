import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visualise_evaluations(model_name: str):
    """Create visualisations of the evaluations."""
    csv = f"./results/evaluations/{model_name}_results.csv"

    df = pd.DataFrame(pd.read_csv(csv))

    sns.set(style="whitegrid")

    # scatter plot of expected_output vs. output
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="expected_output", y="output", data=df)
    plt.title("Expected Output vs. Actual Output")
    plt.xlabel("Expected Output")
    plt.ylabel("Actual Output")
    plt.savefig(f"./results/visualisations/{model_name}_expected_vs_actual_output.png")

    # box plot of differences
    plt.figure(figsize=(8, 6))
    sns.boxplot(y="diff", data=df)
    plt.title("Distribution of Differences (diff) between Expected and Actual Outputs")
    plt.ylabel("Difference (diff)")
    plt.savefig(f"./results/visualisations/{model_name}_diff_distribution.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualise the evaluations.")

    parser.add_argument(
        "model_name",
        type=str,
        help="The name of the model to visualise the evaluations for.",
    )

    args = parser.parse_args()

    model_name = args.model_name

    visualise_evaluations(model_name)
