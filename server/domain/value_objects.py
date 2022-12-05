import re
from dataclasses import dataclass
from datetime import date
from typing import ClassVar, Union
from .exceptions import *
from . import config
'''
    Base class for value objects
'''


@dataclass(frozen=True)
class ValueObject:
    validated_data: Union[str, tuple, dict]


@dataclass(frozen=True)
class Password(ValueObject):
    regex: ClassVar[str] = config.get('REGEX').get('PASSWORD')

    def __post_init__(self):
        if re.fullmatch(self.__class__.regex, self.validated_data) is None:
            raise InvalidPassword


@dataclass(frozen=True)
class Email(ValueObject):
    regex: ClassVar[str] = config.get('REGEX').get('EMAIL')

    def __post_init__(self):
        if re.fullmatch(self.__class__.regex, self.validated_data) is None:
            raise InvalidEmail


@dataclass(frozen=True)
class Username(ValueObject):
    regex: ClassVar[str] = config.get('REGEX').get('USERNAME')

    def __post_init__(self):
        if re.fullmatch(self.__class__.regex, self.validated_data) is None:
            raise InvalidUsername


@dataclass(frozen=True)
class AccountType(ValueObject):
    choices: ClassVar[set[str]] = config.get('ACCOUNT_TYPES')
    secret_key: str = None

    def __post_init__(self):
        if self.validated_data not in self.__class__.choices:
            raise InvalidAccountType
        if self.validated_data == 'admin' and self.secret_key != config.get('SECRET_KEY'):
            raise InvalidSecretKey


@dataclass(frozen=True)
class Language(ValueObject):
    supported_languages: ClassVar[set[tuple[str, str]]] = config.get('SUPPORTED_LANGUAGES')

    def __post_init__(self):
        if self.validated_data not in self.__class__.supported_languages:
            raise UnsupportedLanguage


@dataclass(frozen=True)
class Currency(ValueObject):
    supported_currencies: ClassVar[set[tuple[str, str]]] = config.get('SUPPORTED_CURRENCIES')

    def __post_init__(self):
        if self.validated_data not in set(curr[1] for curr in self.__class__.supported_currencies):
            raise UnsupportedCurrency


@dataclass(frozen=True)
class SeatOfferingBenchmark(ValueObject):
    benchmark: dict

    def __post_init__(self):
        if not set(self.validated_data).issubset(self.benchmark['seat_offering']):
            raise IncompatibleSeatOffering('Incompatible seats offering')
        if not all(isinstance(v, int) for v in self.validated_data.values()):
            raise IncompatibleSeatOffering('Seat quantity must be a number')
        for k, v in self.validated_data.items():
            available = self.benchmark['seat_offering'][k]
            if v > available:
                raise IncompatibleSeatOffering(f'Not enough number of {k} seats. There is only {available} of them')


@dataclass(frozen=True)
class ISODate(ValueObject):
    regex: ClassVar[str] = config.get('REGEX').get('ISODATE')

    def __post_init__(self):
        if re.fullmatch(self.__class__.regex, self.validated_data) is None:
            raise InvalidDateFormat
        if date.fromisoformat(self.validated_data) < date.today():
            raise PastDate(f'{self.validated_data} has already passed')
