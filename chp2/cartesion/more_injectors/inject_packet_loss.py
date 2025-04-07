
import subprocess
import time
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl

class PacketLossFaultInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()

    def inject_packet_loss(self, microservices: list[str], loss_percentage: int):
        """Inject a fault by dropping a percentage of network packets."""
        pods = self.kubectl.list_pods(self.namespace)
        target_pods = [
            pod.metadata.name
            for pod in pods.items
            if any(service in pod.metadata.name for service in microservices)
        ]

        print(f"Target Pods for packet loss injection: {target_pods}")

        for pod in target_pods:
            # Adding iptables rule to drop a percentage of packets
            packet_loss_command = (
                f"kubectl exec -it {pod} -n {self.namespace} -- "
                f"/bin/sh -c 'tc qdisc add dev eth0 root netem loss {loss_percentage}%'"
            )
            try:
                result = self.kubectl.exec_command(packet_loss_command)
                print(f"Packet loss injection result for {pod}: {result}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to inject packet loss on {pod}: {e}")

    def recover_packet_loss(self, microservices: list[str]):
        """Recover from packet loss by removing iptables rules."""
        pods = self.kubectl.list_pods(self.namespace)
        target_pods = [
            pod.metadata.name
            for pod in pods.items
            if any(service in pod.metadata.name for service in microservices)
        ]

        print(f"Target Pods for packet loss recovery: {target_pods}")

        for pod in target_pods:
            # Removing iptables rule
            recover_command = (
                f"kubectl exec -it {pod} -n {self.namespace} -- "
                f"/bin/sh -c 'tc qdisc del dev eth0 root netem'"
            )
            try:
                result = self.kubectl.exec_command(recover_command)
                print(f"Packet loss recovery result for {pod}: {result}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to recover packet loss on {pod}: {e}")


if __name__ == "__main__":
    namespace = "test-hotel-reservation"
    microservices = ["geo", "rate"]
    fault_type = "packet_loss"
    loss_percentage = 10  # Specify the percentage of packet loss

    injector = PacketLossFaultInjector(namespace)
    print("Start injection ...")
    injector.inject_packet_loss(microservices, loss_percentage)
    time.sleep(30)  # Let the fault run for some time
    print("Start recovery ...")
    injector.recover_packet_loss(microservices)
