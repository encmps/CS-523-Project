
import subprocess
import time
from aiopslab.generators.fault.base import FaultInjector


class HighIOWaitFaultInjector(FaultInjector):
    def __init__(self, duration: int = 60, block_size: int = 512, count: int = 1024):
        """
        Initialize the HighIOWaitFaultInjector with parameters to control the fault injection.
        
        :param duration: Duration to maintain the high I/O wait condition in seconds.
        :param block_size: The block size in bytes for the high I/O operation.
        :param count: The number of 512-byte blocks to be written to the disk for simulating high I/O.
        """
        self.duration = duration
        self.block_size = block_size
        self.count = count

    def inject_high_io_wait(self):
        """
        Injects high I/O wait by performing a large number of read/write operations to disk.
        """
        print(f"Starting high I/O wait injection for {self.duration} seconds...")

        try:
            # Use 'dd' command to write large data to disk, simulating high I/O wait
            command = [
                "sudo", "dd", "if=/dev/zero", "of=/tmp/testfile",
                f"bs={self.block_size}", f"count={self.count}"
            ]
            subprocess.Popen(command)
            
            print(f"Sleeping for {self.duration} seconds to simulate high I/O wait...")
            time.sleep(self.duration)

        except subprocess.CalledProcessError as e:
            print(f"Failed to inject high I/O wait: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """
        Clean up after fault injection by removing the generated test file.
        """
        try:
            print("Cleaning up test artifacts...")
            subprocess.run(["sudo", "rm", "-f", "/tmp/testfile"], check=True)
            print("Cleanup successful.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clean up: {e}")

    def recover_high_io_wait(self):
        """
        Recovers from the high I/O wait condition.
        """
        print("Recovery from high I/O wait is typically as simple as cleanup.")
        self.cleanup()


if __name__ == "__main__":
    injector = HighIOWaitFaultInjector(duration=60, block_size=512, count=1024)
    injector.inject_high_io_wait()
