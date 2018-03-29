"""HTTP helpers."""


class Status(object):

    @staticmethod
    def code(response_or_status_code):
        if isinstance(response_or_status_code, int):
            return response_or_status_code
        return response_or_status_code.status_code

    @classmethod
    def good(cls, response_or_status):
        return 200 <= cls.code(response_or_status) < 300
