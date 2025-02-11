import json
def schedule_retrieve_payload(
                            employee_id,
                            start_date,
                            end_date
                            ):
 
#construct payload for request
  payload = json.dumps({
    "select": [
      "SHIFTS"
    ],
    "where": {
      "employees": {
        "dateRange": {
          "endDate": end_date,
          "startDate": start_date
        },
        "employees": {
          "qualifiers": [
            employee_id
          ]
        }
      },
      "excludeBreaks": True
    }
  })
  return (payload)
    
