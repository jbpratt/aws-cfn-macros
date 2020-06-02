import json


PREFIX = "SFDSSDK::"


def handle_template(request_id, template):
    for name, resource in template.get("Resources", {}).items():
        if resource["Type"].startswith(PREFIX):
            print(resource)
            code = resource.get("Properties", {}).get("Code")
            print(exec(code))


def handler(event, context):
    fragment = event["fragment"]
    status = "success"

    try:
        fragment = handle_template(event["requestId"], event["fragment"])
    except Exception as e:
        raise e

    return {
        "requestId": event["requestId"],
        "status": status,
        "fragment": fragment,
    }
