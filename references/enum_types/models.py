import enum

class step_type(str, enum.Enum):
    line = 'Линейное'
    paralel = 'Паралельное'

class status_type (str, enum.Enum):
    signed = 'Подписан'
    rejected = 'Отклонен'
    canceled = 'Отменен'
    in_process = 'В работе'
    draft = 'Черновик'    