"""
Waste Data Model (M in MVC)
Defines the business logic, metadata, recyclability schemas, and logging
for solid waste categories and the human safety non-waste entity in EcoVision.
"""

import time
from datetime import datetime

# Domain metadata for each target category
WASTE_CATEGORIES = {
    "human": {
        "id": "human",
        "name": "Human — NOT A WASTE",
        "emoji": "🧑",
        "bin_color": "#DC2626",  # Red Alert
        "bin_name": "⛔ NOT A WASTE (Living Being)",
        "recyclable": False,
        "disposal_type": "Living Human Being (Zero Disposal Action)",
        "decomposition_years": "N/A (Living Person)",
        "co2_saved_kg": 0.0,
        "instructions": "⛔ Safety Interlock: Living human detected! Do NOT dispose. Please keep hands, face, and person clear of the disposal chute.",
        "common_items": ["Living individual", "User face / selfie", "Human hand or arm", "Person in frame"]
    },
    "plastic": {
        "id": "plastic",
        "name": "Plastic",
        "emoji": "🧴",
        "bin_color": "#2563EB",  # Blue
        "bin_name": "Blue Recycling Bin (Dry Recyclables)",
        "recyclable": True,
        "disposal_type": "Recyclable Polymer",
        "decomposition_years": "450–1000 years",
        "co2_saved_kg": 1.5,
        "instructions": "Empty all liquids, rinse off food residue, remove caps if non-recyclable, and compress container.",
        "common_items": ["PET beverage bottles", "milk jugs", "shampoo bottles", "detergent flasks", "plastic containers"]
    },
    "paper": {
        "id": "paper",
        "name": "Paper",
        "emoji": "📄",
        "bin_color": "#D97706",  # Amber/Yellow
        "bin_name": "Yellow Bin (Clean Paper & Card)",
        "recyclable": True,
        "disposal_type": "Cellulose Fiber",
        "decomposition_years": "2–6 weeks",
        "co2_saved_kg": 0.9,
        "instructions": "Keep clean and dry. Do not recycle if soaked in oil, grease, or food stains.",
        "common_items": ["Office printing paper", "newspapers", "magazines", "envelopes", "receipts"]
    },
    "glass": {
        "id": "glass",
        "name": "Glass",
        "emoji": "🍾",
        "bin_color": "#0D9488",  # Teal / Green
        "bin_name": "Teal Bin (Glass Segregation)",
        "recyclable": True,
        "disposal_type": "Inert Mineral (100% Infinitely Recyclable)",
        "decomposition_years": "1,000,000+ years",
        "co2_saved_kg": 0.3,
        "instructions": "Rinse containers clean. Remove metal/plastic lids. Do not mix with ceramic or heat-resistant Pyrex.",
        "common_items": ["Beverage bottles", "jam & condiment jars", "perfume bottles", "glass containers"]
    },
    "metal": {
        "id": "metal",
        "name": "Metal & Aluminium",
        "emoji": "🥫",
        "bin_color": "#475569",  # Steel Gray
        "bin_name": "Silver/Gray Bin (Scrap Metal & Cans)",
        "recyclable": True,
        "disposal_type": "Ferrous & Non-Ferrous Metal",
        "decomposition_years": "50–500 years",
        "co2_saved_kg": 2.1,
        "instructions": "Rinse completely, crush cans to save space, and place in metal recycling bin.",
        "common_items": ["Aluminium soda cans", "tin soup cans", "foil trays", "aerosol cans (empty)", "hardware tools"]
    },
    "cardboard": {
        "id": "cardboard",
        "name": "Cardboard",
        "emoji": "📦",
        "bin_color": "#B45309",  # Brown/Amber
        "bin_name": "Brown Bin (Corrugated Cardboard)",
        "recyclable": True,
        "disposal_type": "Corrugated Fiberboard",
        "decomposition_years": "2–3 months",
        "co2_saved_kg": 1.1,
        "instructions": "Flatten all shipping boxes, remove plastic tape/packing slips, keep dry.",
        "common_items": ["Corrugated delivery boxes", "cereal cartons", "shoe boxes", "paperboard packaging"]
    },
    "organic": {
        "id": "organic",
        "name": "Organic Waste",
        "emoji": "🍎",
        "bin_color": "#16A34A",  # Green
        "bin_name": "Green Bin (Compost & Biodegradables)",
        "recyclable": False,
        "compostable": True,
        "disposal_type": "Biodegradable Organic Biomass",
        "decomposition_years": "1–6 months",
        "co2_saved_kg": 0.5,
        "instructions": "Place in dedicated organic/compost bin. Keep free of plastic wrap, stickers, and metal ties.",
        "common_items": ["Fruit & vegetable scraps", "coffee grounds", "egg shells", "leaves & potted houseplants"]
    }
}


class WasteLogManager:
    """Maintains in-memory and chronological classification logs."""
    _history = []
    _stats = {
        "total_scanned": 0,
        "plastic": 0,
        "paper": 0,
        "glass": 0,
        "metal": 0,
        "cardboard": 0,
        "organic": 0,
        "human": 0
    }

    @classmethod
    def record(cls, category_id, confidence, filename="upload.jpg", source="upload"):
        """Record a newly classified item."""
        cls._stats["total_scanned"] += 1
        if category_id in cls._stats:
            cls._stats[category_id] += 1

        record = {
            "id": int(time.time() * 1000),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category_id,
            "category_name": WASTE_CATEGORIES.get(category_id, {}).get("name", category_id.title()),
            "confidence": round(confidence * 100, 1),
            "filename": filename,
            "source": source
        }
        cls._history.insert(0, record)
        if len(cls._history) > 50:
            cls._history.pop()
        return record

    @classmethod
    def get_history(cls, limit=20):
        return cls._history[:limit]

    @classmethod
    def get_stats(cls):
        return dict(cls._stats)
