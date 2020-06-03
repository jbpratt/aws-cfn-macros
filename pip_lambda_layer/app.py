from typing import Dict
from typing import List
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
            packages: List[Dict[str, str]] = props["Packages"]
            bucket = props["BucketName"]

            directory = tempfile.TemporaryDirectory().name

            packages_str = "".join([f'{x["name"]}=={x["version"]} ' for x in packages])
            subprocess.run(["pip", "install", packages_str, "-t", directory])
            filename = packages_str.strip().replace("==", "-")
            filename_w_dir = os.path.join(directory, filename)

            shutil.make_archive(filename_w_dir, "zip", directory)

            filename = filename + ".zip"
            try:
                s3_client.put_object(Body=filename_w_dir, Bucket=bucket, Key=filename)
            except s3_client.exceptions.ClientError as err:
                raise err

            new_resources[name] = {
                "Type": "AWS::Lambda::LayerVersion",
                "Properties": {
                    "CompatibleRuntimes": props["CompatibleRuntimes"],
                    "Content": {"S3Bucket": bucket, "S3Key": filename},
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
