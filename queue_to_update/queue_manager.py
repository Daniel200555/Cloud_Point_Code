from queue import Queue
from config.models import UnitConfig

class QueueManager:
    def __init__(self):
        self.queue = Queue(UnitConfig)

    def add_to_queue(self, unit_config: UnitConfig):
        self.queue.put(unit_config)

    def get_from_queue(self, unit_config: UnitConfig):
        self.queue.get(unit_config)


# if "Apple" in my_queue.queue: