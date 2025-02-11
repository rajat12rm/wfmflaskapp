from flask import Blueprint, jsonify, request,current_app
from ..services.function import (compare_timestamps,convoHistory)
from datetime import datetime
import boto3
import http.client

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
        try:
            data = request.get_json()
            print(current_app.config['loginUserArray'])
            if str(data['username']) in current_app.config['loginUserArray']:
                currentTime = str(datetime.now())
                print(currentTime)
                loginTime = str(current_app.config['loginUserArray'][data['username']]['time'])
                print(loginTime)
                result = compare_timestamps(loginTime,currentTime)
                print(result)
                if result==False:
                    message = "Session Time Out"
                    return jsonify(message),408
                else:
                    user = current_app.config['loginUserArray'][data['username']]['object']
                    client = boto3.client('lexv2-runtime',
                      region_name='us-east-1',
                      aws_access_key_id=user.aws_access_key,
                      aws_secret_access_key=user.aws_secret_access_key
                      )
                    print (client)
                    conn = http.client.HTTPSConnection(user.wfm_url)
                    headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'''{current_app.config['loginUserArray'][data['username']]['wfmAccessToken']}''',
                    'Cookie': f'''AUTHZ_TOKEN= "{current_app.config['loginUserArray'][data['username']]['wfmIdToken']}";'''
                    }
                    chatOut = convoHistory(conn,headers,data['userMessage'],user,client,current_app.config['loginUserArray'][data['username']]['awsSessionId'])
                    return jsonify(chatOut),200
                     
                
            else:
                message = "User not Authenticated, Please Login"
                return jsonify(message),403

            
        except Exception as e:
              print(e)
              return jsonify(str(e)),400