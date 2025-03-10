
import time
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl

class DatabaseConnectionTimeoutInjector(FaultInjector):
    def __init__(self, namespace: str, timeout_duration: int):
        self.namespace = namespace
        self.timeout_duration = timeout_duration
        self.kubectl = KubeCtl()

    def inject_timeout(self, microservices: list[str]):
        """Injects a fault by causing database queries to time out."""
        for service in microservices:
            print(f"Injecting database connection timeout for {service}")
            # Get the deployment associated with the service
            deployment = self.kubectl.get_deployment(service, self.namespace)
            if deployment:
                # Assume the service may support an environment variable to simulate timeouts
                for container in deployment.spec.template.spec.containers:
                    if "DB_CONNECTION_TIMEOUT" in container.env:
                        original_timeout = container.env["DB_CONNECTION_TIMEOUT"].value
                        container.env["DB_CONNECTION_TIMEOUT"].value = str(self.timeout_duration)
                    else:
                        container.env.append({
                            "name": "DB_CONNECTION_TIMEOUT",
                            "value": str(self.timeout_duration)
                        })
                self.kubectl.update_deployment(service, self.namespace, deployment)
                time.sleep(10)

    def recover_timeout(self, microservices: list[str]):
        for service in microservices:
            print(f"Recovering database connection timeout for {service}")
            deployment = self.kubectl.get_deployment(service, self.namespace)
            if deployment:
                for container in deployment.spec.template.spec.containers:
                    # Remove the timeout environment variable or reset to the original value
                    container.env = [
                        env for env in container.env if env.name != "DB_CONNECTION_TIMEOUT"
                    ]
                self.kubectl.update_deployment(service, self.namespace, deployment)

if __name__ == "__main__":
    namespace = "test-hotel-reservation"
    microservices = ["mongodb-geo"]
    timeout_duration = 30  # Timeout duration in seconds
    print("Start injection/recovery ...")
    injector = DatabaseConnectionTimeoutInjector(namespace, timeout_duration)
    injector.inject_timeout(microservices)
    # injector.recover_timeout(microservices)
