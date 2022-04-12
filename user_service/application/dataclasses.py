from typing import Optional

import attr


@attr.dataclass
class User:
    name: str
    email: str
    id: Optional[int] = None
