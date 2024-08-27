from fastapi import status

class BaseError(Exception):

    def __init__(
        self,
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_msg=None,
        error_code=None,
        error_detail=None,
    ):
        super(BaseError, self).__init__()
        self.code = code
        self.error_code = error_code
        self.error_msg = error_msg
        self.error_detail = error_detail
    
    def __str__(self):
        return self.__class__.__name__


class CustomException(BaseError):
    def __init__(
        self,
        error_msg=None,
        error_code=None,
        error_detail=None,
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super(CustomException, self).__init__(
            code=code,
            error_msg=error_msg,
            error_code=error_code,
            error_detail=error_detail,
        )