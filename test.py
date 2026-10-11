from gitlab_client.client import GitLabClient
from controller.controller import Controller
import os
import psutil

print("Logical CPUs:", os.cpu_count())
print("Available CPUs:", psutil.Process().cpu_affinity())
print("Physical cores:", psutil.cpu_count(logical=False))
print("Logical cores:", psutil.cpu_count(logical=True))
# print(Controller().sync_config())

# print([yaml.getvalue() for yaml in GitLabClient().get_unit_files()])