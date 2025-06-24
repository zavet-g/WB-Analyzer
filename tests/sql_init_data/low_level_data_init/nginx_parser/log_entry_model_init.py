import re

from datetime import UTC
from datetime import datetime
from datetime import timedelta

from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import Insert

from apps.api.v1.models.log_entry_model import LogEntryModel


def get_log_entry_model_init() -> list[Insert]:
    """Создает SQL выражение для вставки логов из nginx_access.log в таблицу log_entry_model,
    разбивая их на группы по 20 штук с разным server_id.

    Returns:
        List[Insert]: Список SQL выражений для множественной вставки.
    """

    log_file_path = 'src/nginx_access.log'

    # Регулярное выражение для парсинга строки Nginx-лога
    log_pattern = re.compile(
        r'(?P<remote_addr>\S+) - - \[(?P<timestamp>[^\]]+)] '
        r'"(?P<method>\S+) (?P<uri>\S+) (?P<http_version>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )

    log_entries = []
    base_time = datetime.now(tz=UTC)

    with open(log_file_path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            match = log_pattern.match(line)
            if not match:
                continue  # пропустить строки, не соответствующие шаблону

            gd = match.groupdict()  # словарь с данными из строки

            try:
                # Преобразование строки времени из access-лога в datetime с учетом временной зоны
                parsed_time = datetime.strptime(gd['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
            except ValueError:
                parsed_time = base_time + timedelta(
                    seconds=i
                )  # fallback если парсинг времени не удался

            server_id = i // 20 + 1

            log_entries.append(
                {
                    'timestamp': parsed_time,  # время запроса
                    'remote_addr': gd['remote_addr'],  # IP-адрес клиента
                    'method': gd['method'],  # HTTP-метод (GET, POST и т.п.)
                    'uri': gd['uri'],  # запрошенный путь
                    'http_version': gd['http_version'],  # версия HTTP
                    'status': int(gd['status']),  # статус-код ответа
                    'size': int(gd['size']),  # размер ответа в байтах
                    'referrer': gd['referrer'] or None,  # откуда пришёл запрос (может быть "-")
                    'user_agent': gd['user_agent'],  # строка user-agent клиента
                    'server_id': server_id,  # внешний ключ на server_model
                }
            )

    return [insert(LogEntryModel).values(log_entries)]
