from dataclasses import dataclass
from . import config


class InvalidUsername(Exception):
    message = '''\
Invalid username / \
username is 4-32 characters long, \
no _,- or . at the beginning, \
no __ or . or . or .. or .- or _- inside, \
no _,- or . at the end'''


class InvalidEmail(Exception):
    message = '''\
Invalid email / \
email must consist an email prefix and an email domain \
following this format: prefix@domain'''


class InvalidPassword(Exception):
    message = '''\
Invalid password / \
Has minimum 8 characters in length, \
At least one uppercase English letter, \
At least one lowercase English letter, \
At least one digit, \
At least one special character'''


class InvalidAccountType(Exception):
    account_types = config.get('ACCOUNT_TYPES')
    message = 'Account must be of one of these types: '\
              + ', '.join(account_types)


class InvalidSecretKey(Exception):
    message = 'Not authorized to have admin account'


class InvalidDateFormat(Exception):
    message = 'Date must follow the ISO 8601 format'


@dataclass
class PastDate(Exception):
    message: str


class UnsupportedLanguage(Exception):
    supported_languages = config.get('SUPPORTED_LANGUAGES')
    message = 'This language is not supported at the moment. We are currently supporting: '\
              + ', '.join([lang[0] for lang in supported_languages])


class UnsupportedCurrency(Exception):
    supported_currencies = config.get('SUPPORTED_CURRENCIES')
    message = 'This currency is not supported at the moment. We are currently supporting: ' \
              + ', '.join([curr[1] for curr in supported_currencies])


@dataclass
class DBIntegrityError(Exception):
    message: str


@dataclass
class NotExist(Exception):
    message: str


class InvalidUserIdentity(Exception):
    message = "Invalid user identity"


class Unauthorized(Exception):
    message = "Not authorized to perform this action"


class IncompatibleSeatOffering(Exception):
    message = "One or more update fields are not compatible"


@dataclass
class IncompatibleUpdate(Exception):
    message: str


