import json
def schedule_create_payload(
                            employee_id,
                            start_date_time,
                            end_date_time
                            ):
 
#construct payload for request
  payload = json.dumps([
    {
      "shifts": {
        "create": [
          {
            "employee": {
              "qualifier": employee_id
            },
            "startDateTime": start_date_time,
            "endDateTime": end_date_time,
            "segments": [
              {
                "startDateTime": start_date_time,
                "endDateTime": end_date_time,
                "segmentTypeRef": {
                  "qualifier": "REGULAR_SEGMENT"
                }
              }
            ]
          }
        ]
      }
    }
  ])
  
  return (payload)
    
