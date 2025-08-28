from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List
import uuid


@dataclass
class Job:
    """Simple job container passed between pipeline services."""

    data: Any
    workspace: Path
    steps: List[str] = field(default_factory=list)

    @classmethod
    def create(cls, data: Any, base_dir: Path | None = None) -> "Job":
        """Create a job with a unique workspace directory."""
        base = base_dir or Path("workspaces")
        base.mkdir(parents=True, exist_ok=True)
        workspace = base / f"job-{uuid.uuid4().hex}"
        workspace.mkdir()
        return cls(data=data, workspace=workspace)

    def record_step(self, name: str) -> None:
        """Append a step name to the trace and create a marker file."""
        self.steps.append(name)
        marker = self.workspace / f"{name}.txt"
        marker.write_text(name)
