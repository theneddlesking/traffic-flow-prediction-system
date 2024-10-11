class TrainingConfig:
    """Training configuration for a model."""

    def __init__(
        self,
        epochs: int,
        batch_size: int,
        train_test_proportion: float = 0.7,
        validation_split: float = 0.05,
    ):
        self.epochs = epochs
        self.batch_size = batch_size
        self.validation_split = validation_split
        self.train_test_proportion = train_test_proportion
