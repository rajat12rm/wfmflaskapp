import http.client
import json

conn = http.client.HTTPSConnection("partnersand-034.cfn.mykronos.com")
payload = json.dumps({
  "where": {
    "hyperfind": {
      "hyperfindRef": {
        "qualifier": "All Home"
      },
      "startDate": "2025-02-25",
      "endDate": "2025-02-25"
    }
  }
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'iSmXmFoR4raYUmdUMpVDuCdk2dI',
  'Cookie': 'AUTHZ_TOKEN=VVFxb2NaT3dzODZ2cS9GT2dMWXIvREhRQ3ErQnUyVlZhZkN0UFZSMTA1NjYza1ZJV21zNVVpSXNuamxPRUw5cTgwVXBkZVV6ZUM2S3VhVDZCcFhwSkFwaVUraXkrM0gvZDhYZ3VLb3g3ZExHNElac253emFFVExtbFVqRFR2NFdjbUNoTGdUcFhrVFlocGZ6QWM0cjl4Z0NHdldrZVpEbHZNNGhUOFJsK2hzeTF0TU4ybmdYV3lBVzliTzlrd0pOUk9YQSs2dDJKaXRGeTRvUCtBMUpwL0NZdDduRnlmRUg2V1pqZHFzSGVxRnlQTVhETU0wN0RDQmtBQWh1MlA3VDhwb0lxaUt6eWduZi93VG1ObXJyanZ1cnlWRVlWV1o1X3Yy; WFC_INSTANCE=LI1IuiuN8qZPIaKgkfu+SJ23W7Mr7kO4OreJz/y8b4FVdYfDcQKd8MbarObFNAuQBf1sbFNHQ3McC3sZX+5JCchCoxeYzUKdby8zlnovBGA-; WFC_TENANT_ID=86AXmiQ/Bda0y6ZpH0+ZCpNb4km7LCxYt2//eTonfVkBg25H4oyYyuEnDJwyjgitpLpCpqcCDvvR0+FYtJyfSA--; WFC_USER=rqRnmn1fTeliC+C1m6mTQzcILykNdNb5GeK2MxzRpygZVe/OfpbVrkqfaWBK1bJn; JSESSIONID=9364D0F914FDD3E92186BC23BF840222; srv_id=b8ae48bbfe7a00022b1c535aeef7751d'
}
conn.request("POST", "/api/v1/scheduling/timeoff/multi_read", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
data = json.loads(data)
for i in range(0,len(data)):
    print(data[i]['id'],data[i]['creator']['qualifier'],data[i]['createDateTime'].split('T')[0],data[i]['periods'][0]['startDate'],data[i]['periods'][0]['endDate'],data[i]['periods'][0]['payCode']['qualifier'])
    print(data[i]['currentStatus']['name'])