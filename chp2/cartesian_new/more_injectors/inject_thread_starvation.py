
import time
from threading import Thread, Lock
from aiopslab.generators.fault.base import FaultInjector

class ThreadStarvationFaultInjector(FaultInjector):
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.lock = Lock()
        self.threads = []

    def inject_thread_starvation(self):
        """Injects a fault that causes thread starvation, leading to unresponsiveness."""
        for i in range(10):  # Creating 10 threads that will simulate a lock
            thread = Thread(target=self.locked_function, args=(i,))
            self.threads.append(thread)
            thread.start()
        print("Injected thread starvation fault by locking critical threads.")

    def locked_function(self, thread_id: int):
        """Function that simulates a blocked thread by acquiring a lock and sleeping."""
        with self.lock:
            print(f"Thread {thread_id} acquired the lock and is simulating work.")
            time.sleep(30)  # Simulate long work period
        print(f"Thread {thread_id} released the lock.")

    def recover_thread_starvation(self):
        """Attempts to recover from the thread starvation by terminating all threads."""
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)  # Wait briefly for thread to complete
        print("Recovered from thread starvation, all threads completed.")

if __name__ == "__main__":
    namespace = "test-namespace"
    injector = ThreadStarvationFaultInjector(namespace)
    try:
        injector.inject_thread_starvation()
        time.sleep(60)  # Let the fault simulate for a while
    finally:
        injector.recover_thread_starvation()
