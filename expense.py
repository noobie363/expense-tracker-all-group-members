from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
from typing import Optional


@dataclass
class Expense:
    id: str
    amount: float
    category: str
    date: str  # ISO 8601 string
    description: str = ""

    @classmethod
    def create(cls, amount: float, category: str, date: Optional[str] = None, description: str = ""):
        """Create a new Expense, filling missing date and generating a unique id."""
        if date is None:
            date = datetime.now().isoformat()
        return cls(id=str(uuid.uuid4()), amount=float(amount), category=category, date=date, description=description)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        try:
            # Ensure amount is a float
            amount = float(data.get('amount', 0))
            # Ensure date is a string
            date = str(data.get('date', datetime.now().isoformat()))
            # Ensure category is a string
            category = str(data.get('category', 'Other'))
            return cls(
                id=data.get('id', str(uuid.uuid4())),
                amount=amount,
                category=category,
                date=date,
                description=str(data.get('description', ''))
            )
        except (ValueError, KeyError, TypeError):
            # Return a safe default if data is corrupted
            return cls(
                id=str(uuid.uuid4()),
                amount=0.0,
                category='Other',
                date=datetime.now().isoformat(),
                description='[Corrupted]'
            )

    def __str__(self) -> str:
        d = self.date[:10]
        return f"{self.id} | {d} | {self.category} | {self.amount:.2f} | {self.description}"
