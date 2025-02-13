import json
def createTimeOffRequestPayload(requestSubtype,startDate,endDate,payCode):
    payload = json.dumps({
    "requestSubType": {
        "name": requestSubtype
    },
    "periods": [
        {
        "payCode": {
            "qualifier": payCode
        },
        "startDate": startDate,
        "endDate": endDate,
        "symbolicAmount": {
            "id": -1,
            "symbolicId": "FULL_DAY",
            "name": "Full"
        }
        }
    ]
    })
    return payload
