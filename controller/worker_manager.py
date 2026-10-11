import os
import psutil
from queue import Queue, Empty
from multiprocessing import Process
from config.models import UnitConfig
from worker.unit_worker import Worker

class WorkerManager:

    def __init__(self):
        self.workers: dict[str, Process] = {}
        self.queue: Queue[UnitConfig] = Queue()
        self.queued_names: set[str] = set()
        self.cpu_count = os.cpu_count() or 1
        self.available_cpus = psutil.Process().cpu_affinity()
        if not self.available_cpus:
            raise RuntimeError("No available CPUs")

        self.max_workers = max(1, min(self.cpu_count - 2, len(self.available_cpus)))

    def reconcile(self, configs: list[UnitConfig]) -> None:
        for config in configs:
            name = config.unit_name
            process = self.workers.get(name)
            if process is not None and process.is_alive():
                continue

            if process is not None:
                process.join()
                self._report_exit(name, process)
                del self.workers[name]

            self._enqueue(config)

        self.dispatch()

    def dispatch(self) -> None:
        for name, process in list(self.workers.items()):
            if process.is_alive():
                continue

            process.join()
            self._report_exit(name, process)
            del self.workers[name]

        while len(self.workers) < self.max_workers:
            try:
                config = self.queue.get_nowait()
            except Empty:
                break

            self.queued_names.discard(config.unit_name)
            self.start_worker(config)

    def start_worker(self, unit_config: UnitConfig) -> None:
        name = unit_config.unit_name
        if name in self.workers:
            if self.workers[name].is_alive():
                return
            old_process = self.workers.pop(name)
            old_process.join()
            self._report_exit(name, old_process)
        if len(self.workers) >= self.max_workers:
            self._enqueue(unit_config)
            return
        cpu_index = len(self.workers) % len(self.available_cpus)
        cpu_id = self.available_cpus[cpu_index]
        process = Process(
            target=self._run_worker,
            args=(unit_config, cpu_id),
            name=f"worker-{name}",
        )
        process.start()
        self.workers[name] = process
        print(
            f"Started: {name} | "
            f"PID: {process.pid} | CPU: {cpu_id}"
        )

    def stop_worker(self, unit_config: UnitConfig) -> None:
        name = unit_config.unit_name
        self._remove_queued(name)
        process = self.workers.get(name)
        if process is None:
            return
        if process.is_alive():
            process.terminate()
            process.join()
        del self.workers[name]
        print(f"Stopped worker: {name}")

    def restart_worker(self, unit_config: UnitConfig) -> None:
        self.stop_worker(unit_config)
        self._enqueue(unit_config)
        self.dispatch()
        print(f"Restart requested: {unit_config.unit_name}")

    def _enqueue(self, config: UnitConfig) -> None:
        name = config.unit_name
        if name in self.queued_names:
            return
        process = self.workers.get(name)
        if process is not None and process.is_alive():
            return
        self.queue.put(config)
        self.queued_names.add(name)

    def _remove_queued(self, name: str) -> None:
        remaining = []
        while True:
            try:
                config = self.queue.get_nowait()
            except Empty:
                break
            if config.unit_name != name:
                remaining.append(config)
        for config in remaining:
            self.queue.put(config)
        self.queued_names = {
            config.unit_name for config in remaining
        }

    @staticmethod
    def _report_exit(name: str, process: Process) -> None:
        if process.exitcode == 0:
            print(f"Worker {name} completed successfully.")
        else:
            print(
                f"Worker {name} failed. "
                f"Exit code: {process.exitcode}"
            )

    @staticmethod
    def _run_worker( unit_config: UnitConfig, cpu_id: int):
        process = psutil.Process(os.getpid())
        process.cpu_affinity([cpu_id])

        print(f"Logic started: {unit_config.unit_name}")
        worker = Worker()
        worker.share_point()


        