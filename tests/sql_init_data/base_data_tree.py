from tests.sql_init_data.low_level_data_init.nginx_parser.log_entry_model_init import (
    get_log_entry_model_init,
)
from tests.sql_init_data.low_level_data_init.nginx_parser.server_model_init import (
    get_server_model_init,
)

__all__ = [
    'base_parser_tree',
]


base_parser_tree = get_server_model_init() + get_log_entry_model_init()
