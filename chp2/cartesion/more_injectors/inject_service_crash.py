
import time
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl


class ServiceCrashFaultInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()

    def inject_service_crash(self, microservices: list[str]):
        """Force a service or application to crash unexpectedly."""
        for service in microservices:
            print(f"Forcing crash for service: {service}")
            pods = self.kubectl.list_pods(self.namespace)

            # Find the pods for the specified service
            target_pods = [
                pod.metadata.name
                for pod in pods.items
                if service in pod.metadata.labels.get("app", "")
            ]
            print(f"Target Pods for crash: {target_pods}")

            # Crash the service by killing the pods
            for pod in target_pods:
                crash_command = f"kubectl exec -it {pod} -n {self.namespace} -- /bin/bash -c 'kill 1'"
                result = self.kubectl.exec_command(crash_command)
                print(f"Forced crash for pod {pod}: {result}")

            time.sleep(3)  # Give some time for the crash to propagate

    def recover_service(self, microservices: list[str]):
        """Recover service by redeploying crashed pods."""
        for service in microservices:
            pods = self.kubectl.list_pods(self.namespace)

            # Find the pods for the specified service
            target_pods = [
                pod.metadata.name
                for pod in pods.items
                if service in pod.metadata.labels.get("app", "")
            ]
            print(f"Target Pods for recovery: {target_pods}")

            # In Kubernetes, crashing a pod usually cause automatic recovery
            # Delete the pods to ensure they are restarted
            for pod in target_pods:
                delete_command = f"kubectl delete pod {pod} -n {self.namespace}"
                result = self.kubectl.exec_command(delete_command)
                print(f"Pod {pod} deleted to recover service: {result}")

            time.sleep(10)  # Wait for the pods to be restarted


if __name__ == "__main__":
    namespace = "test-namespace"
    microservices = ["example-service"]
    fault_type = "service_crash"

    print("Start injecting or recovering fault...")
    injector = ServiceCrashFaultInjector(namespace)
    # Uncomment one of the following lines to simulate injection or recovery
    # injector.inject_service_crash(microservices)
    # injector.recover_service(microservices)
