"""Data models for diskindex entities."""

import dataclasses
import json
from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class Scan:
    """Represents a scan session."""
    id: Optional[int] = None
    scan_date: Optional[datetime] = None
    scan_path: str = ""
    duration_seconds: Optional[float] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "scan_date": self.scan_date.isoformat() if self.scan_date else None,
            "scan_path": self.scan_path,
            "duration_seconds": self.duration_seconds,
            "notes": self.notes,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Scan":
        """Create from dictionary."""
        if data.get("scan_date"):
            data["scan_date"] = datetime.fromisoformat(data["scan_date"])
        return cls(**data)


@dataclasses.dataclass
class Volume:
    """Represents a disk volume or partition."""
    id: Optional[int] = None
    scan_id: Optional[int] = None
    label: Optional[str] = None
    filesystem_type: Optional[str] = None
    mount_point: Optional[str] = None
    device_path: Optional[str] = None
    total_size: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "scan_id": self.scan_id,
            "label": self.label,
            "filesystem_type": self.filesystem_type,
            "mount_point": self.mount_point,
            "device_path": self.device_path,
            "total_size": self.total_size,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Volume":
        """Create from dictionary."""
        return cls(**data)


@dataclasses.dataclass
class Directory:
    """Represents a directory in the hierarchy."""
    id: Optional[int] = None
    scan_id: Optional[int] = None
    parent_id: Optional[int] = None
    path: str = ""
    name: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "scan_id": self.scan_id,
            "parent_id": self.parent_id,
            "path": self.path,
            "name": self.name,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Directory":
        """Create from dictionary."""
        return cls(**data)


@dataclasses.dataclass
class File:
    """Represents a file entry."""
    id: Optional[int] = None
    scan_id: Optional[int] = None
    directory_id: Optional[int] = None
    filename: str = ""
    extension: Optional[str] = None
    size: int = 0
    mtime: Optional[datetime] = None
    md5_hash: Optional[str] = None
    deleted_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "scan_id": self.scan_id,
            "directory_id": self.directory_id,
            "filename": self.filename,
            "extension": self.extension,
            "size": self.size,
            "mtime": self.mtime.isoformat() if self.mtime else None,
            "md5_hash": self.md5_hash,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "File":
        """Create from dictionary."""
        if data.get("mtime"):
            data["mtime"] = datetime.fromisoformat(data["mtime"])
        if data.get("deleted_at"):
            data["deleted_at"] = datetime.fromisoformat(data["deleted_at"])
        return cls(**data)


@dataclasses.dataclass
class IgnorePattern:
    """Represents an ignore pattern rule."""
    id: Optional[int] = None
    pattern: str = ""
    is_exception: bool = False
    applies_to: str = "all"
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "pattern": self.pattern,
            "is_exception": self.is_exception,
            "applies_to": self.applies_to,
            "notes": self.notes,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "IgnorePattern":
        """Create from dictionary."""
        return cls(**data)


def serialize_to_json(obj) -> str:
    """Serialize object to JSON string."""
    if hasattr(obj, 'to_dict'):
        return json.dumps(obj.to_dict(), indent=2)
    return json.dumps(obj, indent=2, default=str)
