import json
import urllib.parse
from datetime import datetime,timedelta
from ..services.wfmPunchCreateRequest import punch_create_payload
from ..services.wfmScheduleRetrieveRequest import schedule_retrieve_payload
from ..services.wfmTimeOffCreateRequest import createTimeOffRequestPayload
from ..services.wfmRetrieveTimeOff import retrieveTimeOffPayload
from ..services.wfmUpdateTimeOffStatusRequest import UpdateTimeOffStatusPayload
from ..services.wfmRunAllHomeHyperfindRequest import  allhomeHyperfindPayload
def convoHistory(conn,headers,userMessage,userObject,aws_client,awsSessionId):
    output = lex_convo(aws_client,userObject.botId,userObject.botAliasId,userObject.localeId,awsSessionId, userMessage)
    if ((str(output["sessionState"]["intent"]["name"]) == "PunchIn" and str(output["sessionState"]["intent"]["state"])) == "Fulfilled") or ((str(output["sessionState"]["intent"]["name"]) == "PunchOut" and str(output["sessionState"]["intent"]["state"])) == "Fulfilled"):
        id =2
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)
        if output["sessionState"]["intent"]["name"] == "PunchOut":
          id =4 

        if (punch_import_request(conn,headers,userObject.punch_import_api_url_endpoint,userObject.name,str(datetime.now()).replace(" ","T"),id)):
            response = {
              "category":"text",
              "data":"",
              "message":"Punched SuccessFully"
                }
            return response
        else:
            response = {
              "category":"text",
              "data":"",
              "message":"Not Able To Punch In WFM, Please check Settings or Try Again Later"
                }
            return response
           

    elif (str(output["sessionState"]["intent"]["name"]) == "getSchedule" and str(output["sessionState"]["intent"]["state"])) == "Fulfilled":
        print(output)
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)

        #extract date for schedule - 
        sdate = str(output["sessionState"]["intent"]["slots"]["date"]["value"]["interpretedValue"])
        print(sdate)
        schedule =schedule_retrieve_request(conn,headers,userObject.schedule_retrieve_api_url_endpoint,userObject.name,sdate,sdate)
        if schedule:
            scheduleString = ""
            for i in range(len(schedule)):
              scheduleString = schedule[i] +"\n"+ scheduleString
            response = {
              "category":"text",
              "data":"",
              "message":scheduleString
              }
            return response
        else:
            response = {
              "category":"text",
              "data":"",
              "message":"No Schedules Found"
              }
            return response
    elif (str(output["sessionState"]["intent"]["name"]) == "applyTimeOff" and str(output["sessionState"]["dialogAction"]["type"]) == "ElicitSlot" and str(output["sessionState"]["dialogAction"]["slotToElicit"]) == "requestSubtype"):
        print(output)
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)

        subtype = getRequestSubtype(conn,headers,userObject.wfmRequestSubtypeApiUrlEndPoint)
        print("Retrived subtype from function")
        print(type(subtype))
        if subtype:
          if len(subtype)>0:
            response = {
              "category" : "table",
              "message" : message,
              "data": str(subtype),
              "select": 0
              }
            print(response)
            return response
          else:
            message = "No Subtypes Found in WFM for you, Please Contact Admin or Manager"
            response = {
              "category" : "text",
              "message" : message
              }
            return response
        else:
          message = "Could Not Retrieve Your Time Off Request Subtypes from WFM, try again later!"
          response = {
           "category" : "Text",
           "message" : message 
           }
          return response
        
    elif (str(output["sessionState"]["intent"]["name"]) == "applyTimeOff" and str(output["sessionState"]["dialogAction"]["type"]) == "ElicitSlot" and str(output["sessionState"]["dialogAction"]["slotToElicit"]) == "payCode"):
        print(output)
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)

        subtype = str(output["sessionState"]["intent"]["slots"]["requestSubtype"]["value"]["originalValue"])
        payCodeAccrualbalances = getPayCodeAndAccrualBalanceFromRequestSubtype(conn,
                                                      headers,
                                                      userObject.wfmRequestGetTimeOffAccrualBalanceApiUrlEndPoint,
                                                      subtype,
                                                      str(datetime.now()).split(" ")[0]
                                                      )
        if payCodeAccrualbalances:
          if len(payCodeAccrualbalances)>0:
            response = {
              "category" : "table",
              "message" : message,
              "data": str(payCodeAccrualbalances),
              "select": 0
              }
            return response
          
          else:
            message = "No Pay Codes Found in WFM for you, Please Contact Admin or Manager"
            response = {
              "category" : "text",
              "message" : message
              }
            return response
        else:
          message = "Could Not Retrieve Your Accrual Balances from WFM, try again later!"
          response = {
           "category" : "Text",
           "message" : message 
           }
          return response
        
    elif (str(output["sessionState"]["intent"]["name"]) == "applyTimeOff" and str(output["sessionState"]["intent"]["state"])) == "Fulfilled":
      print(output)
      message = ''
      for i in range (len(output['messages'])):
        message += " "+output['messages'][i]['content']
      print(message)
      print("API Request Applying in WFM")
      applyTimeOffSuccess= applyTimeOff(
                                conn,
                                headers,
                                userObject.wfmCreateTimeOffApiUrlEndPoint,
                                output["sessionState"]["intent"]["slots"]["requestSubtype"]["value"]["originalValue"],
                                output["sessionState"]["intent"]["slots"]["payCode"]["value"]["originalValue"],
                                output["sessionState"]["intent"]["slots"]["sdate"]["value"]["interpretedValue"],
                                output["sessionState"]["intent"]["slots"]["edate"]["value"]["interpretedValue"]
                                )
      
      if applyTimeOffSuccess:
        message = "Time Off Applied Successfully! Take Care"
        response = {
          "category" : "Text",
          "message" : message 
        }
        return response
      else:
        message = "There Was An Issue In Applying Time Off"
        response = {
          "category" : "Text",
          "message" : message 
        }
        return response
    
    elif (str(output["sessionState"]["intent"]["name"]) == "getTimeOffRequests" and str(output["sessionState"]["dialogAction"]["type"]) == "ElicitSlot" and str(output["sessionState"]["dialogAction"]["slotToElicit"]) == "id"):
        print(output)
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)

        requestsArray = getPendingTimeOffRequests(conn,
                                                  userObject.wfmRequestTimeOffApiUrlEndPoint,
                                                  headers)
        if requestsArray:
          response = {
              "category" : "table",
              "message" : message,
              "data": str(requestsArray),
              "select": 0
          }
          return response
        else:
          message = "Could Not Retrieve Any Pending Time Off Requests !"
          response = {
           "category" : "Text",
           "message" : message 
           }
          return response
    elif (str(output["sessionState"]["intent"]["name"]) == "getTimeOffRequests" and str(output["sessionState"]["dialogAction"]["type"]) == "ElicitSlot" and str(output["sessionState"]["dialogAction"]["slotToElicit"]) == "action"):
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)
        response = {
              "category" : "table",
              "message" : message,
              "data": str(fetchActionsOnTimeOffRequests()),
              "select": 0
          }
        return response
    elif (str(output["sessionState"]["intent"]["name"]) == "getTimeOffRequests" and str(output["sessionState"]["intent"]["state"])) == "Fulfilled":
        print(output)
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)
        requestId = output["sessionState"]["intent"]["slots"]["id"]["value"]["originalValue"]
        actionType = output["sessionState"]["intent"]["slots"]["action"]["value"]["originalValue"]
        print(requestId)
        print(actionType)
        if actionType == 'Cancel':
          #8 is for cancel request
          action = applyActionsOnTimeOffRequests(conn,
                                                 userObject.wfmUpdateTimeOffApiUrlEndPoint,
                                                 headers,
                                                 requestId,
                                                 8)
          if action:
            message = "The Request Is Cancelled SuccessFully !"
            response = {
            "category" : "Text",
            "message" : message 
            }
            return response
          else:
            message = "The Request Cannot be Updated !"
            response = {
            "category" : "Text",
            "message" : message 
            }

            return response

        if actionType == 'Approve':
          #4 is for approve request
          action = applyActionsOnTimeOffRequests(conn,
                                                 userObject.wfmUpdateTimeOffApiUrlEndPoint,
                                                 headers,
                                                 requestId,
                                                 4)
          if action:
            message = "The Request Is Approved SuccessFully !"
            response = {
            "category" : "Text",
            "message" : message 
            }
            return response
          else:
            message = "The Request Cannot be Updated !"
            response = {
            "category" : "Text",
            "message" : message 
            }

            return response

        if actionType == 'Ignore':
          #5 is for ignore request
          action = applyActionsOnTimeOffRequests(conn,
                                                 userObject.wfmUpdateTimeOffApiUrlEndPoint,
                                                 headers,
                                                 requestId,
                                                 5)
          if action:
            message = "The Request Is Ignored SuccessFully !"
            response = {
            "category" : "Text",
            "message" : message 
            }
            return response
          else:
            message = "The Request Cannot be Updated !"
            response = {
            "category" : "Text",
            "message" : message 
            }

            return response

    elif (str(output["sessionState"]["intent"]["name"]) == "reportingEmployees" and str(output["sessionState"]["intent"]["state"])) == "Fulfilled":
      print(output)
      message = ''
      for i in range (len(output['messages'])):
        message += " "+output['messages'][i]['content']
      print(message)
      reportingEmployees = executeAllHomeHyperfind(conn,
                                                   userObject.wfmExecuteHyperfindApiUrlEndPoint,
                                                   headers)
      if reportingEmployees:
        response = {
              "category" : "table",
              "message" : message,
              "data": str(reportingEmployees)
          }
        return response
      else:
          message = "Could Not Fetch Employee List, check settings or Try Again Later!"
          response = {
            "category" : "Text",
            "message" : message 
            }
         
         


    else:
        #Let the normal conversion flow from Lex Happen
        message = ''
        for i in range (len(output['messages'])):
            message += " "+output['messages'][i]['content']
        print(message)
        response = {
           "category" : "Text",
           "message" : message 
           }
        return response
   

def lex_convo(client,botId,botAliasId,localeId , sessionId, user_query):
  response = client.recognize_text(botId=botId,
                                   botAliasId=botAliasId,
                                   localeId=localeId,
                                   sessionId=sessionId,
                                   text=user_query
                                   )
  return response
def generateAccessKeyPayload(username,
                             password,
                             wfmClientId,
                             wfmClientSecretKey,
                             wfmPasswordGrantType):
    accessKeyPayload = f'username={username}&'+f'password={password}&'+f'client_id={wfmClientId}&'+f'client_secret={wfmClientSecretKey}&'+f'grant_type={wfmPasswordGrantType}'
    return accessKeyPayload


def getUserAccessToken(conn,
                       wfmAccessTokenApiUrlEndPoint,
                       accessKeyPayload,
                       accessKeyHeaders
                       ):   
    conn.request("POST",
                 wfmAccessTokenApiUrlEndPoint,
                 accessKeyPayload,
                 accessKeyHeaders
                 )
    res = conn.getresponse()
    print(res.status)
    if int(res.status) == 400:
      return (None,None)
    else:
      data = res.read()
      #print(data.decode("utf-8"))
      data = data.decode("utf-8")
      data = json.loads(data)
      #print(type(data))
      print(data, "\n\n\n")
      return (data['access_token'],data['id_token'])
    
def compare_timestamps(login_time_str, current_time_str):
    # Parse the string timestamps into datetime objects including microseconds
    login_time = datetime.strptime(login_time_str, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S.%f")
    
    # Calculate the difference between the two timestamps
    time_difference = current_time - login_time
    
    # Define the maximum allowed difference as 2 minutes and 50 seconds
    max_difference = timedelta(minutes=29, seconds=50)
    
    # Compare the time difference with the maximum allowed difference
    if time_difference > max_difference:
        return False
    else:
        return True
    
def punch_import_request(
    conn,
    headers,
    url,
    employee_id,
    date_time,
    id
    ):
  
  conn.request("POST", 
               url,
               punch_create_payload(
                employee_id,
                date_time,
                id
                ), 
               headers)
  res = conn.getresponse()
  if int(res.status)==400:
    print(400)
    print(res)
    return False
  elif int(res.status)==200:
    data = res.read()
    print(data.decode("utf-8"))
    return (True)
  

def schedule_retrieve_request(
    conn,
    headers,
    url,
    employee_id,
    start_date,
    end_date
    ):
  print(url)
  print(employee_id)
  payload = ""
  conn.request("GET",
               f"{url}?select=SHIFTS&start_date={start_date}&end_date={end_date}&person_number={employee_id}",
               payload,
               headers
               )
  res = conn.getresponse()
  data = res.read()
  data = data.decode("utf-8")
  print(data)
  if int(res.status) == (400):
    print(400)
    return False
  elif int(res.status) ==(200):
    print(200)
    scheduleArray = []
    data = json.loads(data)
    print(type(data))
    for i in range(len(data["shifts"])):
      # Extract Job from Business Structure
      x= str(data["shifts"][i]["segments"][0]['orgJobRef']['qualifier'])
      job = x.split("/")[-1]
      print(job)
      # Extract Dates
      startDate= data["shifts"][i]["startDateTime"].split("T")[0]
      endDate =data["shifts"][i]["endDateTime"].split("T")[0]
      # Extract Time
      startTime =convert_time(data["shifts"][i]["startDateTime"].split("T")[1]) 
      endTime = convert_time(data["shifts"][i]["endDateTime"].split("T")[1])
      # Append Data
      scheduleArray.append(
                f"For schedule on {startDate}, "
                f"schedule begins at {startTime} "
                f"and ends on {endDate} at {endTime} "
                f"with Job of {job}"
                )
    print(scheduleArray)
    return scheduleArray

  
def convert_time(time_str):
    # Parse the time string to a datetime object
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    # Format the time to a 12-hour format with AM/PM
    formatted_time = time_obj.strftime('%I %p')
    # Remove leading zero and convert to lowercase
    formatted_time = formatted_time.lstrip('0').lower()
    return formatted_time

def getRequestSubtype(conn,headers,url):
  payload = ''
  conn.request("GET", url, payload, headers)
  res = conn.getresponse()
  if int(res.status) == 400:
    return False
  else:
    data = res.read()
    data=data.decode("utf-8")
    data = json.loads(data)
    print(data)
    #print(data)
    subTypeArray = []
    if len(data)>0:
        subTypeArray.append(['Request Sub-Types'])
        for i in range(0,len(data)):
            print(data[i]['name'],"\n")
            subTypeArray.append([data[i]['name']])
        print(i+1," Request Subtypes Found")
        return subTypeArray
    else:
        print("No Subtypes Found")
        return subTypeArray

def getPayCodeAndAccrualBalanceFromRequestSubtype(conn,headers,url,subtype,currentdate):
  payload = ''
  #subtype = 'Time Off'
  encoded_subtype = urllib.parse.quote(subtype)  # Encode the 'Time Off' parameter
  conn.request("GET",
               f'{url}?subtype_name={encoded_subtype}&date={currentdate}',
               payload,
               headers)
  res = conn.getresponse()
  if int(res.status) ==400:
    return False
  else:
    data = res.read()
    data = data.decode("utf-8")
    print(data)
    data = json.loads(data)
    payCodeAccrualTable = []
    if len(data)>0:
      # set table headers
      payCodeAccrualTable.append(["Pay Code","Balance","Accrual"])
      for i in range(0,len(data)):
        if len(data[i]['balances'])>0:
          payCodeAccrualTable.append([data[i]['payCode']['qualifier'],
                                      (int(data[i]['balances'][0]['dayBalances'][0]['availableBalanceInSeconds'])/3600),
                                      data[i]['balances'][0]['accrualCode']['qualifier']])
      print(payCodeAccrualTable)
      return payCodeAccrualTable
       
       
def applyTimeOff(conn,headers,url,requestSubType,payCode,startDate,endDate):
  conn.request("POST",
              url,
              createTimeOffRequestPayload(
                requestSubType,
                startDate,
                endDate,
                payCode
                ),
              headers
              )
  
  res = conn.getresponse()
  print(res.status)
  if int(res.status)==400:
    return False
  else:
    data = res.read()
    data = data.decode("utf-8")
    print(data)
    return True

   
def getPendingTimeOffRequests(conn,url,headers):
  conn.request("POST",url, retrieveTimeOffPayload(), headers)
  res = conn.getresponse()
  if res.status == 400:
    print("Error in WFM")
    return False
  if res.status == 200:
    data = res.read()
    data = data.decode("utf-8")
    print(data)
    data = json.loads(data)
    timeOffRequestArray = []
    if len(data)>0:
      timeOffRequestArray.append(["(Action)Request-ID","Employee User-Name", "Date Of Creation","Start-Date","End-Date", "Pay Code", "Status"])
      for i in range(0,len(data)):
        print(data[i],"\n")
        timeOffRequestArray.append(
              [
              data[i]['id'],
              data[i]['creator']['qualifier'],
              data[i]['createDateTime'].split('T')[0],
              data[i]['periods'][0]['startDate'],
              data[i]['periods'][0]['endDate'],
              data[i]['periods'][0]['payCode']['qualifier'],
              data[i]['currentStatus']['name']
              ]
        )
      return timeOffRequestArray
    else:
      return False
    
def applyActionsOnTimeOffRequests(conn,url,headers,TimeOffRequestId,actionId):
  conn.request("POST",url, UpdateTimeOffStatusPayload(actionId,TimeOffRequestId), headers)
  res = conn.getresponse()
  if int(res.status) == 400:
    print("Error in WFM")
    return False
  if int(res.status) == 200:
    print("Success")
    data = res.read()
    data = data.decode("utf-8")
    print(data)
    return True

def fetchActionsOnTimeOffRequests():
  actionArray = [['Update Status To - '],['Cancel'],['Approve'],['Ignore']]
  return actionArray

def executeAllHomeHyperfind(conn,url,headers):
  conn.request("POST",url, allhomeHyperfindPayload(), headers)
  res = conn.getresponse()
  if int(res.status) == 400:
    print("Error in WFM")
    return False
  if int(res.status) == 200:
    print("Success")
    data = res.read()
    data = data.decode("utf-8")
    print(data)
    data = json.loads(data)
    print(data)
    if len(data)>0:
      reportingEmployees = []
      reportingEmployees.append(['Person Number','Employee Name'])
      personArray = (data['result']['basePersons'])
      print(personArray)
      for i in range(0,len(personArray)):
          reportingEmployees.append([personArray[i]['personNumber'],(personArray[i]['fullName'])])

      return reportingEmployees

   
   


