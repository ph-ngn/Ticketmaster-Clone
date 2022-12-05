config = {
    'SECRET_KEY': 'aPdSgVkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!z%C*F-JaNcRfUjXn2r5u8x/A?D(',
    'REGEX': {
        'USERNAME': r'^(?=.{4,32}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$',
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'PASSWORD': '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
        'ISODATE': r'^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$'

    },
    'ACCOUNT_TYPES': {'promoter', 'consumer', 'admin'},
    'SUPPORTED_LANGUAGES': {('ENGLISH', 'ENG')},
    'SUPPORTED_CURRENCIES': {('Canadian Dollar', 'CAD')},
}
