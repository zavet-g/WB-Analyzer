from apps.utils.enums.base_enum import BaseENUM


class FlagEnum(BaseENUM):
    MESSAGE_ARRIVAL = '<='  # прибытие сообщения (в этом случае за флагом следует адрес отправителя)
    MESSAGE_SENDED = '=>'  # нормальная доставка сообщения
    ADDITIONAL_ADDRESS_IN_MESSAGE = '->'  # дополнительный адрес в той же доставке
    MESSAGE_FAILED = '**'  # доставка не удалась
    MESSAGE_DELAYED = '=='  # доставка задержана (временная проблема)
