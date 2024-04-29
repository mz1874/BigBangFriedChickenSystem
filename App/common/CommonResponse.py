class CommonResponse:
    def __init__(self, status_code=200, message="Success", data=None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_dict(self):
        response_dict = {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data
        }
        return response_dict

    @staticmethod
    def success(message="Success", data=None):
        return CommonResponse(status_code=200, message=message, data=data).to_dict()


    @staticmethod
    def failure(message="Failure", data=None, status_code=400):
        return CommonResponse(status_code=status_code, message=message, data=data).to_dict()
