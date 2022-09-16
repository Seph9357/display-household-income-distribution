import logging
import typing
import uuid
import rest_framework.exceptions as drf_exceptions
from rest_framework import renderers
from rest_framework.response import Response

from . import exception as id_exceptions

logger = logging.getLogger('server')


class ResponseSchema(typing.NamedTuple):

    code: str
    serialno: str
    msg: str
    data: typing.Optional[dict]


def unique_id():
    return str(uuid.uuid4())

def exception_handler(exc, context):
    """handle and solve exceptions
    """

    logger.info("Invalid Request", exc_info=exc)

    if isinstance(exc, drf_exceptions.MethodNotAllowed):
        exc = id_exceptions.IDMethodNotAllowed()

    if isinstance(exc, drf_exceptions.ParseError):
        exc = id_exceptions.ParseError()

    if isinstance(exc, drf_exceptions.UnsupportedMediaType):
        exc = id_exceptions.MediaTypeError()

    if isinstance(exc, id_exceptions.IDException):

        rs = ResponseSchema(
            code=exc.code,
            serialno=unique_id(),
            msg=exc.message,
            data=getattr(exc, 'data', None))
        return Response(rs._asdict())

    if isinstance(exc, drf_exceptions.ValidationError):
        rs = ResponseSchema(
            code='0',
            serialno=unique_id(),
            msg=id_exceptions.IDValidationError.message,
            data=getattr(exc, 'detail', None))
        return Response(rs._asdict())


    logger.exception(exc)
    data = ResponseSchema(
        code=id_exceptions.UnknownError.code,
        serialno=unique_id(),
        msg=id_exceptions.UnknownError.message,
        data=None
    )._asdict()

    return Response(data)


class WrapperJSONRender(renderers.JSONRenderer):
    """After encapsulation, final the JSON format:

    ```
    {
        "code": "1"
        "serialno": "fb27c9b3-a017-4ef1-98ed-75c1fcf11232_8AAOLD_cf9752dc-b947-4ede-97c0-f3eda24b87b9",
        "msg": "success",
        "data": {
            ...
        }
    }
    ```

    """

    def wrap(self, data: dict) -> dict:
        serialno = unique_id()
        rs = ResponseSchema(code='1', serialno=serialno, msg='success', data=data)
        return rs._asdict()

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        response: Response = renderer_context['response']
        if not response.exception:
            data = self.wrap(data)

        resp = super().render(data, accepted_media_type, renderer_context)
        # logger.info(resp.decode('utf-8'))
        return resp