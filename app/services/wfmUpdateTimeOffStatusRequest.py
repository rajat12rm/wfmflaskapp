import json
from datetime import datetime
def UpdateTimeOffStatusPayload(statusId,RequestId):
    payload = json.dumps({
    "changeState": {
    "do": {
        "toStatus": {
        "id": statusId
        }
    },
    "where": {
        "timeOffRequestId": RequestId
    }
    }
    })
    return payload
