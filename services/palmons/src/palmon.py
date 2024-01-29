from typing import Dict, Any
import random

def generate_palmon() -> Dict[str, Any]:
    stats = [
        random.randint(80, 120),
        random.randint(80, 120),
        random.randint(80, 120),
        random.randint(80, 120),
    ]
    return {
        "type": "Micy",
        "lvl": 1,
        "hp": stats[0],
        "stats": stats
    }