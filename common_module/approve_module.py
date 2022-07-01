import json
from sqlalchemy import select
import requests
from catalogs.approval_route.views import get_current_approval_routes_by_approval_process_id
from catalogs.user_activity.models import UserActivity

from core.db import database


async def notificate_user_by_approval_process_id(approval_process_id: int, **kwargs):
    current_routes = await get_current_approval_routes_by_approval_process_id(approval_process_id, **kwargs)
    if len(current_routes)>0:
        for itemAR in current_routes:
            token = await get_device_token(itemAR['user_id'])
            if token == '':
                return

            context = {
                'user': itemAR['user_name'],
                'token': token,
                'body': str('ggggg'),
                'title': 'Поступил новый документ на согласования',
                'data': {}
                }
            send_message(context)

async def get_device_token(user_id):
    
    query = select(UserActivity.device_token).\
            where(UserActivity.user_id == user_id).\
            order_by(UserActivity.last_activity.desc()).\
            limit(1)
    result = await database.fetch_one(query)
    if result == None:
        return ''
    return result['device_token']

def send_message(context):
    
    if context['token'] == '':
        return

    data = {
        'to' : context['token'],
        'collapse_key' : 'type_a',
        'notification' : {
            'body' : context['body'],
            'title': context['title']
        },
        'data' : {'click_action':'FLUTTER_NOTIFICATION_CLICK', 'documentMetadataName': 'purchase_requisition'}
    }    
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': 'key=AAAAEUUvl70:APA91bH1lNUuHm_F1VWLpgwcczHBMBeZAHOGrhrN4NV2wqJkDHinol08GP30IXknqzUcnUF4kG_v3Ygr5UlJn_DPfvrUugQuBDsWiDODp3CZr6aE09YUrX_AHsi31dA9f6V2sK63GfgV'
        }
    response = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
    content = response.content
    print(content)
    # need message log

