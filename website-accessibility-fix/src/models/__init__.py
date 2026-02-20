"""Core data models for website accessibility fix tool."""

from .diagnostic_result import DiagnosticResult
from .server_configuration import ServerConfiguration
from .firewall_rule import FirewallRule
from .test_result import TestResult

__all__ = [
    "DiagnosticResult",
    "ServerConfiguration", 
    "FirewallRule",
    "TestResult"
]