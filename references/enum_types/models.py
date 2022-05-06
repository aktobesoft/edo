import enum

class step_type(enum.Enum):
    line = 'Линейное'
    paralel = 'Паралельное'

class status_type(enum.Enum):
    signed = 'Подписан'
    rejected = 'Отклонен'
    canceled = 'Отменен'
    in_process = 'В работе'
    draft = 'Черновик'    