import enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
from typing import Dict, Any


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class MessageParser(ABC):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        payload_dict = json.loads(message.payload)
        return self.parse_payload(payload_dict)

    @abstractmethod
    def parse_payload(self, payload: Dict[str, Any]) -> ParsedMessage:
        ...


class TelegramParser(MessageParser):
    def parse_payload(self, payload: Dict[str, Any]) -> ParsedMessage:
        pass


class MattermostParser(MessageParser):
    def parse_payload(self, payload: Dict[str, Any]) -> ParsedMessage:
        pass


class SlackParser(MessageParser):
    def parse_payload(self, payload: Dict[str, Any]) -> ParsedMessage:
        pass


class ParserFactory:
    _parsers = {
        MessageType.TELEGRAM: TelegramParser(),
        MessageType.MATTERMOST: MattermostParser(),
        MessageType.SLACK: SlackParser()
    }

    @classmethod
    def get_parser(cls, message_type: MessageType) -> MessageParser:
        return cls._parsers[message_type]
