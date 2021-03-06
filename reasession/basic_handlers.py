from networking import IHandler
import reapy as rpr
from common import log


class PrintHandler(IHandler):
    def can_handle(self, data_type: bytes) -> bool:
        if data_type == b'print':
            return True
        return False

    def handle(self, data_type: bytes, data: bytes) -> bytes:
        log(str(data, 'utf-8'))
        return b'success'


class PingHandler(IHandler):
    def can_handle(self, data_type: bytes) -> bool:
        if data_type == b'ping':
            return True
        return False

    def handle(self, data_type: bytes, data: bytes) -> bytes:
        log(str(data, 'utf-8'))
        return b'success'
