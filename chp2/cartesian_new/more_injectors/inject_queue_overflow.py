
import json
import time
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl

class QueueOverflowInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()
        self.queue_service_name = f"{namespace}-queue-service"

    def inject_queue_overflow(self):
        print("Starting queue overflow injection...")
        pods = self.kubectl.list_pods(self.namespace)
        
        # Identify queue-related pods
        queue_pods = [
            pod.metadata.name
            for pod in pods.items
            if "queue" in pod.metadata.name or "eventbus" in pod.metadata.name
        ]
        print(f"Identified queue pods: {queue_pods}")

        for pod in queue_pods:
            try:
                # Overload the queue by sending a burst of messages
                send_command = f"kubectl exec -it {pod} -n {self.namespace} -- /bin/bash /scripts/queue_overload.sh"
                result = self.kubectl.exec_command(send_command)
                print(f"Queue overload result for {pod}: {result}")
            except Exception as e:
                print(f"Failed to overload queue in pod {pod}: {e}")

    def recover_queue_overflow(self):
        print("Starting queue overflow recovery...")
        pods = self.kubectl.list_pods(self.namespace)
        
        # Identify queue-related pods
        queue_pods = [
            pod.metadata.name
            for pod in pods.items
            if "queue" in pod.metadata.name or "eventbus" in pod.metadata.name
        ]
        print(f"Identified queue pods for recovery: {queue_pods}")

        for pod in queue_pods:
            try:
                # Clear the queue by executing a cleanup script
                clear_command = f"kubectl exec -it {pod} -n {self.namespace} -- /bin/bash /scripts/queue_clear.sh"
                result = self.kubectl.exec_command(clear_command)
                print(f"Queue clear result for {pod}: {result}")
            except Exception as e:
                print(f"Failed to clear queue in pod {pod}: {e}")

def main():
    namespace = "my-namespace"
    injector = QueueOverflowInjector(namespace)
    print("Injecting queue overflow fault...")
    injector.inject_queue_overflow()
    time.sleep(10)  # Keep the fault for 10 seconds
    print("Recovering from queue overflow fault...")
    injector.recover_queue_overflow()

if __name__ == "__main__":
    main()
