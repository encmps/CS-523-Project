
import time
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl


class LogFloodingFaultInjector(FaultInjector):
    def __init__(self, namespace: str, target_microservices: list[str], flooding_duration: int = 60):
        self.namespace = namespace
        self.target_microservices = target_microservices
        self.flooding_duration = flooding_duration  # Duration in seconds
        self.kubectl = KubeCtl()

    def inject_log_flooding(self):
        """Inject a log flooding fault to overwhelm logging systems."""
        print(f"Starting log flooding for microservices: {self.target_microservices}")
        pods = self.kubectl.list_pods(self.namespace)

        for service in self.target_microservices:
            target_pods = [
                pod.metadata.name
                for pod in pods.items
                if service in pod.metadata.name
            ]
            print(f"Target Pods for log flooding: {target_pods}")

            for pod in target_pods:
                flood_command = f"kubectl exec -it {pod} -n {self.namespace} -- /bin/bash -c 'for i in {{1..10000}}; do echo \"Flooding logs...\"; done'"
                result = subprocess.Popen(flood_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Let the flooding continue for the specified duration
                time.sleep(self.flooding_duration)
                result.kill()
                print(f"Completed log flooding for {pod}")

        print("Log flooding fault injection complete.")

    def recover_log_flooding(self):
        """
        Since the log flooding fault is time-based and we kill the flood process
        after the duration, there might not be additional recovery needed beyond
        what's executed in the `inject_log_flooding` method.
        """
        print("Recovery typically not needed beyond stopping log generation.")
        # In a real-world setup, this would involve cleaning up or resetting logging systems


if __name__ == "__main__":
    namespace = "test-namespace"
    target_microservices = ["service1", "service2"]
    flooding_duration = 60  # Log flooding for 60 seconds

    print("Start injection/recovery of log flooding...")
    injector = LogFloodingFaultInjector(namespace, target_microservices, flooding_duration)
    injector.inject_log_flooding()
    # Since recovery might not be necessary, this is just for completeness
    injector.recover_log_flooding()
