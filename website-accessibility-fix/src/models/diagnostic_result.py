"""DiagnosticResult data model for network diagnostic results."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class ConnectionStatus(Enum):
    """Enumeration for connection status values."""
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    REFUSED = "refused"
    UNREACHABLE = "unreachable"
    UNKNOWN = "unknown"


@dataclass
class DiagnosticResult:
    """
    Data model for storing network diagnostic test results.
    
    Attributes:
        timestamp: When the diagnostic test was performed
        test_type: Type of diagnostic test (ping, port_scan, traceroute, dns)
        source_location: Location/identifier of the testing source
        target_ip: IP address of the target server
        status: Connection status result
        response_time: Response time in milliseconds (None if failed)
        error_details: Detailed error message if test failed
        recommendations: List of recommended actions based on results
    """
    timestamp: datetime
    test_type: str
    source_location: str
    target_ip: str
    status: ConnectionStatus
    response_time: Optional[float] = None
    error_details: Optional[str] = None
    recommendations: Optional[List[str]] = None
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.recommendations is None:
            self.recommendations = []
    
    def is_successful(self) -> bool:
        """Check if the diagnostic test was successful."""
        return self.status == ConnectionStatus.SUCCESS
    
    def add_recommendation(self, recommendation: str) -> None:
        """Add a recommendation to the result."""
        if self.recommendations is None:
            self.recommendations = []
        self.recommendations.append(recommendation)
    
    def to_dict(self) -> dict:
        """Convert the diagnostic result to a dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "test_type": self.test_type,
            "source_location": self.source_location,
            "target_ip": self.target_ip,
            "status": self.status.value,
            "response_time": self.response_time,
            "error_details": self.error_details,
            "recommendations": self.recommendations or []
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DiagnosticResult':
        """Create a DiagnosticResult from a dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            test_type=data["test_type"],
            source_location=data["source_location"],
            target_ip=data["target_ip"],
            status=ConnectionStatus(data["status"]),
            response_time=data.get("response_time"),
            error_details=data.get("error_details"),
            recommendations=data.get("recommendations", [])
        )