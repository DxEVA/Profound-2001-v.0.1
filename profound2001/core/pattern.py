"""
Pattern contract
"""
from abc import ABC, abstractmethod
from profound2001.runtime.context import Context

from dataclasses import dataclass, field
from typing import List

@dataclass
class PatternConstraints:
    time_complexity: str = "Unknown"
    memory_estimate: str = "Unknown"
    negative_capabilities: List[str] = field(default_factory=list)
    provenance: str = "User"
    is_reversible: bool = False
    designed_failure: bool = False
    confidence: float = 1.0

class Pattern(ABC):
    """
    Base contract for all logic units.
    Must be deterministic and stateless.
    """
    
    @property
    @abstractmethod
    def constraints(self) -> PatternConstraints:
        """Constitutional constraints declaration."""
        pass
    
    @abstractmethod
    def execute(self, context: Context) -> None:
        """
        Execute the pattern logic against the given context.
        Modifies context in-place.
        """
        pass

