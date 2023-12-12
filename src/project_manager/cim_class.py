from dataclasses import dataclass, asdict
from typing import List


@dataclass(frozen=True)
class CimClass:

    classId: str
    classVersion: str
    dataItems: List[dict]
    description: str
    compositeMembers: List[dict] = None

    def to_dict(self):
        return asdict(self)
