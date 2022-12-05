class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        self.status_code = status_code \
            if status_code is not None else self.__class__.status_code

    def to_dict(self):
        return dict(message=self.message)
