import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visualise_evaluations(test_names: list):
    """Create visualisations of the evaluations for multiple models in a single image."""

    sns.set_theme(style="whitegrid")

    # scatter plot of expected_output vs output with a line of best fit for all models in one figure
    plt.figure(figsize=(10, 8))
    for model_name in test_names:
        csv = f"./results/evaluations/{model_name}_results.csv"
        df = pd.read_csv(csv)
        sns.scatterplot(x="expected_output", y="output", data=df, label=model_name)
        sns.regplot(x="expected_output", y="output", data=df, scatter=False, ci=None)

    plt.title("Expected Output vs. Actual Output Comparison (All Models)")
    plt.xlabel("Expected Output (hours)")
    plt.ylabel("Actual Output (hours)")
    plt.legend(title="Models")
    plt.savefig("./results/visualisations/comparison_expected_vs_actual_output.png")
    plt.show()

    # overall accuracy comparison
    model_accuracy = {}
    for model_name in test_names:
        csv = f"./results/evaluations/{model_name}_results.csv"
        df = pd.read_csv(csv)
        model_accuracy[model_name] = df["accuracy"].mean()

    plt.figure(figsize=(10, 8))
    sns.barplot(x=list(model_accuracy.keys()), y=list(model_accuracy.values()))
    plt.title("Model Accuracy Comparison (Overall)")
    plt.ylabel("Accuracy (%)")
    plt.savefig("./results/visualisations/comparison_model_accuracy.png")
    plt.show()

    # accuracy comparison across different times
    time_intervals = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]
    plt.figure(figsize=(12, 8))

    for model_name in test_names:
        csv = f"./results/evaluations/{model_name}_results.csv"
        df = pd.read_csv(csv)

        # Filter and calculate accuracy for each time interval
        accuracies = []
        for time in time_intervals:
            time_data = df[df["expected_output"] <= time]
            accuracies.append(time_data["accuracy"].mean())

        # Plot each model's accuracy over time intervals
        plt.plot(time_intervals, accuracies, marker="o", label=model_name)

    plt.title(f"Model Accuracy For Different Route Lengths ({model_name})")
    plt.xlabel("Length of Time of Route (hours)")
    plt.ylabel("Accuracy (%)")
    plt.legend(title="Models")
    plt.savefig("./results/visualisations/comparison_accuracy_over_time.png")
    plt.show()


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

    # list of model names
    model_names = args.model_names

    # alpha and betas
    alphas = [0.6, 0.7, 0.8]
    betas = [0.1, 0.3, 0.4]

    # best is alpha=0.6, beta=0.3

    test_names = []

    for model_name in model_names:
        for alpha in alphas:
            for beta in betas:
                test_name = f"{model_name}_a{alpha}_b{beta}"
                test_names.append(test_name)

    visualise_evaluations(test_names)
