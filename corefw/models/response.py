from corefw.constants.messages import UNKNOWN_ERROR


class Response(dict):
    """
    Standard model response
    {
        data: {}
        message: ""
        code: ""
        response_params: []
    }
    """

    def __new__(cls, message=UNKNOWN_ERROR, data=None, response_params=None):
        response = {
            "code": message[0],
            "message": message[1]
            if not response_params
            else message[1].format(*response_params),
            "data": data,
        }
        return response
