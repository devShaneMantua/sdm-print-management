import json
import os
from typing import Optional
from models import Order

# Path to the orders JSON file
ORDERS_FILE = "orders.json"


def _ensure_file_exists() -> None:
    """Create the orders file if it doesn't exist"""
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w') as f:
            json.dump([], f)


def load_orders() -> list[dict]:
    """Load all orders from the JSON file"""
    _ensure_file_exists()
    try:
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_orders(orders: list[dict]) -> None:
    """Save all orders to the JSON file"""
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)


def get_next_order_id() -> int:
    """Get the next order ID (incremental)"""
    orders = load_orders()
    if not orders:
        return 1
    max_id = max(int(order.get("order_id", 0)) for order in orders)
    return max_id + 1


def add_order(order: Order) -> Order:
    """Add a new order to storage"""
    orders = load_orders()
    orders.append(order.model_dump())
    save_orders(orders)
    return order


def get_all_orders() -> list[Order]:
    """Retrieve all orders from storage"""
    orders_data = load_orders()
    return [Order(**order) for order in orders_data]


def get_order_by_id(order_id: str) -> Optional[Order]:
    """Retrieve a specific order by ID"""
    orders_data = load_orders()
    for order in orders_data:
        if order.get("order_id") == order_id:
            return Order(**order)
    return None


def update_order_status(order_id: str, status: str) -> Optional[Order]:
    """Update the status of an order"""
    orders = load_orders()
    for order in orders:
        if order.get("order_id") == order_id:
            order["status"] = status
            save_orders(orders)
            return Order(**order)
    return None


def delete_order(order_id: str) -> bool:
    """Delete an order by ID"""
    orders = load_orders()
    original_length = len(orders)
    orders = [o for o in orders if o.get("order_id") != order_id]
    
    if len(orders) < original_length:
        save_orders(orders)
        return True
    return False
