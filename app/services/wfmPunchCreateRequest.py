import json
def punch_create_payload(
                          employee_id,
                          date_time,
                          id
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
				"id": id
			  }
      }
    ]
  })

  return payload
