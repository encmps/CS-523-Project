
import time
import subprocess
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl

class MemoryLeakFaultInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()

    def inject_memory_leak(self, microservices: list[str]):
        """Introduce a memory leak in the specified microservices."""
        for service in microservices:
            pods = self.kubectl.list_pods(self.namespace)
            target_pods = [
                pod.metadata.name 
                for pod in pods.items 
                if service in pod.metadata.name
            ]
            print(f"Target Pods for memory leak: {target_pods}")

            for pod in target_pods:
                # Run a script inside the pod to cause it a memory leak
                leak_command = f"kubectl exec -it {pod} -n {self.namespace} -- /bin/bash /scripts/memory-leak.sh"
                try:
                    result = self.kubectl.exec_command(leak_command)
                    print(f"Memory leak injected in {pod}: {result}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to inject memory leak into {pod}: {e}")

            time.sleep(5)  # Wait to observe the memory leak effect

    def recover_memory_leak(self, microservices: list[str]):
        """Recover from a memory leak in the specified microservices."""
        for service in microservices:
            pods = self.kubectl.list_pods(self.namespace)
            target_pods = [
                pod.metadata.name 
                for pod in pods.items 
                if service in pod.metadata.name
            ]
            print(f"Target Pods for memory leak recovery: {target_pods}")

            for pod in target_pods:
                # Run a script inside the pod to stop the memory leak
                recover_command = f"kubectl exec -it {pod} -n {self.namespace} -- /bin/bash /scripts/recover-memory-leak.sh"
                try:
                    result = self.kubectl.exec_command(recover_command)
                    print(f"Memory leak recovered in {pod}: {result}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to recover memory leak in {pod}: {e}")

if __name__ == "__main__":
    namespace = "test-namespace"
    microservices = ["example-service"]
    inject_recover = "inject"  # Choose either 'inject' or 'recover'
    
    injector = MemoryLeakFaultInjector(namespace)
    if inject_recover == "inject":
        injector.inject_memory_leak(microservices)
    elif inject_recover == "recover":
        injector.recover_memory_leak(microservices)
