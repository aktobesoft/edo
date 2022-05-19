
from references.enum_types.models import step_type


async def list_object_to_list_dict(list_of_object: list, ignore_field: list = []):
    listDict = []
    for item in list_of_object:
        itemDict = dict(item)
        itemDict['type'] = 'Линейное' if itemDict['type'] == step_type.line  else 'Паралельное'
        # for field in ignore_field:
        #     itemDict.pop(itemDict)
        listDict.append(itemDict)
    return listDict