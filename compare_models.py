import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visualise_evaluations(models: list):
    """Create visualisations of the evaluations for multiple models in a single image."""

    sns.set_theme(style="whitegrid")

    # scatter plot of expected_output vs output for all models in one figure
    plt.figure(figsize=(10, 8))
    for model_name in models:
        csv = f"./results/evaluations/{model_name}_results.csv"
        df = pd.read_csv(csv)
        sns.scatterplot(x="expected_output", y="output", data=df, label=model_name)

    plt.title("Expected Output vs. Actual Output Comparison (All Models)")
    plt.xlabel("Expected Output")
    plt.ylabel("Actual Output")
    plt.legend(title="Models")
    plt.savefig("./results/visualisations/comparison_expected_vs_actual_output.png")
    plt.show()

    # compare accuracy of all models in one figure
    model_accuracy = {}

    for model_name in models:
        csv = f"./results/evaluations/{model_name}_results.csv"
        df = pd.read_csv(csv)
        model_accuracy[model_name] = df["accuracy"].mean()

    plt.figure(figsize=(10, 8))
    sns.barplot(x=list(model_accuracy.keys()), y=list(model_accuracy.values()))
    plt.title("Model Accuracy Comparison")
    plt.ylabel("Accuracy")
    plt.savefig("./results/visualisations/comparison_model_accuracy.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualise the evaluations for multiple models."
    )

    parser.add_argument(
        "model_names",
        nargs="+",
        type=str,
        help="The names of the models to visualise the evaluations for.",
    )

    args = parser.parse_args()

    # List of model names
    model_names = args.model_names

    visualise_evaluations(model_names)
