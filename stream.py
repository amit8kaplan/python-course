
import threading
from queue import Queue


class Stream:
    def __init__(self):
        self._queue = Queue()
        self._thread = threading.Thread(target=self._process)
        self._action = None
        self._stop = False
        self._result_stream = None

        # start thread
        self._thread.start()

    def add(self, item):
        self._queue.put(item)

        # start processing if action and queue are not empty
        if self._action and not self._queue.empty():
            self._process_item()

    def apply(self, action):
        def stream_action(x):
            result = action(x)
            if result is True:
                self._result_stream.add(x)
            elif result is not None:
                self._result_stream.add(result)

        self._result_stream = Stream()
        self._result_stream._action = stream_action
        return self._result_stream

    def forEach(self, action):
        self._action = action

        # start processing if queue is not empty
        if not self._queue.empty():
            self._process_item()

    def stop(self):
        self._stop = True

    def _process(self):
        while True:
            if self._stop:
                break

            if self._action and not self._queue.empty():
                self._process_item()
            else:
                # sleep to reduce CPU usage
                threading.Event().wait(0.1)

    def _process_item(self):
        item = self._queue.get()
        self._action(item)

        # start processing result stream if not empty
        if self._result_stream and not self._result_stream._queue.empty():
            self._result_stream._process_item()
