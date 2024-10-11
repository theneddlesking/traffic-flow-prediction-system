from sklearn import metrics


class ModelEvaluator:
    """ModelEvaluator class is used to evaluate the performance of the model"""

    def compute_mape(self, y_true: list, y_pred: list) -> float:
        """Mean Absolute Percentage Error

        # Arguments
            y_true: List/ndarray, true data.
            y_pred: List/ndarray, predicted data.
        # Returns
            mape: Double, result data for train.
        """

        y = [x for x in y_true if x > 0]
        y_pred = [y_pred[i] for i in range(len(y_true)) if y_true[i] > 0]

        num = len(y_pred)
        sums = 0

        for i in range(num):
            tmp = abs(y[i] - y_pred[i]) / y[i]
            sums += tmp

        mape = sums * (100 / num)

        return mape

    def evaluate_regressor(self, y_true: list, y_pred: list):
        """Evaluation for regressor

        # Arguments
            y_true: List/ndarray, true data.
            y_pred: List/ndarray, predicted data.
        """

        mape = self.compute_mape(y_true, y_pred)
        vs = metrics.explained_variance_score(y_true, y_pred)
        mae = metrics.mean_absolute_error(y_true, y_pred)
        rmse = metrics.root_mean_squared_error(y_true, y_pred)
        r2 = metrics.r2_score(y_true, y_pred)

        return {
            "explained_variance_score": vs,
            "mape": mape,
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
        }
