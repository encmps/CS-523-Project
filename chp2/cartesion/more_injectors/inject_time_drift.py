
import subprocess
import time
from aiopslab.generators.fault.base import FaultInjector


class TimeDriftFaultInjector(FaultInjector):
    def __init__(self):
        pass

    def inject_time_drift(self, offset_seconds: int):
        """
        Injects a time drift by offsetting the system clock by a specified number of seconds.
        
        :param offset_seconds: The number of seconds by which the system clock will be offset.
        """
        try:
            # Display the current time
            print("Current system time before drift:")
            subprocess.run(["date"])

            # Offset the system clock
            drift_command = f"sudo date -s @$(($(date +%s) + {offset_seconds}))"
            print(f"Injecting time drift with command: {drift_command}")
            subprocess.run(drift_command, shell=True, check=True)

            # Confirm the time offset
            print("System time after drift:")
            subprocess.run(["date"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to inject time drift: {e}")

    def recover_time_drift(self):
        """
        Recovers the system time by synchronizing with the network time protocol (NTP).
        """
        try:
            # Attempt to synchronize time with NTP
            print("Recovering system time using NTP synchronization.")
            subprocess.run(["sudo", "ntpdate", "-u", "pool.ntp.org"], check=True)

            # Confirm the resynchronization
            print("System time after recovery:")
            subprocess.run(["date"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to recover system time: {e}")


def main():
    injector = TimeDriftFaultInjector()
    # Example: Inject a time drift of 120 seconds (2 minutes)
    injector.inject_time_drift(120)
    time.sleep(10)  # Simulate waiting period for demonstration purposes
    injector.recover_time_drift()


if __name__ == "__main__":
    main()
