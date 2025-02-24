import json
from datetime import datetime
def retrieveTimeOffPayload():
    payload = json.dumps({
    "where": {
    "hyperfind": {
        "hyperfindRef": {
        "qualifier": "All Home"
        },
        "startDate": str(datetime.now()).split(" ")[0],
        "endDate": '2025-05-12'
    }
    }
    }
    )
    return payload
