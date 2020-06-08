from typing import Dict
from typing import Union
from typing import Any
import subprocess
import tempfile
import shutil
import os

import boto3


PREFIX = "PythonLayer"


def handle_template(template: Dict[str, Any]) -> Dict[str, Any]:
    s3_client = boto3.client("s3")
    for _name, resource in template.get("Resources", {}).items():
        if resource["Type"] == PREFIX:
            props = resource["Properties"]
            package: Dict[str, str] = props["Package"]
            bucket = props["BucketName"]

            package_str = f'{package["name"]}=={package["version"]}'
            tmp_dir = tempfile.TemporaryDirectory()

            filename = package_str.strip().replace("==", "-")
            layer_dir = os.path.join("python", "lib", "python3.8", "site-packages")
            directory = os.path.join(tmp_dir.name, layer_dir)
            subprocess.run(["pip", "install", package_str, "-t", directory], check=True)

            os.chdir(tmp_dir.name)
            path = shutil.make_archive(layer_dir, "zip")

            try:
                s3_client.put_object(
                    Body=open(path, "rb"), Bucket=bucket, Key=filename + ".zip"
                )
            except s3_client.exceptions.ClientError as err:
                raise err

            resource.update(
                {
                    "Type": "AWS::Lambda::LayerVersion",
                    "Properties": {
                        "CompatibleRuntimes": props["CompatibleRuntimes"],
                        "Content": {"S3Bucket": bucket, "S3Key": filename + ".zip"},
                        "LayerName": props["LayerName"],
                    },
                }
            )

    return template


def handler(event, _context) -> Dict[str, Union[str, int]]:
    os.chdir("/tmp")

    fragment = event["fragment"]
    status = "success"
    try:
        fragment = handle_template(event["fragment"])
    except Exception as error:
        status = "failed"
        message = str(error)
    return {
        "requestId": event["requestId"],
        "status": status,
        "fragment": fragment,
        "message": message,
    }
