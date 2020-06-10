# Custom AWS CloudFormation Macros

- PipLambdaLayer: provision Lambda Layers by providing the Pip package and
  version to download. (Not relevant if using SAM CLI v0.50.0+ https://github.com/awslabs/aws-sam-cli/releases/tag/v0.50.0)
- DataScienceSDK SF: provision workflows with the [StepFunctions Data Science SDK](https://aws-step-functions-data-science-sdk.readthedocs.io/en/latest/index.html) in a CloudFormation template

The macros are provisioned via [SAM](https://github.com/awslabs/serverless-application-model)
```
sam build -t template.cfn.yaml
sam deploy --guided -t template.cfn.yaml
```
