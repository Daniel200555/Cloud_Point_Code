import time

from config.models import UnitConfig
from config.loader import ConfigLoader
from gitlab_client.client import GitLabClient
from controller.worker_manager import WorkerManager
from queue_to_update.queue_manager import QueueManager

class Controller:

    def __init__(self):
        self.worker_manager = WorkerManager()
        self.git_lab_client = GitLabClient()
        self.config_loader = ConfigLoader()
        self.queue_manager = QueueManager()

    def run(self) -> None:
        while True:
            if self.worker_manager.workers == self.worker_manager.cpu_count:
                pass;
            # add her put data for upgrade from state xlsx units
            self.worker_manager.reconcile(self.sync_config())#only for this time
            time.sleep(300)
                            

    def sync_config(self) -> list[UnitConfig]:
        result: list[UnitConfig] = []
        for data in self.git_lab_client.get_unit_files():
            result.append(self.config_loader.load(data))
        return result
