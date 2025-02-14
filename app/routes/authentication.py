from flask import Blueprint, jsonify,current_app,request
import logging
import http.client
from config import Config
from datetime import datetime
from ..services.function import (generateAccessKeyPayload,
                               getUserAccessToken)


authentication_bp = Blueprint('authentication', __name__)

@authentication_bp.route('/api/authentication', methods=['POST'])
def authentication():
    try:
        data = request.get_json()

        # check for empty username password or missing one
        if data['password']==None or len(data['password'])==0 or data['username'] == None or len(data['username'])==0:
            message = "User Name and Password Cannot be Empty or Null"
            return jsonify(message),400
    

        else:
            print(current_app.config['loginUserArray'])
        
            usernameObject= Config(data['username'])
            conn = http.client.HTTPSConnection(usernameObject.wfm_url)
            #print(usernameObject.name)

            accessKeyHeaders = {
            'Content-Type': 'application/x-www-form-urlencoded'
                    }

            wfm_access_token, wfm_id_token = getUserAccessToken(
                                                conn,
                                                usernameObject.wfmAccessTokenApiUrlEndPoint,
                                                generateAccessKeyPayload(
                                                    data['username'],
                                                    data['password'],
                                                    usernameObject.wfmClientId,
                                                    usernameObject.wfmClientSecretKey, 
                                                    usernameObject.wfmPasswordGrantType
                                                    ),
                                                accessKeyHeaders
                                    )
            if wfm_access_token and wfm_id_token and len(wfm_access_token)>0 and len(wfm_id_token)>0:
                loginTime = str(datetime.now())
                if len(current_app.config['loginUserArray'])==0:
                    current_app.config['loginUserArray'] = {
                    f'{usernameObject.name}' : {
                        "time":loginTime,
                        "object":usernameObject,
                        "awsSessionId" : usernameObject.name+str(datetime.now()).replace(" ",'-').replace(":",'-').replace(".","-"),
                        "wfmAccessToken" : wfm_access_token,
                        "wfmIdToken" : wfm_id_token
                        }
                    } 
                else:
                    current_app.config['loginUserArray'][usernameObject.name] = {
                        "time":loginTime,
                        "object":usernameObject,
                        "awsSessionId" : usernameObject.name+str(datetime.now()).replace(" ",'-').replace(":",'-').replace(".","-"),
                        "wfmAccessToken" : wfm_access_token,
                        "wfmIdToken" : wfm_id_token
                    }
                
                message = "Authenticated successfully"
                return jsonify(message),200
            else:
                message = "Check Credentials or User Authorization and Try Again"
                current_app.logger.error(f"Authentication failure for {str(data['username'])}")
                return jsonify(str(message)),401

    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify(str(e)),400
