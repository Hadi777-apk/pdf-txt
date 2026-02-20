"""FirewallRule data model for firewall rule configuration."""

from enum import Enum
from typing import Optional
from dataclasses import dataclass


class TrafficDirection(Enum):
    """Enumeration for traffic direction values."""
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"


class RuleAction(Enum):
    """Enumeration for firewall rule actions."""
    ALLOW = "allow"
    DENY = "deny"
    DROP = "drop"
    REJECT = "reject"


@dataclass
class FirewallRule:
    """
    Data model for storing firewall rule information.
    
    Attributes:
        rule_id: Unique identifier for the firewall rule
        direction: Traffic direction (inbound, outbound, bidirectional)
        protocol: Network protocol (tcp, udp, icmp, any)
        port_range: Port or port range (e.g., "80", "80-443", "any")
        source_address: Source IP address or range (e.g., "any", "192.168.1.0/24")
        destination_address: Destination IP address or range
        action: Action to take (allow, deny, drop, reject)
        priority: Rule priority (lower numbers = higher priority)
    """
    rule_id: str
    direction: TrafficDirection
    protocol: str
    port_range: str
    source_address: str
    destination_address: str
    action: RuleAction
    priority: int
    
    def is_web_traffic_rule(self) -> bool:
        """Check if this rule affects web traffic (ports 80, 443)."""
        web_ports = ["80", "443", "80-443", "any", "*"]
        return any(port in self.port_range for port in web_ports)
    
    def allows_external_access(self) -> bool:
        """Check if this rule allows external access."""
        external_sources = ["any", "0.0.0.0/0", "::/0", "*"]
        return (
            self.action == RuleAction.ALLOW and
            self.direction in [TrafficDirection.INBOUND, TrafficDirection.BIDIRECTIONAL] and
            any(source in self.source_address for source in external_sources)
        )
    
    def blocks_external_access(self) -> bool:
        """Check if this rule blocks external access."""
        external_sources = ["any", "0.0.0.0/0", "::/0", "*"]
        return (
            self.action in [RuleAction.DENY, RuleAction.DROP, RuleAction.REJECT] and
            self.direction in [TrafficDirection.INBOUND, TrafficDirection.BIDIRECTIONAL] and
            any(source in self.source_address for source in external_sources)
        )
    
    def affects_port(self, port: int) -> bool:
        """Check if this rule affects a specific port."""
        if self.port_range in ["any", "*"]:
            return True
        
        if "-" in self.port_range:
            # Handle port ranges like "80-443"
            try:
                start_port, end_port = map(int, self.port_range.split("-"))
                return start_port <= port <= end_port
            except ValueError:
                return False
        else:
            # Handle single ports
            try:
                return int(self.port_range) == port
            except ValueError:
                return False
    
    def to_dict(self) -> dict:
        """Convert the firewall rule to a dictionary."""
        return {
            "rule_id": self.rule_id,
            "direction": self.direction.value,
            "protocol": self.protocol,
            "port_range": self.port_range,
            "source_address": self.source_address,
            "destination_address": self.destination_address,
            "action": self.action.value,
            "priority": self.priority
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FirewallRule':
        """Create a FirewallRule from a dictionary."""
        return cls(
            rule_id=data["rule_id"],
            direction=TrafficDirection(data["direction"]),
            protocol=data["protocol"],
            port_range=data["port_range"],
            source_address=data["source_address"],
            destination_address=data["destination_address"],
            action=RuleAction(data["action"]),
            priority=data["priority"]
        )