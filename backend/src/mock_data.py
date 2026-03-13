"""
mock_data.py — Simulated E-Commerce Database
=============================================
This module provides mock data that simulates a real e-commerce backend.
In production, these would be replaced by actual database queries / API calls.
"""

from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------
CUSTOMERS = {
    "C001": {
        "id": "C001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "tier": "Gold",
        "joined": "2023-01-15",
    },
    "C002": {
        "id": "C002",
        "name": "Bob Smith",
        "email": "bob@example.com",
        "tier": "Silver",
        "joined": "2023-06-20",
    },
    "C003": {
        "id": "C003",
        "name": "Carol Davis",
        "email": "carol@example.com",
        "tier": "Bronze",
        "joined": "2024-02-10",
    },
    "C004": {
        "id": "C004",
        "name": "Dan Wilson",
        "email": "dan@example.com",
        "tier": "Gold",
        "joined": "2022-11-05",
    },
    "C005": {
        "id": "C005",
        "name": "Eve Martinez",
        "email": "eve@example.com",
        "tier": "Silver",
        "joined": "2024-08-01",
    },
    "C006": {
        "id": "C006",
        "name": "Frank Miller",
        "email": "frank@example.com",
        "tier": "Bronze",
        "joined": "2024-09-12",
    },
    "C007": {
        "id": "C007",
        "name": "Grace Lee",
        "email": "grace@example.com",
        "tier": "Gold",
        "joined": "2024-10-05",
    },
}

# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
PRODUCTS = {
    "P001": {
        "id": "P001",
        "name": "ProBook Laptop 15",
        "brand": "TechPro",
        "category": "Electronics",
        "price": 1299.99,
        "rating": 4.7,
        "description": "15-inch professional laptop with 32GB RAM, 1TB SSD. Ideal for developers and creators.",
        "specs": "CPU: Intel i9, RAM: 32GB, Storage: 1TB SSD, Display: 15.6\" 4K, Battery: 12hrs",
        "warranty": "2-year manufacturer warranty",
        "tags": "laptop, professional, techpro, developer, 4k",
        "in_stock": True,
    },
    "P002": {
        "id": "P002",
        "name": "SoundMax Wireless Headphones",
        "brand": "AudioPure",
        "category": "Electronics",
        "price": 149.99,
        "rating": 4.5,
        "description": "Active noise-canceling Bluetooth headphones with 30-hour battery life.",
        "specs": "Type: Over-ear, Battery: 30h, Connectivity: Bluetooth 5.2, Noise-Canceling: Yes",
        "warranty": "1-year accidental damage protection",
        "tags": "headphones, wireless, noise-canceling, audio",
        "in_stock": True,
    },
    "P003": {
        "id": "P003",
        "name": "ErgoDesk Standing Desk",
        "brand": "FlexiWork",
        "category": "Furniture",
        "price": 549.99,
        "rating": 4.8,
        "description": "Electric height-adjustable standing desk with memory presets.",
        "specs": "Height Range: 24\"-50\", Weight Capacity: 220 lbs, Top Material: Oak Wood",
        "warranty": "5-year motor warranty",
        "tags": "desk, office, standing, ergonomic, furniture",
        "in_stock": True,
    },
    "P004": {
        "id": "P004",
        "name": "CodeMaster Mechanical Keyboard",
        "brand": "TypistX",
        "category": "Electronics",
        "price": 89.99,
        "rating": 4.6,
        "description": "Cherry MX Brown switches, RGB backlight, USB-C connectivity.",
        "specs": "Switches: Cherry MX Brown, Layout: Tenkeyless, RGB: Per-key, Connection: USB-C",
        "warranty": "1-year limited warranty",
        "tags": "keyboard, mechanical, coding, rgb, typistx",
        "in_stock": True,
    },
    "P005": {
        "id": "P005",
        "name": "UltraWide Monitor 34\"",
        "brand": "VisionCore",
        "category": "Electronics",
        "price": 699.99,
        "rating": 4.4,
        "description": "34-inch curved ultrawide monitor, 3440x1440, 144Hz refresh rate.",
        "specs": "Resolution: 3440x1440p, Refresh Rate: 144Hz, Panel: IPS, Curvature: 1500R",
        "warranty": "3-year zero-pixel guarantee",
        "tags": "monitor, ultrawide, gaming, curved, visioncore",
        "in_stock": False,
    },
    "P006": {
        "id": "P006",
        "name": "ComfortPlus Office Chair",
        "brand": "SootheSeat",
        "category": "Furniture",
        "price": 399.99,
        "rating": 4.3,
        "description": "Ergonomic mesh office chair with lumbar support and adjustable armrests.",
        "specs": "Material: Breathable Mesh, Base: Reinforced Nylon, Max Load: 300 lbs",
        "warranty": "2-year part replacement warranty",
        "tags": "chair, ergonomics, office, mesh, sootheat",
        "in_stock": True,
    },
    "P007": {
        "id": "P007",
        "name": "SmartHome Hub Pro",
        "brand": "ConnectLife",
        "category": "Smart Home",
        "price": 199.99,
        "rating": 4.1,
        "description": "Central hub for smart home devices. Works with Alexa, Google, and HomeKit.",
        "specs": "Connectivity: Zigbee, Z-Wave, WiFi, Audio: Internal speaker, Voice: Multi-assistant",
        "warranty": "1-year limited warranty",
        "tags": "smarthome, hub, automation, connectlife",
        "in_stock": True,
    },
    "P008": {
        "id": "P008",
        "name": "TechPack Laptop Backpack",
        "brand": "CarryAll",
        "category": "Accessories",
        "price": 79.99,
        "rating": 4.9,
        "description": "Water-resistant laptop backpack with USB charging port and anti-theft design.",
        "specs": "Capacity: 25L, Size: Fits up to 16\" laptop, Material: Water-resistant Nylon",
        "warranty": "Lifetime replacement warranty",
        "tags": "backpack, accessories, travel, laptop-bag",
        "in_stock": True,
    },
    "P009": {
        "id": "P009",
        "name": "Titan Gaming Laptop",
        "brand": "GameForce",
        "category": "Electronics",
        "price": 2499.00,
        "rating": 4.9,
        "description": "Extreme performance gaming laptop with NVIDIA RTX 4090.",
        "specs": "GPU: RTX 4090, CPU: i9-14900HX, RAM: 64GB DDR5, Screen: 18\" 240Hz",
        "warranty": "1-year premium on-site repair",
        "tags": "gaming, laptop, rtx4090, high-end, gameforce",
        "in_stock": True,
    },
    "P010": {
        "id": "P010",
        "name": "Minimalist Oak Coffee Table",
        "brand": "ScandiBuild",
        "category": "Furniture",
        "price": 199.50,
        "rating": 4.6,
        "description": "Sleek coffee table made from solid Scandinavian oak.",
        "specs": "Dimensions: 40\"x20\"x18\", Material: Solid Oak, Finish: Natural Oil",
        "warranty": "Lifetime wood integrity warranty",
        "tags": "furniture, living-room, oak, scandi, table",
        "in_stock": True,
    }
}

PRODUCT_REVIEWS = [
    {"product_id": "P001", "rating": 5, "comment": "Incredible performance. Runs Docker and heavy IDEs without breaking a sweat.", "customer_name": "Alice J.", "date": "2024-01-20"},
    {"product_id": "P001", "rating": 4, "comment": "Screen is beautiful, but the fans can get a bit loud under load.", "customer_name": "Mark R.", "date": "2024-02-05"},
    {"product_id": "P002", "rating": 5, "comment": "Noise cancellation is rivaling Bose. Love the battery life.", "customer_name": "Sarah K.", "date": "2023-12-12"},
    {"product_id": "P003", "rating": 5, "comment": "Saved my back! Smooth motor and very sturdy.", "customer_name": "Bob S.", "date": "2024-03-01"},
    {"product_id": "P009", "rating": 5, "comment": "A absolute beast. Cyberpunk at 4K maxed out with ease.", "customer_name": "GamerX", "date": "2024-03-10"},
]

# ---------------------------------------------------------------------------
# Orders — dates are relative to "today" so the demo always feels current
# ---------------------------------------------------------------------------
_today = datetime.now()


def _date(days_ago: int) -> str:
    """Return an ISO-format date string for `days_ago` days in the past."""
    return (_today - timedelta(days=days_ago)).strftime("%Y-%m-%d")


def _future(days_ahead: int) -> str:
    """Return an ISO-format date string for `days_ahead` days in the future."""
    return (_today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")


ORDERS = {
    "1001": {
        "id": "1001",
        "customer_id": "C001",
        "items": [
            {"product_id": "P001", "name": "ProBook Laptop 15", "qty": 1, "price": 1299.99},
        ],
        "total": 1299.99,
        "status": "shipped",
        "ordered_date": _date(5),
        "shipped_date": _date(3),
        "tracking_number": "FX-78923456",
        "estimated_delivery": _future(2),
    },
    "1002": {
        "id": "1002",
        "customer_id": "C001",
        "items": [
            {"product_id": "P002", "name": "SoundMax Wireless Headphones", "qty": 1, "price": 149.99},
            {"product_id": "P004", "name": "CodeMaster Mechanical Keyboard", "qty": 1, "price": 89.99},
        ],
        "total": 239.98,
        "status": "delivered",
        "ordered_date": _date(15),
        "shipped_date": _date(13),
        "delivered_date": _date(10),
        "tracking_number": "FX-78923457",
    },
    "1003": {
        "id": "1003",
        "customer_id": "C002",
        "items": [
            {"product_id": "P003", "name": "ErgoDesk Standing Desk", "qty": 1, "price": 549.99},
        ],
        "total": 549.99,
        "status": "processing",
        "ordered_date": _date(1),
    },
    "1004": {
        "id": "1004",
        "customer_id": "C002",
        "items": [
            {"product_id": "P006", "name": "ComfortPlus Office Chair", "qty": 2, "price": 399.99},
        ],
        "total": 799.98,
        "status": "delivered",
        "ordered_date": _date(45),
        "shipped_date": _date(43),
        "delivered_date": _date(40),
        "tracking_number": "FX-78923460",
    },
    "1005": {
        "id": "1005",
        "customer_id": "C003",
        "items": [
            {"product_id": "P007", "name": "SmartHome Hub Pro", "qty": 1, "price": 199.99},
            {"product_id": "P008", "name": "TechPack Laptop Backpack", "qty": 1, "price": 79.99},
        ],
        "total": 279.98,
        "status": "delivered",
        "ordered_date": _date(20),
        "shipped_date": _date(18),
        "delivered_date": _date(14),
        "tracking_number": "FX-78923461",
    },
    "1006": {
        "id": "1006",
        "customer_id": "C003",
        "items": [
            {"product_id": "P002", "name": "SoundMax Wireless Headphones", "qty": 1, "price": 149.99},
        ],
        "total": 149.99,
        "status": "returned",
        "ordered_date": _date(25),
        "shipped_date": _date(23),
        "delivered_date": _date(20),
        "returned_date": _date(18),
        "refund_status": "completed",
        "tracking_number": "FX-78923462",
    },
    "1007": {
        "id": "1007",
        "customer_id": "C004",
        "items": [
            {"product_id": "P001", "name": "ProBook Laptop 15", "qty": 1, "price": 1299.99},
            {"product_id": "P004", "name": "CodeMaster Mechanical Keyboard", "qty": 1, "price": 89.99},
        ],
        "total": 1389.98,
        "status": "shipped",
        "ordered_date": _date(3),
        "shipped_date": _date(1),
        "tracking_number": "FX-78923463",
        "estimated_delivery": _future(4),
    },
    "1008": {
        "id": "1008",
        "customer_id": "C004",
        "items": [
            {"product_id": "P005", "name": "UltraWide Monitor 34\"", "qty": 1, "price": 699.99},
        ],
        "total": 699.99,
        "status": "cancelled",
        "ordered_date": _date(10),
        "cancelled_date": _date(9),
        "cancel_reason": "Item out of stock",
    },
    "1009": {
        "id": "1009",
        "customer_id": "C005",
        "items": [
            {"product_id": "P008", "name": "TechPack Laptop Backpack", "qty": 1, "price": 79.99},
        ],
        "total": 79.99,
        "status": "delivered",
        "ordered_date": _date(8),
        "shipped_date": _date(6),
        "delivered_date": _date(3),
        "tracking_number": "FX-78923465",
    },
    "1010": {
        "id": "1010",
        "customer_id": "C005",
        "items": [
            {"product_id": "P003", "name": "ErgoDesk Standing Desk", "qty": 1, "price": 549.99},
            {"product_id": "P006", "name": "ComfortPlus Office Chair", "qty": 1, "price": 399.99},
        ],
        "total": 949.98,
        "status": "processing",
        "ordered_date": _date(0),
    },
    "1011": {
        "id": "1011",
        "customer_id": "C001",
        "items": [
            {"product_id": "P002", "name": "SoundMax Wireless Headphones", "qty": 2, "price": 149.99},
        ],
        "total": 299.98,
        "status": "delivered",
        "ordered_date": _date(60),
        "delivered_date": _date(55),
    },
    "1012": {
        "id": "1012",
        "customer_id": "C006",
        "items": [
            {"product_id": "P002", "name": "SoundMax Wireless Headphones", "qty": 1, "price": 149.99},
            {"product_id": "P008", "name": "TechPack Laptop Backpack", "qty": 1, "price": 79.99},
        ],
        "total": 229.98,
        "status": "delivered",
        "ordered_date": _date(5),
        "delivered_date": _date(2),
    },
    "1013": {
        "id": "1013",
        "customer_id": "C007",
        "items": [
            {"product_id": "P002", "name": "SoundMax Wireless Headphones", "qty": 5, "price": 149.99},
            {"product_id": "P009", "name": "Titan Gaming Laptop", "qty": 1, "price": 2499.00},
        ],
        "total": 3248.95,
        "status": "processing",
        "ordered_date": _date(1),
    },
}

# ---------------------------------------------------------------------------
# Support Ticket History (for escalation context)
# ---------------------------------------------------------------------------
SUPPORT_TICKETS = {
    "T001": {
        "id": "T001",
        "customer_id": "C001",
        "order_id": "1001",
        "subject": "When will my laptop arrive?",
        "status": "open",
        "created": _date(1),
        "priority": "normal",
    },
    "T002": {
        "id": "T002",
        "customer_id": "C003",
        "order_id": "1006",
        "subject": "Headphones stopped working after 2 weeks",
        "status": "closed",
        "created": _date(19),
        "resolved": _date(18),
        "priority": "high",
    },
}
