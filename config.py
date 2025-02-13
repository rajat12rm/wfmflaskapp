import os
from dotenv import load_dotenv
import logging

class Config:

    schedule_create_update_delete_api_url_endpoint = os.getenv('SCHEDULE_CREATE_UPDATE_DELETE_URL')
    wfm_url = os.getenv('WFM_URL')
    wfm_appkey =os.getenv('APP_KEY')
    wfm_auth_token = os.getenv('AUTHN_TOKEN')
    wfm_auth_ssid =os.getenv('AUTHN_SSID')
    schedule_retrieve_api_url_endpoint = os.getenv('SCHEDULE_RETRIEVE_URL')
    punch_import_api_url_endpoint = os.getenv('PUNCH_IMPORT_URL')
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
    botId =os.getenv('AWS_BOT_ID')
    botAliasId= os.getenv('AWS_BOT_ALIAS_ID')
    localeId=os.getenv('AWS_LOCATION')
    wfmClientId =os.getenv('WFM_CLIENT_ID')
    wfmClientSecretKey=os.getenv('WFM_CLIENT_SECRET_KEY')
    wfmPasswordGrantType =os.getenv('WFM_ACCESS_GRANT_TYPE')
    wfmAccessTokenApiUrlEndPoint =os.getenv('WFM_ACCESS_TOKEN_REQUEST_URL')
    wfmRequestSubtypeApiUrlEndPoint = os.getenv('WFM_REQUEST_SUBTYPES_URL')
    wfmRequestGetTimeOffAccrualBalanceApiUrlEndPoint = os.getenv('WFM_REQUEST_TIMEOFF_ACCRUAL_BALANCE')
    
    def __init__(self, name):
        self.name = name

    # Add other configuration settings as needed
