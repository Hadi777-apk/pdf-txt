"""ServerConfiguration data model for server configuration information."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class ServiceStatus(Enum):
    """Enumeration for service status values."""
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    UNKNOWN = "unknown"
    STARTING = "starting"
    STOPPING = "stopping"


@dataclass
class ServerConfiguration:
    """
    Data model for storing server configuration information.
    
    Attributes:
        service_name: Name of the web service (e.g., nginx, apache, httpd)
        binding_address: IP address the service is bound to (e.g., 127.0.0.1, 0.0.0.0)
        listening_ports: List of ports the service is listening on
        configuration_file_path: Path to the service configuration file
        status: Current status of the service
        last_modified: When the configuration was last modified
        backup_path: Path to configuration backup file (if created)
    """
    service_name: str
    binding_address: str
    listening_ports: List[int]
    configuration_file_path: str
    status: ServiceStatus
    last_modified: datetime
    backup_path: Optional[str] = None
    
    def is_localhost_only(self) -> bool:
        """Check if the service is bound only to localhost."""
        localhost_addresses = ["127.0.0.1", "::1", "localhost"]
        return self.binding_address in localhost_addresses
    
    def is_accessible_externally(self) -> bool:
        """Check if the service is configured to accept external connections."""
        external_addresses = ["0.0.0.0", "::", "*"]
        return self.binding_address in external_addresses
    
    def has_web_ports(self) -> bool:
        """Check if the service is listening on standard web ports."""
        web_ports = [80, 443, 8080, 8443]
        return any(port in web_ports for port in self.listening_ports)
    
    def is_running(self) -> bool:
        """Check if the service is currently running."""
        return self.status == ServiceStatus.RUNNING
    
    def needs_external_binding(self) -> bool:
        """Check if the service needs to be reconfigured for external access."""
        return self.is_localhost_only() and not self.is_accessible_externally()
    
    def to_dict(self) -> dict:
        """Convert the server configuration to a dictionary."""
        return {
            "service_name": self.service_name,
            "binding_address": self.binding_address,
            "listening_ports": self.listening_ports,
            "configuration_file_path": self.configuration_file_path,
            "status": self.status.value,
            "last_modified": self.last_modified.isoformat(),
            "backup_path": self.backup_path
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ServerConfiguration':
        """Create a ServerConfiguration from a dictionary."""
        return cls(
            service_name=data["service_name"],
            binding_address=data["binding_address"],
            listening_ports=data["listening_ports"],
            configuration_file_path=data["configuration_file_path"],
            status=ServiceStatus(data["status"]),
            last_modified=datetime.fromisoformat(data["last_modified"]),
            backup_path=data.get("backup_path")
        )