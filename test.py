import http.client
import json
import urllib.parse

conn = http.client.HTTPSConnection("partnersand-034.cfn.mykronos.com")
payload = ''
headers = {
  'Content-Type': 'application/json',
  'Authorization': '1qNyWp2bSl9hY_G0o60t_n6Or8g'
}
subtype = 'Time Off'
encoded_subtype = urllib.parse.quote(subtype)  # Encode the 'Time Off' parameter
date = '2025-02-07'
url = f'/api/v1/scheduling/employee_timeoff/accruals?subtype_name={encoded_subtype}&date={date}'
conn.request("GET", url, payload, headers)
res = conn.getresponse()
if int(res.status) ==400:
  print(False)
else:
  data = res.read()
  data = data.decode("utf-8")
  print(data)
  data = json.loads(data)
  payCodeAccrualArray = [[],[],[]]
  if len(data)>0:
    for i in range(0,len(data)):
      if len(data[i]['balances'])>0:
        print(data[i]['balances'][0]['dayBalances'][0]['availableBalanceInSeconds'])
        print(type(data[i]['balances'][0]))
        print(data[i]['balances'][0]['accrualCode']['qualifier'])
        #data[i]['balances']['dayBalances']['availableBalanceInSeconds']