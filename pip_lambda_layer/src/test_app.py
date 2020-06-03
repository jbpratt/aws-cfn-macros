from .app import handler
from moto import mock_s3
import boto3


initial_template = {
    "accountId": "123451678910",
    "fragment": {
        "Resources": {
            "MyLambdaLayer": {
                "Type": "AWS::Serverless::PythonLayer",
                "Properties": {
                    "CompatibleRuntimes": ["python3.6", "python3.7", "python3.8"],
                    "LayerName": "camelcaselayer",
                    "Packages": [{"name": "camelcase", "version": "0.2"}],
                    "BucketName": "testbucket",
                },
            }
        }
    },
    "transformId": "123451678910::PythonLambdaLayer",
    "requestId": "346b0915-b365-499a-a6ef-022e048301b1",
    "region": "us-east-1",
    "params": {},
    "templateParameterValues": {},
}

result_template = {
    "requestId": "346b0915-b365-499a-a6ef-022e048301b1",
    "status": "success",
    "fragment": {
        "Resources": {
            "MySNSTopic": {
                "Type": "AWS::Lambda::LayerVersion",
                "Properties": {
                    "CompatibleRuntimes": ["python3.6", "python3.7", "python3.8"],
                    "Content": {
                        "S3Bucket": "testbucket",
                        "S3Key": "camelcase-0.2.zip",
                    },
                    "LayerName": "camelcaselayer",
                },
            }
        }
    },
}


@mock_s3
def create_bucket():
    bucketname = initial_template["fragment"]["Resources"]["MyLambdaLayer"][
        "Properties"
    ]["BucketName"]
    boto3.client("s3").create_bucket(Bucket=bucketname)
    yield bucketname


# This test requires pip and access to disk
@mock_s3
def test_handle_template():
    create_bucket()
    assert handler(initial_template, {}) == result_template
