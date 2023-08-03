from metaflow import FlowSpec, step, Parameter, current, Flow, catch, retry
from constants import (
    PERFORMANCE_THRESHOLDS,
    EVALUATE_DEPLOYMENT_CANDIDATES_COMMAND,
)


class EvaluateNewModel(FlowSpec):

    """
    A workflow to train a model and evaluate its performance.
    A data scientist may wish to run this locally after making edits to my_data_science_module.py.
    This will run in the CI/CD process via GitHub Actions on the Outerbounds platform.
    """

    data_param = Parameter("data_input", help="Input to the model.", default=0)

    @catch(var="model_evaluation_error")
    @retry(times=3)
    @step
    def start(self):
        "Train and evaluate a model defined in my_data_science_module.py."
        
        # Import my organization's custom .
        from my_data_science_module import MyDataLoader, MyModel

        # Load some data.
        self.train_data = MyDataLoader().load(input=self.data_param)
        # In this toy example, the "data loader" will return the the same value (a no op).
        # In practice this may return a tabular dataframe or a DataLoader object for images or text.

        # Simulate scores measured on your model's performance.
        self.model = MyModel() # When this flow passes your CI/CD criteria, this artifacin production to produce predictions.
        self.eval_metrics = self.model.score(data=self.train_data)
        # In this toy example, the "model evaluation" will just add 1 to the "self.train_data" integer.

        self.next(self.end)

    @step
    def end(self):
        # A simple example of how to use Metaflow's tags to mark a run as a candidate for deployment.
        # In practice, you might want to add additional conditions to identify the model suitability for production.
        # For example, you may want to run a test suite over the APIs called in upstream steps, such as MyDataLoader().load().
        if self.eval_metrics['accuracy'] >= PERFORMANCE_THRESHOLDS['accuracy']:
            run = Flow(current.flow_name)[current.run_id]
            run.add_tag("deployment_candidate")
        else:
            print(
                f"Run {current.run_id} did not meet production performance threshold."
            )


if __name__ == "__main__":
    EvaluateNewModel()