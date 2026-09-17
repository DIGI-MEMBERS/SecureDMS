from dataclasses import dataclass
from typing import Optional


@dataclass
class Case:
    id: Optional[int]
    case_number: str
    title: str
    description: Optional[str]
    investigator_id: Optional[int]
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]