# Pip Lambda Layer Macro

Create Lambda Layers from a specified Pip package:version
```yaml
Transform:
  - PythonLambdaLayer
Resources:
  SixLayer:
    Type: "AWS::Serverless::PythonLayer"
    Properties:
      BucketName: ""
      CompatibleRuntimes:
        - python3.6
        - python3.7
        - python3.8
      LayerName: six
      Package:
        name: six
        version: "1.15.0"
```

### Setup
The macro should be deployed to the account so that CloudFormation knows where
to find the transform Lambda.
```
sam build -t template.cfn.yaml
sam deploy -t template.cfn.yaml
```
