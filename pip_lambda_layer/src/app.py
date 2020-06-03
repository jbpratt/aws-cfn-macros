from typing import Dict
from typing import Union
from typing import Any
import subprocess
import tempfile
import shutil
import os

import boto3


PREFIX = "AWS::Serverless::PythonLayer"


def handle_template(request_id: str, template: Dict[str, Any]) -> Dict[str, Any]:
    s3_client = boto3.client("s3")
    new_resources = {}

    for name, resource in template.get("Resources", {}).items():
        if resource["Type"] == PREFIX:
            props = resource["Properties"]
            package: Dict[str, str] = props["Package"]
            bucket = props["BucketName"]

            package_str = "".join(f'{package["name"]}=={package["version"]}')

            filename = package_str.strip().replace("==", "-")
            layer_dir = os.path.join(
                package["name"], "python", "lib", "python3.8", "site-packages"
            )
            directory = os.path.join(tmp_dir, layer_dir)
            subprocess.run(["pip", "install", package_str, "-t", directory])

            os.chdir(tmp_dir)
            path = shutil.make_archive(layer_dir, "zip")

            try:
                s3_client.put_object(
                    Body=open(path, "rb"), Bucket=bucket, Key=filename + ".zip"
                )
            except s3_client.exceptions.ClientError as err:
                raise err

            new_resources[name] = {
                "Type": "AWS::Lambda::LayerVersion",
                "Properties": {
                    "CompatibleRuntimes": props["CompatibleRuntimes"],
                    "Content": {"S3Bucket": bucket, "S3Key": filename + ".zip"},
                    "LayerName": props["LayerName"],
                },
            }

    for name, resource in new_resources.items():
        template["Resources"][name] = resource

    return template


def handler(event, context) -> Dict[str, Union[str, int]]:
    fragment = event["fragment"]
    status = "success"
    try:
        fragment = handle_template(event["requestId"], event["fragment"])
    except Exception as e:
        raise e
    return {"requestId": event["requestId"], "status": status, "fragment": fragment}
