# GitHub Actions on Outerbounds Platform Demo
A basic repo structure to run CI/CD jobs on Outerbounds platform. 

### Create a machine user in Outerbounds UI
- In the Outerbounds UI, go to the `Admin` panel on the left side navigation and select `Users`. 
- Under `Machines` click the `Create New` button.
- Fill out the form, choosing the desired GitHub Actions form, and filling in the desired GitHub organization and repository. 
- After submitting, click the row for the Machine User you created, and a code snippet will appear.
- Paste the command in actions file in `.github/workflows/` and modify it to run Metaflow code in the repository.

### Write flows and run them on desired GitHub Actions
Our goal is to update the model used in the `Predict` workflow defined in `prediction_flow.py`. As a starting point for the CI/CD lifecycle, consider how a data scientist iterates. This repository demonstrates how to take the result of experimental, interactive development and use it to: 
- create a GitHub branch, 
- let an automatic CI/CD process built with GitHub Actions validate the model's quality (using Outerbounds platform resources), and
- if the new model code meets certain user-defined criteria, automatically deploy the newly trained model to be used in the production workflow that makes predictions accessed by other production applications.


### Deploy the `Predict` workflow to production
A data scientist or ML engineer would do this rarely, and typically less frequently than the model selection/architecture in `my_data_science_module.py` updates.
This only needs to be done if the code in `predict_flow.py` file updates.
```
python predict_flow.py --production argo-workflows create
```

#### Manually trigger the production workflow
This is a way to manually trigger a refresh of the production run that populates the model prediction cache accessed by other production applications.
```
python predict_flow.py --production argo-workflows trigger
```

### Local iteration on `EvaluateNewModel`
Local/workstation testing:
```
python evaluate_new_model_flow.py run
```

### CI/CD process using GitHub Actions
When a data scientist is satisfied with what they see on local runs, then they can use GitHub commands like a regular software development workflow:
```
git switch -c 'my-new-model-branch'
git add .
git commit -m 'A model I think is ready for production'
git push --set-upstream origin my-new-model-branch
```

After the model is pushed to the remote branch of `my-new-model-branch`, the data scientist or an engineering colleague can open a pull request against the main branch. When this pull request gets merged to the `main` branch of the repository, a GitHub action defined in `.github/workflows/assess_new_production_model.yml` is triggered. To explore the many complex patterns like this you can implement with GitHub actions, consider step 5 of the [Create and Configure your IAM Role](https://docs.google.com/document/d/1If-Nh4EY4cs5wDihWhnDglE-NKqu8Gv0-ZwXcw4cons/edit) section, and the many types of [events you can use to trigger a GitHub Action](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).

The GitHub Action in this template will do the following:
1. Run the `EvaluateNewModel` workflow defined in `evaluate_new_model_flow.py`.
2. If the `EvaluateNewModel` workflow produces a model that meets some user-defined criteria (e.g., beyond some performance metric threshold), then tag the Metaflow run in which the model was trained as a `deployment_candidate`.
3. If the upstream `EvaluateNewModel` run is tagged as a `deployment_candidate` and the model meets any other criteria you add to this template, then the production workflow will use a new version of the model in the `predict.py` flow in an ongoing fashion.