"""TestResult data model for comprehensive testing results."""

from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class TestType(Enum):
    """Enumeration for test type values."""
    ACCESSIBILITY = "accessibility"
    LOAD = "load"
    CROSS_PLATFORM = "cross_platform"
    REGRESSION = "regression"
    SECURITY = "security"
    PERFORMANCE = "performance"
    NETWORK_LOCATION = "network_location"


@dataclass
class TestResult:
    """
    Data model for storing comprehensive test results.
    
    Attributes:
        test_id: Unique identifier for the test
        test_type: Type of test performed
        source_device: Device/platform used for testing
        source_network: Network location of the test source
        target_url: URL that was tested
        success: Whether the test was successful
        response_code: HTTP response code received
        response_time: Response time in milliseconds
        error_message: Error message if test failed
        timestamp: When the test was performed
    """
    test_id: str
    test_type: TestType
    source_device: str
    source_network: str
    target_url: str
    success: bool
    response_code: Optional[int] = None
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def is_http_success(self) -> bool:
        """Check if the HTTP response indicates success."""
        return self.response_code is not None and 200 <= self.response_code < 300
    
    def is_connection_refused(self) -> bool:
        """Check if the test failed due to connection refused."""
        return (
            not self.success and
            self.error_message is not None and
            "connection refused" in self.error_message.lower()
        )
    
    def is_timeout(self) -> bool:
        """Check if the test failed due to timeout."""
        return (
            not self.success and
            self.error_message is not None and
            "timeout" in self.error_message.lower()
        )
    
    def get_performance_category(self) -> str:
        """Categorize response time performance."""
        if self.response_time is None:
            return "unknown"
        elif self.response_time < 200:
            return "excellent"
        elif self.response_time < 500:
            return "good"
        elif self.response_time < 1000:
            return "acceptable"
        elif self.response_time < 2000:
            return "slow"
        else:
            return "very_slow"
    
    def to_dict(self) -> dict:
        """Convert the test result to a dictionary."""
        return {
            "test_id": self.test_id,
            "test_type": self.test_type.value,
            "source_device": self.source_device,
            "source_network": self.source_network,
            "target_url": self.target_url,
            "success": self.success,
            "response_code": self.response_code,
            "response_time": self.response_time,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TestResult':
        """Create a TestResult from a dictionary."""
        timestamp = None
        if data.get("timestamp"):
            timestamp = datetime.fromisoformat(data["timestamp"])
        
        return cls(
            test_id=data["test_id"],
            test_type=TestType(data["test_type"]),
            source_device=data["source_device"],
            source_network=data["source_network"],
            target_url=data["target_url"],
            success=data["success"],
            response_code=data.get("response_code"),
            response_time=data.get("response_time"),
            error_message=data.get("error_message"),
            timestamp=timestamp
        )