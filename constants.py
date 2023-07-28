### model training constants
EVALUATE_DEPLOYMENT_CANDIDATES_COMMAND = ["python", "evaluate_deployment_candidates.py"]

# This is the threshold that determines whether a model is a candidate for deployment.
# In practice, you might define this by comparing the result against a baseline model's performance.
PERFORMANCE_THRESHOLDS = {
    'accuracy': 90
}

### prediction constants
UPSTREAM_FLOW_NAME = "EvaluateNewModel"
CICD_NAMESPACE = "user:my-sp-1"
