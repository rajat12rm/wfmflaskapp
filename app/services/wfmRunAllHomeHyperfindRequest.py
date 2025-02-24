import json
from datetime import datetime
def allhomeHyperfindPayload():
    payload = json.dumps({
    "dateRange": {
        "symbolicPeriod": {
        "qualifier": "Current_Payperiod"
        }
    },
    "hyperfind": {
        "qualifier": "All Home"
    }
    })
    return payload
