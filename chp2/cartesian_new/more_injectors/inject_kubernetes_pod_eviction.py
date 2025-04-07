
import subprocess
import time
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl

class KubernetesPodEvictionInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()

    def inject_pod_eviction(self, pod_name: str):
        """Inject a fault to evict a Kubernetes Pod."""
        print(f"Starting eviction of pod {pod_name} in namespace {self.namespace}.")
        
        # Evict the pod using kubectl
        evict_command = (
            f"kubectl delete pod {pod_name} -n {self.namespace} --grace-period=0 --force"
        )
        try:
            result = self.kubectl.exec_command(evict_command)
            print(f"Eviction result: {result}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to evict pod {pod_name}: {e}")

    def recover_pod_eviction(self, pod_name: str):
        """Recover from the pod eviction fault by waiting for a pod to be rescheduled."""
        print(f"Checking if pod {pod_name} is rescheduled in namespace {self.namespace}.")
        
        # Wait until the pod is rescheduled
        while True:
            pods = self.kubectl.list_pods(self.namespace)
            if any(pod.metadata.name == pod_name for pod in pods.items):
                print(f"Pod {pod_name} has been rescheduled.")
                break
            else:
                print(f"Pod {pod_name} is not yet rescheduled. Waiting...")
                time.sleep(5)

def main():
    namespace = "default"  # specify your namespace
    pod_name = "example-pod"  # specify the pod name to evict

    injector = KubernetesPodEvictionInjector(namespace)
    injector.inject_pod_eviction(pod_name)

if __name__ == "__main__":
    main()
