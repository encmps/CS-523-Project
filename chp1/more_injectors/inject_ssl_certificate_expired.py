
import subprocess
from aiopslab.generators.fault.base import FaultInjector
from aiopslab.service.kubectl import KubeCtl


class SSLCertificateExpiredFaultInjector(FaultInjector):
    def __init__(self, namespace: str, certificate_path: str, expired_certificate_path: str):
        self.namespace = namespace
        self.kubectl = KubeCtl()
        self.certificate_path = certificate_path
        self.expired_certificate_path = expired_certificate_path

    def inject_ssl_certificate_expired(self, service_name: str):
        command = f"kubectl get secret {service_name}-tls -n {self.namespace} -o json"
        try:
            output = self.kubectl.exec_command(command)
            secret = json.loads(output)
        except subprocess.CalledProcessError:
            raise ValueError(f"Secret '{service_name}-tls' not found in namespace '{self.namespace}'.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON for Secret '{service_name}-tls'.")

        # Replacing with expired certificate
        with open(self.expired_certificate_path, "r") as file:
            expired_certificate = file.read()

        secret["data"]["tls.crt"] = expired_certificate.encode('base64').rstrip()
        self.kubectl.create_or_update_secret(f"{service_name}-tls", self.namespace, secret)
        print(f"Injected expired SSL certificate for service '{service_name}'.")

    def recover_ssl_certificate_expired(self, service_name: str):
        command = f"kubectl get secret {service_name}-tls -n {self.namespace} -o json"
        try:
            output = self.kubectl.exec_command(command)
            secret = json.loads(output)
        except subprocess.CalledProcessError:
            raise ValueError(f"Secret '{service_name}-tls' not found in namespace '{self.namespace}'.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON for Secret '{service_name}-tls'.")

        # Reverting to valid certificate
        with open(self.certificate_path, "r") as file:
            valid_certificate = file.read()

        secret["data"]["tls.crt"] = valid_certificate.encode('base64').rstrip()
        self.kubectl.create_or_update_secret(f"{service_name}-tls", self.namespace, secret)
        print(f"Recovered SSL certificate for service '{service_name}'.")

def main():
    namespace = "your-namespace"
    service_name = "your-service-name"
    certificate_path = "/path/to/valid/certificate.crt"
    expired_certificate_path = "/path/to/expired/certificate.crt"

    injector = SSLCertificateExpiredFaultInjector(namespace, certificate_path, expired_certificate_path)
    injector.inject_ssl_certificate_expired(service_name)
    # Run recovery when needed
    # injector.recover_ssl_certificate_expired(service_name)

if __name__ == "__main__":
    main()
