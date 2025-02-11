import json
def punch_create_payload(
                          employee_id,
                          date_time
                          ):
 
#construct payload for request
  payload = json.dumps({
    "punches": [
      {
        "punchDtm": date_time,
        "employee": {
          "qualifier": employee_id
        },
        "typeOverride": {
				"id": 2
			  }
      }
    ]
  })

  return payload
