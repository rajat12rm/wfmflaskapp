import http.client
import json

conn = http.client.HTTPSConnection("partnersand-034.cfn.mykronos.com")
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
headers = {
  'Content-Type': 'application/json',
  'Authorization': 't_e0zyGYqK1uIcluRNL7_alkCnU',
  'Cookie': 'AUTHZ_TOKEN=VHlnNUptQWd6NzNxMTM0dm5rVGxYQ25FdENuOWZQcGU5MU1rL1NqSnRFVEphbytMTDdmZi9aQk5jNkNDb09FVGtRQ3F6dGV2UkxCUWErOXhVNUIwVkkrNFplbjlwYlUwWVp5NHJqcGlacEJiejkwQ1hOak1pejFqb1NmWDdFbXFNWVc3Ty9xYjIrRlVWMzRZa25RWGlvRGdWbkJDQXVHYm51ZDdlSStrbTFOOHlkMkd2cjI3eVBhV2hEYVpnWGJmSVlTMzVhT0l0VUo3ZW5sdVgrMG1QTXNHOFdXOGVjS3pqVllBNUs3M29uM241QlF6NFZQNjJCQnZSbENSVStmQ2tVb2tEbmFJcXVFWGE2Z0RuYUljK0t0a1IzMHp5d0o2X3Yy; WFC_INSTANCE=LI1IuiuN8qZPIaKgkfu+SJ23W7Mr7kO4OreJz/y8b4Ei0OGSdxJ2EMcevOX4oeZ3Bf1sbFNHQ3McC3sZX+5JCchCoxeYzUKdby8zlnovBGA-; WFC_TENANT_ID=86AXmiQ/Bda0y6ZpH0+ZClmLwmbYtuJD7PvhvPkqmyNE4q0p43ANGgJug8u/scZq2GZ5AyuhGJO6mPwnpliiNw--; WFC_USER=O4hEH4l74iiPyy/5WOY32Vkj7m+sFR9glkopKsuQ/+QuT155Tzz5ut811EDrjODF; JSESSIONID=1C5226E07C237A03A4694CBB6B24219A; srv_id=57efcb80edcc9fab369c13f168bc479f'
}
conn.request("POST", "/api/v1/commons/hyperfind/execute", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))