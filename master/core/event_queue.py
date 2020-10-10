from queue import Queue


class EventQueue():
    _event_queue = Queue()

    @classmethod
    def push_event(cls, event):
        cls._event_queue.put(block=False)

    @classmethod
    def pop_event(cls):
        return cls._event_queue.get(block=True)
