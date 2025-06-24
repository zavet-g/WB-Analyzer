from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import Insert

from apps.api.v1.models.server_model import ServerModel


def get_server_model_init() -> list[Insert]:
    """Создает SQL выражение для вставки тестовых серверов с фиксированными ID.

    Returns:
        List[Insert]: Список с одним SQL выражением для множественной вставки.
    """
    test_servers = [
        {
            'id': 1,
            'name': 'main-nginx',
            'description': 'Основной боевой сервер с Nginx',
            'ip_address': '192.168.0.1',
        },
        {
            'id': 2,
            'name': 'dev-nginx',
            'description': 'Стенд для тестирования и разработки',
            'ip_address': '192.168.0.2',
        },
        {
            'id': 3,
            'name': 'backup-nginx',
            'description': 'Резервная копия основного сервера',
            'ip_address': '192.168.0.3',
        },
        {
            'id': 4,
            'name': 'legacy-nginx',
            'description': 'Старый сервер с устаревшей конфигурацией',
            'ip_address': '192.168.0.4',
        },
        {
            'id': 5,
            'name': 'monitoring-nginx',
            'description': 'Сервер для логов и мониторинга',
            'ip_address': '192.168.0.5',
        },
    ]

    return [insert(ServerModel).values(test_servers)]
