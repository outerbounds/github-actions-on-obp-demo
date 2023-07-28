class MyDataLoader:
    def __init__(self):
        pass

    def load(self, input):
        """
        A toy function that returns an integer.
        This function mimics loading data from your warehouse / lake.
        In this case we return a single number to reduce complexity.
        In practice this might be a dataframe, PyTorch DataLoader, etc.
        """
        my_dataset_or_dataloader = input
        return my_dataset_or_dataloader


class MyModel:
    def __init__(self):
        pass

    def predict(self, data):
        """
        A toy function that returns the input plus one.
        This function mimics a prediction from a model.
        """
        return data + 2 # a very silly "model" 

    def score(self, data):
        """
        A toy function that returns the input plus one.
        This function mimics an evaluation of a model's performance.
        """
        return {'accuracy': 100.}


class MyPredictionStore:
    def __init__(self):
        self.store_url = "https://my-prediction-store.com"

    def cache_new_preds(self, preds=None):
        """
        Logic to push a model's predictions to a cache accessible by other production apps.
        This definition is just a placeholder.
        For a realistic example of doing this using DynamoDB, see: https://outerbounds.com/docs/recsys-tutorial-S2E4/.
        There are many patterns for storing predictions
        """
        assert (
            preds is not None
        ), "Not a valid set of predictions... Not overwriting the current prediction cache."
        # You probably want to insert other logic here, such as ensuring the predictions are properly formed,
        # and the cache contents you are about to replace are versioned/backed up somewhere in case you need to roll back.
        print(f"Pushing predictions to {self.store_url}")
