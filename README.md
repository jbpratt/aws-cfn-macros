# Custom AWS CloudFormation Macros

- PipLambdaLayer: provision Lambda Layers by providing the Pip package and
  version to download.
- DataScienceSDK SF: provision workflows with the [StepFunctions Data Science SDK](https://aws-step-functions-data-science-sdk.readthedocs.io/en/latest/index.html) in a CloudFormation template

The macros are provisioned via [SAM](https://github.com/awslabs/serverless-application-model)
```
sam build -t template.cfn.yaml
sam deploy --guided -t template.cfn.yaml
```
