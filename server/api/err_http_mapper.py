mapping = {
    'InvalidUsername': 400,
    'InvalidEmail': 400,
    'InvalidPassword': 400,
    'InvalidAccountType': 400,
    'InvalidSecretKey': 401,
    'DBIntegrityError': 409,
    'InvalidUserIdentity': 401,
    'NotExist': 404,
    'Unauthorized': 403,
}


def http_code_mapper(err_type):
    return mapping.get(err_type)
