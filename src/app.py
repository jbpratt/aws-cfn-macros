from typing import Dict
import json


def handler(event, _context) -> Dict[str, str]:
    print(json.dumps(event))

    return {"requestId": event["requestId"], "status": "success"}
