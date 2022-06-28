from datetime import datetime, timezone
from json import loads as parse_json
from string import Template as StandardTemplate
from typing import Any, Callable, Final, Optional

from aiofiles import open as open_file
from aiohttp import ClientSession
from discord import Member
from dotenv import dotenv_values, find_dotenv
from humanize import naturaltime


class Constants:
    QI_BOT_VERSION: Final[str] = "0.1.0"
    DEFAULT_COMMAND_PREFIX: Final[str] = "."


class Config:
    _ENV: Final[dict[str, Any]] = dotenv_values(dotenv_path=find_dotenv(), verbose=True)

    BOT_TOKEN: Final[str] = _ENV["BOT_TOKEN"]
    SERVER_ID: Final[int] = int(_ENV["SERVER_ID"])
    DEV_MODE_ENABLED: Final[bool] = _ENV.get("DEV_MODE_ENABLED", False)
    CUSTOM_COMMAND_PREFIX: Final[Optional[str]] = _ENV.get("CUSTOM_COMMAND_PREFIX")
    CUSTOM_LOG_THRESHOLD: Final[Optional[str]] = _ENV.get("CUSTOM_LOG_THRESHOLD")

    @classmethod
    def get_channel_id(cls, channel_name: str) -> int:
        return cls._ENV.get(f"{channel_name.upper()}_CHANNEL_ID", 0)


class Template(StandardTemplate):
    sub: Final[Callable[..., str]] = StandardTemplate.substitute
    safe_sub: Final[Callable[..., str]] = StandardTemplate.safe_substitute


class Utils:
    _HTTP_SESSION: Final[ClientSession] = ClientSession()

    _JSON_FILE_PATH: Final[Template] = Template("assets/data/${name}.json")
    _MEMBER_NAMETAG: Final[Template] = Template("${name}#${tag}")
    _TIME_FORMAT: Final[Template] = Template("<t:${timestamp}> (${elapsed})")

    @classmethod
    def format_time(cls, time: datetime) -> str:
        # noinspection PyTypeChecker
        elapsed = naturaltime(datetime.now(timezone.utc) - time)
        return cls._TIME_FORMAT.sub(timestamp=int(time.timestamp()), elapsed=elapsed)

    @classmethod
    def get_member_nametag(cls, member: Member) -> str:
        return cls._MEMBER_NAMETAG.sub(name=member.name, tag=member.discriminator)

    @classmethod
    async def load_content_from_url(cls, url: str) -> bytes:
        async with cls._HTTP_SESSION.get(url) as response:
            return await response.read()

    @classmethod
    async def load_json_from_file(cls, name: str) -> dict[str, Any] | list[Any]:
        filename = cls._JSON_FILE_PATH.sub(name=name)
        async with open_file(filename, mode="r", encoding="utf-8") as file:
            return parse_json(await file.read())
