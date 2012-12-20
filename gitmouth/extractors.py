import json

from twisted.internet.protocol import Protocol


class BuildServerExtractor(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.collected = ''

    def dataReceived(self, bytes):
        self.collected += bytes

    def connectionLost(self, reason):
        payload = json.loads(self.collected)
        self.finished.callback(payload)


class UserExtractor(Protocol):
    def __init__(self, finished, key_fingerprint, credentials):
        self.finished = finished
        self.credentials = credentials
        self.collected = ''
        self.key_fingerprint = key_fingerprint

    def dataReceived(self, bytes):
        self.collected += bytes

    def connectionLost(self, reason):
        parts = self.collected.split(':')
        self.credentials.username = '%s:%s' % (parts[1], self.key_fingerprint)
        self.finished.callback(True)
