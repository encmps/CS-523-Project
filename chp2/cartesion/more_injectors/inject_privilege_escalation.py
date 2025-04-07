
import json
import subprocess
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl


class PrivilegeEscalationFaultInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()
        self.configmap_name = f"{namespace}-user-config"

    def inject_privilege_escalation(self, target_user: str):
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

        user_data = json.loads(configmap["data"]["users.json"])

        if target_user in user_data["users"]:
            user_data["users"][target_user]["role"] = "admin"
        else:
            raise ValueError(
                f"User '{target_user}' not found in ConfigMap '{self.configmap_name}'."
            )

        updated_data = {"users.json": json.dumps(user_data, indent=2)}
        self.kubectl.create_or_update_configmap(
            self.configmap_name, self.namespace, updated_data
        )
        print(f"Privilege escalation fault injected: User '{target_user}' role set to 'admin'.")

    def recover_privilege_escalation(self, target_user: str):
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

        user_data = json.loads(configmap["data"]["users.json"])

        if target_user in user_data["users"]:
            user_data["users"][target_user]["role"] = "user"
        else:
            raise ValueError(
                f"User '{target_user}' not found in ConfigMap '{self.configmap_name}'."
            )

        updated_data = {"users.json": json.dumps(user_data, indent=2)}
        self.kubectl.create_or_update_configmap(
            self.configmap_name, self.namespace, updated_data
        )
        print(f"Privilege escalation fault recovered: User '{target_user}' role set to 'user'.")


def main():
    namespace = "example-namespace"
    target_user = "some-user"
    injector = PrivilegeEscalationFaultInjector(namespace)
    # injector.inject_privilege_escalation(target_user)
    injector.recover_privilege_escalation(target_user)


if __name__ == "__main__":
    main()
