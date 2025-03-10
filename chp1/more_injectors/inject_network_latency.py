
import time
import subprocess
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl

class NetworkLatencyInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()

    def inject_network_latency(self, pod_names: list[str], delay: int):
        """Inject artificial network latency into specified pods."""
        print(f"Injecting network latency of {delay}ms into pods: {pod_names}")
        
        # Iterate over each pod and add network latency using tc (traffic control)
        for pod in pod_names:
            add_latency_command = (
                f"kubectl exec -it {pod} -n {self.namespace} -- "
                f"tc qdisc add dev eth0 root netem delay {delay}ms"
            )
            try:
                result = self.kubectl.exec_command(add_latency_command)
                print(f"Injected latency into {pod}: {result}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to inject latency into {pod}: {e}")

        time.sleep(3)

    def recover_network_latency(self, pod_names: list[str]):
        """Remove artificial network latency from specified pods."""
        print(f"Removing network latency from pods: {pod_names}")
        
        # Iterate over each pod and remove network latency using tc (traffic control)
        for pod in pod_names:
            remove_latency_command = (
                f"kubectl exec -it {pod} -n {self.namespace} -- "
                "tc qdisc del dev eth0 root netem"
            )
            try:
                result = self.kubectl.exec_command(remove_latency_command)
                print(f"Removed latency from {pod}: {result}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove latency from {pod}: {e}")

if __name__ == "__main__":
    namespace = "test-namespace"
    pods = ["pod-1", "pod-2"]  # replace with your pod names
    latency = 100  # latency in milliseconds
    print("Start injecting/recovering network latency...")
    
    injector = NetworkLatencyInjector(namespace)
    injector.inject_network_latency(pods, latency)
    # Uncomment the following line to test recovery
    # injector.recover_network_latency(pods)
