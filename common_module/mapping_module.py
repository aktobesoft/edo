
from catalogs.enum_types.models import EnumStepType


async def list_object_to_list_dict(list_of_object: list, ignore_field: list = []):
    listDict = []
    for item in list_of_object:
        itemDict = dict(item)
        listDict.append(itemDict)
    return listDict