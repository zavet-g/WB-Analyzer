import asyncio
import sys

from importlib import import_module


async def cli() -> None:
    """Императивный запуск Python модулей.

    Запуск:
        python3 -m cli module_name function_name *function_params
    """
    module_name = sys.argv[1]
    fn_name = sys.argv[2]
    args = sys.argv[3:]

    module = import_module(module_name)
    fn = getattr(module, fn_name)

    await fn(*args) if args else await fn()


if __name__ == '__main__':
    asyncio.run(cli())
