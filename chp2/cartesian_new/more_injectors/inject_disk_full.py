
import subprocess
import os
import tempfile
from aiopslab.generators.fault.base import FaultInjector

class DiskFullInjector(FaultInjector):
    def __init__(self, target_path="/mnt") -> None:
        """
        Initializes the DiskFullInjector with the specified target path on the node.
        
        Args:
            target_path (str): The directory path where the disk space will be filled.
                               Default is '/mnt'.
        """
        self.target_path = target_path
        self.temp_files = []

    def inject_disk_full(self) -> None:
        """
        Fills the disk space on the specified node path, preventing applications from writing logs,
        storing data, or functioning properly.
        """
        try:
            print(f"Starting disk full injection on path: {self.target_path}")

            free_space = self.get_free_space()
            print(f"Free space available initially: {free_space} bytes")

            if free_space <= 0:
                print("No free space available to fill.")
                return
                
            filled_space = 0
            while filled_space < free_space:
                # Create a large temporary file to fill disk space
                temp_file_path = os.path.join(self.target_path, next(tempfile._get_candidate_names()))
                with open(temp_file_path, 'wb') as f:
                    # Write data to fill up space in 100MB chunks
                    chunk_size = min(free_space - filled_space, 100 * 1024 * 1024)
                    data = b'0' * chunk_size
                    f.write(data)
                    filled_space += chunk_size

                self.temp_files.append(temp_file_path)
                print(f"Filled {filled_space} bytes. Remaining space: {free_space - filled_space} bytes")

            print("Disk full fault injection completed!")

        except Exception as e:
            print(f"Failed to fill disk space due to error: {e}")

    def recover_disk_full(self) -> None:
        """
        Attempts to recover from the disk space full condition by removing the temporary files.
        """
        try:
            for file in self.temp_files:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"Removed temporary file: {file}")

            self.temp_files.clear()
            print("Disk space has been reclaimed successfully.")
            
        except Exception as e:
            print(f"Failed to recover disk space due to error: {e}")

    def get_free_space(self) -> int:
        """
        Retrieves the amount of free space available on the target path.

        Returns:
            int: The available free space in bytes.
        """
        st = os.statvfs(self.target_path)
        return st.f_bavail * st.f_frsize


def main():
    injector = DiskFullInjector()
    injector.inject_disk_full()


if __name__ == "__main__":
    main()

