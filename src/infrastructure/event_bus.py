from typing import Callable, Type, Dict, List
import threading

class EventBus:
    def __init__(self):
        self._handlers: Dict[Type, List[Callable]] = {}

    def subscribe(self, event_type: Type, handler: Callable) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event) -> None:
        for handler in self._handlers.get(type(event), []):
            thread = threading.Thread(target=handler, args=(event,))
            thread.daemon = True
            thread.start()
