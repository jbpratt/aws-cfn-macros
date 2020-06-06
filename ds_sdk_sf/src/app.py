PREFIX = "AWS::DSSDK::Workflow"


def handle_template(request_id, template):
    for name, resource in template.get("Resources", {}).items():
        if resource["Type"].startswith(PREFIX):
            props = resource["Properties"]
            workflow = {}
            code = props["Code"]
            code = (
                code
                + f'\nglobals()["workflow"] = {props["WorkflowVariableName"]}.definition.to_json()'
            )
            exec(code, workflow)
            resource.update(
                {
                    "Type": "AWS::StepFunctions::StateMachine",
                    "Properties": {
                        "DefinitionString": f'{workflow["workflow"]}',
                        "RoleArn": props["RoleArn"],
                        "StateMachineName": props["StateMachineName"],
                    },
                }
            )

    return template


def handler(event, context):
    fragment = event["fragment"]
    status = "success"

    try:
        fragment = handle_template(event["requestId"], event["fragment"])
    except Exception as e:
        status = "fail"
        raise e

    return {
        "requestId": event["requestId"],
        "status": status,
        "fragment": fragment,
    }
