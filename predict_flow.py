from metaflow import FlowSpec, step, Flow, Parameter, schedule, project, namespace
from constants import UPSTREAM_FLOW_NAME, CICD_NAMESPACE


def fetch_default_run_id():
    """
    Return the run id of the latest successful 's deployment_candidate.
    In practice, you will want far more rigorous conditions. 
    For example, you might want to smoke test the model rather than just assert is not None.
    """
    namespace(CICD_NAMESPACE)
    for run in Flow(UPSTREAM_FLOW_NAME):
        if (
            "deployment_candidate" in run.tags
            and run.successful
            and run.data.model is not None
        ):
            return run.id


@project(name="batch_prediction_cicd_on_obp")
@schedule(daily=True)
class Predict(FlowSpec):
    "A FlowSpec to run predictions on the Outerbounds platform using a model vetted in a CI/CD process."

    data_param = Parameter("data_param", help="Input to the model.", default=0)
    upstream_run_id = Parameter(
        "upstream-run-id",
        help="The run ID of the upstream flow.",
        default=fetch_default_run_id(),
    )

    @step
    def start(self):
        # Valdiate the upstream_run_id returned by fetch_default_run_id is usable.
        if self.upstream_run_id is None:
            raise ValueError(
                "Please provide the run ID of the upstream flow as a parameter in: python predict_flow.py run --upstream-run-id <ID>"
            )
        print("Using upstream run with ID: ", self.upstream_run_id)

        # Import my organization's custom modules.
        from my_data_science_module import MyDataLoader, MyPredictionStore

        # Load some data.
        self.train_data = MyDataLoader().load(input=self.data_param)
        # In this toy example, the "data loader" will add 1 to self.data_param and return the same value (a no op) to keep it simple.
        # In practice this might return a tabular dataframe or a DataLoader object for images or text.

        # Load model from the upstream_run.
        upstream_run = Flow(UPSTREAM_FLOW_NAME)[self.upstream_run_id]
        model = upstream_run.data.model
        # Notice we don't need to store the model as artifact, since we can use self.upstream_run_id to fetch it.

        # Make predictions and cache them in a prediction store accessible to your production apps.
        self.predictions = model.predict(data=self.train_data)

        production_store_handler = MyPredictionStore()
        production_store_handler.cache_new_preds(preds=self.predictions)

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    Predict()
