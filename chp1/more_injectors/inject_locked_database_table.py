
import time
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl

class LockedTableFaultInjector(FaultInjector):
    def __init__(self, namespace: str, db_name: str, table_name: str):
        self.namespace = namespace
        self.db_name = db_name
        self.table_name = table_name
        self.kubectl = KubeCtl()

    def inject_locked_table(self, microservices: list[str]):
        """Simulate a fault where a critical database table remains locked."""
        for service in microservices:
            pods = self.kubectl.list_pods(self.namespace)
            target_db_pods = [
                pod.metadata.name
                for pod in pods.items
                if service in pod.metadata.name
            ]
            print(f"Target Database Pods for locking: {target_db_pods}")

            for pod in target_db_pods:
                # Command to run a lock on the specified table
                lock_command = (
                    f"kubectl exec -it {pod} -n {self.namespace} -- "
                    f"/bin/bash -c \"psql -U postgres -d {self.db_name} -c "
                    f"'BEGIN; LOCK TABLE {self.table_name} IN ACCESS EXCLUSIVE MODE;'\""
                )
                result = self.kubectl.exec_command(lock_command)
                print(f"Lock command result for {self.table_name} in {service}: {result}")

    def recover_locked_table(self, microservices: list[str]):
        """Recover by ending the transaction, releasing the lock on the table."""
        for service in microservices:
            pods = self.kubectl.list_pods(self.namespace)
            target_db_pods = [
                pod.metadata.name
                for pod in pods.items
                if service in pod.metadata.name
            ]
            print(f"Target Database Pods for recovery: {target_db_pods}")

            for pod in target_db_pods:
                # Command to end the transaction and release the lock
                release_command = (
                    f"kubectl exec -it {pod} -n {self.namespace} -- "
                    f"/bin/bash -c \"psql -U postgres -d {self.db_name} -c 'END;'\""
                )
                result = self.kubectl.exec_command(release_command)
                print(f"Unlock command result for {self.table_name} in {service}: {result}")

if __name__ == "__main__":
    namespace = "test-namespace"
    db_name = "testdb"
    table_name = "critical_table"
    microservices = ["db-microservice"]

    print("Start injection/recovery ...")
    injector = LockedTableFaultInjector(namespace, db_name, table_name)
    
    # Choose inject or recover based on the desired action
    injector.inject_locked_table(microservices)
    # injector.recover_locked_table(microservices)
