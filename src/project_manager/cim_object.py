from dataclasses import dataclass, asdict
from typing import List


@dataclass
class CimObject:

    Attributes: List[dict]
    ClassID: str
    Description: str
    ID: str
    Routing: List[str]

    def to_dict(self):
        return asdict(self)
