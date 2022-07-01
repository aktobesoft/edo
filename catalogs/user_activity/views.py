from datetime import datetime
from catalogs.user_activity.models import UserActivity
from core.db import database
from sqlalchemy import insert

async def post_user_activity(user_activity : dict, **kwargs):
    query = insert(UserActivity).values(
                        device_token = user_activity['device_token'], 
                        last_activity = datetime.now(),
                        action = user_activity['action'], 
                        user_id = user_activity['user_id'], )

    return await database.execute(query)

