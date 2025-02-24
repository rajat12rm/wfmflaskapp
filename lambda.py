def validate_schedule_slots(slots):
    if not slots['date']:
        print("Date not found in slots")
        return {
            'isValid':False,
            'violatedSlot':'date'
        }
    date = slots['date']['value']['resolvedValues']
    return {
        'isValid':True,
        'date':date
    }

def validate_retrieve_timeoff_slots(slots):
    if not slots['id']:
        print("ID not found")
        return {
            'isValid':False,
            'violatedSlot':'id'
        }
    if not slots['action']:
        print("Action not found")
        return {
            'isValid':False,
            'violatedSlot':'action'
        }

    # requestID = slots['id']['value']['resolvedValues']
    # action = slots['id']['value']['resolvedValues']
    return {
        'isValid':True,
    }

def validate_timeoff_slots(slots):
    if not slots['sdate']:
        print("Start Date not found in slots")
        return {
            'isValid':False,
            'violatedSlot':'sdate'
        }
    if not slots['edate']:
        print("End Date not found in slots")
        return {
            'isValid':False,
            'violatedSlot':'edate'
        }
    if not slots['requestSubtype']:
        print("Request Subtype not found in slots")
        return {
            'isValid':False,
            'violatedSlot':'requestSubtype'
        }
    if not slots['payCode']:
        print("Pay Code not found in slots")
        return {
            'isValid':False,
            'violatedSlot':'payCode'
        }
        
    sdate = slots['sdate']['value']['resolvedValues']
    return {
        'isValid':True,
    }
         
         
def lambda_handler(event, context):
    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    # user_id = event['sessionState']['sessionAttributes']['user_id']
    print(intent)
    print(slots)
    print(bot)
    if intent == 'PunchIn':
        if event['invocationSource'] == 'DialogCodeHook':
                response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                    
                    }
        
                        }
                    }
                return response


        if event['invocationSource'] == 'FulfillmentCodeHook':
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots,
                        'state':'Fulfilled'
                        
                        }
            
                    },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": f"Punch In Triggered In WFM"
                        
                        
                    }
                    ]
                    }
                
            return response
            
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name':intent,
                    'slots': slots,
                    'state':'Failed'
                    
                    }
        
                },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"Not Able to Punch In Now"
                    
                    
                }
                ]
                }
            
            return response

    if intent == 'PunchOut':
        if event['invocationSource'] == 'DialogCodeHook':
                response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                    
                    }
        
                        }
                    }
                return response


        if event['invocationSource'] == 'FulfillmentCodeHook':
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots,
                        'state':'Fulfilled'
                        
                        }
            
                    },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": f"Punch Out Triggered in WFM"
                        
                        
                    }
                    ]
                    }
                
            return response
            
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name':intent,
                    'slots': slots,
                    'state':'Failed'
                    
                    }
        
                },
                "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"Not Able to Punch Out Now"
                    
                    
                }
                ]
                }
            
            return response
        
    if intent == 'getSchedule':
        print(slots)
        
        check =validate_schedule_slots(slots)
        if event['invocationSource'] == 'DialogCodeHook':
                if not check['isValid']:
                    response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit":check['violatedSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            'name':intent,
                            'slots': slots
                        
                        }
            
                            }
                        }
                    return response
                else:
                    response = {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Delegate"
                        },
                        "intent": {
                            'name':intent,
                            'slots': slots

                        }

                            }
                        }
                    return response



        if event['invocationSource'] == 'FulfillmentCodeHook':
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots,
                        'state':'Fulfilled'
                        
                        }
            
                    },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": f"Get Schedule Triggered in WFM"
                        
                        
                    }
                    ]
                    }
                
            return response
            
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name':intent,
                    'slots': slots,
                    'state':'Failed'
                    
                    }
        
                },
                "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"Not Able to Get Schedule Now"
                    
                    
                }
                ]
                }
            
            return response
        
    if intent == 'applyTimeOff':
        print(slots)
        check = validate_timeoff_slots(slots)
        if event['invocationSource'] == 'DialogCodeHook':
            if not check['isValid']:
                response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit":check['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots                  
                    }
        
                        }
                    }
                return response
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots

                    }

                        }
                    }
                return response

        if event['invocationSource'] == 'FulfillmentCodeHook':
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots,
                        'state':'Fulfilled'
                        
                        }
            
                    },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": f"Apply Time Off Triggered In WFM"
                        
                        
                    }
                    ]
                    }
                
            return response
            
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name':intent,
                    'slots': slots,
                    'state':'Failed'
                    
                    }
        
                },
                "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"Not Able to Apply Time Off Right Now"
                    
                    
                }
                ]
                }
            
            return response
        
    if intent == 'getTimeOffRequests':
        print(slots)
        check = validate_retrieve_timeoff_slots(slots)
        if event['invocationSource'] == 'DialogCodeHook':
            if not check['isValid']:
                response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit":check['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots                  
                    }
        
                        }
                    }
                return response
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots

                    }

                        }
                    }
                return response

        if event['invocationSource'] == 'FulfillmentCodeHook':
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots,
                        'state':'Fulfilled'
                        
                        }
            
                    },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": f"Request Time Off Triggered In WFM"
                        
                        
                    }
                    ]
                    }
                
            return response
            
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name':intent,
                    'slots': slots,
                    'state':'Failed'
                    
                    }
        
                },
                "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"Not Able to Fetch Any Time Off Requests !"
                    
                    
                }
                ]
                }
            
            return response