from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


DEFAULT_GOALS: List[str] = [
    "Költségcsökkentés",
    "Bevétel növelése",
    "Termékminőség javítása",
    "Ügyfél elégedettség növelése",
]

DEFAULT_ROLES: List[str] = [
    "Projektcsapat tag",
    "Pénzügyi ellenőr",
    "Minőségbiztosítás",
    "Beszállító kapcsolattartó",
]

DEFAULT_ROLE_LABELS: List[str] = ["beszállító", "belső munkatárs"]

DEFAULT_IMPACT_AREAS: List[str] = [
    "Ütemezés",
    "Költségvetés",
    "Ügyfélélmény",
    "Minőség",
    "Erőforrások",
]


@dataclass
class Stakeholder:
    role: str
    display_name: str
    email: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    dedication_fte: Optional[float] = None


@dataclass
class Risk:
    description: str
    probability: int  # 1-4 (Fibonacci)
    impact_area: str
    severity: int  # 1-4 (Fibonacci)


@dataclass
class Link:
    description: str
    url: str


@dataclass
class Project:
    start_date: date
    end_date: Optional[date] = None
    duration_months: Optional[int] = None
    goals: List[str] = field(default_factory=list)
    stakeholders: List[Stakeholder] = field(default_factory=list)
    budget: Optional[float] = None
    budget_approved: bool = False
    risks: List[Risk] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.end_date is None and self.duration_months is None:
            raise ValueError("Either end_date or duration_months must be set")
        if self.end_date is not None and self.duration_months is not None:
            raise ValueError("Only one of end_date or duration_months can be set")
