"""本模块定义了 Monitor 的日志记录 Logger。
Monitor 使用 [`loguru`][loguru] 来记录日志信息。
自定义 logger 请参考 [自定义日志](https://v2.wechat_bot.dev/docs/tutorial/custom-logger)
以及 [`loguru`][loguru] 文档。
[loguru]: https://github.com/Delgan/loguru
FrontMatter:
    sidebar_position: 7
    description: wechat_bot.log 模块
"""

import logging
import sys
from typing import TYPE_CHECKING, Union

import loguru

if TYPE_CHECKING:
    # avoid sphinx autodoc resolve annotation failed
    # because loguru module do not have `Logger` class actually
    from loguru import Logger

# logger = logging.getLogger("wechat_bot")
logger: "Logger" = loguru.logger
"""Monitor 日志记录器对象。
默认信息:
- 格式: `[%(asctime)s %(name)s] %(levelname)s: %(message)s`
- 等级: `INFO` ，根据 `config.log_level` 配置改变
- 输出: 输出至 stdout
用法:
    ```python
    from wechat_bot.log import logger
    ```
"""


# default_handler = logging.StreamHandler(sys.stdout)
# default_handler.setFormatter(
#     logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s"))
# logger.addHandler(default_handler)


class Filter:
    def __init__(self) -> None:
        self.level: Union[int, str] = "INFO"

    def __call__(self, record):
        module_name: str = record["name"]
        # get plugin name instead of module name
        # module = sys.modules.get(module_name)
        # if module and hasattr(module, "__plugin__"):
        #     plugin: "Plugin" = getattr(module, "__plugin__")
        #     module_name = plugin.module_name
        record["name"] = module_name.split(".")[0]
        levelno = (
            logger.level(self.level).no if isinstance(self.level, str) else self.level
        )
        return record["level"].no >= levelno


class LoguruHandler(logging.Handler):  # pragma: no cover
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logger.remove()
default_filter: Filter = Filter()
"""默认日志等级过滤器"""
default_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "<c>{function}:{line}</c>| "
    "{message}"
)
"""默认日志格式"""
logger_id = logger.add(
    sys.stdout,
    level=0,
    diagnose=False,
    filter=default_filter,
    format=default_format,
)

__autodoc__ = {"Filter": False, "LoguruHandler": False}
