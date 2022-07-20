"""pub_sub_receive.py -- receive OpenCV stream using PUB SUB."""

import sys
import traceback
import datazmq
import threading
import time
import json

# Helper class implementing an IO deamon thread
class JSONStreamSubscriber:

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self._stop = False
        self._data_ready = threading.Event()
        self._thread = threading.Thread(target=self._run, args=())
        self._thread.daemon = True
        self._thread.start()

    def receive(self, timeout=15.0):
        flag = self._data_ready.wait(timeout=timeout)
        if not flag:
            raise TimeoutError(
                "Timeout while reading from subscriber tcp://{}:{}".format(self.hostname, self.port))
        self._data_ready.clear()
        return self._data

    def _run(self):
        receiver = datazmq.JSONHub("tcp://{}:{}".format(self.hostname, self.port), REQ_REP=False)
        while not self._stop:
            self._data = receiver.recv_json()
            # self._data = json.loads(self._data)
            self._data_ready.set()
        receiver.close()

    def close(self):
        self._stop = True

