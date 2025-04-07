
import json
import subprocess
import random
import string
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl


class ConfigFileFaultInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()
        self.configmap_name = f"{namespace}-config"

    def inject_corrupt_configuration(self, config_key: str):
        command = (
            f"kubectl get configmap {self.configmap_name} -n {self.namespace} -o json"
        )
        try:
            output = self.kubectl.exec_command(command)
            configmap = json.loads(output)
        except subprocess.CalledProcessError:
            raise ValueError(
                f"ConfigMap '{self.configmap_name}' not found in namespace '{self.namespace}'."
            )
        except json.JSONDecodeError:
            raise ValueError(
                f"Error decoding JSON for ConfigMap '{self.configmap_name}'."
            )

        if config_key in configmap["data"]:
            original_data = configmap["data"][config_key]
            corrupted_data = self._corrupt_data(original_data)
            configmap["data"][config_key] = corrupted_data
        else:
            raise ValueError(
                f"Configuration key '{config_key}' not found in ConfigMap '{self.configmap_name}'."
            )

        self.kubectl.create_or_update_configmap(
            self.configmap_name, self.namespace, configmap["data"]
        )
        print(f"Fault injected: Configuration file '{config_key}' corrupted.")

    def recover_corrupt_configuration(self, config_key: str):
        # To recover, we need the original, this assumes we have some backup/restore process
        # For simplicity, we'll just 'undo' the corruption process, which may not be realistic in real scenarios.
        print(f"Recovery for corrupted configuration on key '{config_key}' is not implemented.")
        # This would usually involve rolling back or reapplying the original config

    @staticmethod
    def _corrupt_data(data: str) -> str:
        # Simple corruption by introducing random noise in the data
        noise = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        corrupted_data = data + noise
        return corrupted_data


def main():
    namespace = "test-namespace"
    config_key = "critical-config.json"
    injector = ConfigFileFaultInjector(namespace)
    injector.inject_corrupt_configuration(config_key)


if __name__ == "__main__":
    main()
