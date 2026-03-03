from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
from typing import Optional

from models import (
    OrderCreate, 
    Order, 
    OrderResponse, 
    OrderListResponse, 
    PrintType, 
    PRICING
)
import storage

app = FastAPI(
    title="Printing Order Management System",
    description="A digital system to manage printing orders, compute costs automatically, and track order history.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Info"])
def root():
    """Welcome endpoint with system information"""
    return {
        "system": "Printing Order Management System",
        "version": "1.0.0",
        "pricing": {
            "black_white": "PHP 2.00/page",
            "colored": "PHP 5.00/page",
            "photo_paper": "PHP 20.00/page"
        },
        "endpoints": {
            "create_order": "POST /orders",
            "list_orders": "GET /orders",
            "get_order": "GET /orders/{order_id}",
            "update_status": "PATCH /orders/{order_id}/status",
            "delete_order": "DELETE /orders/{order_id}",
            "get_pricing": "GET /pricing"
        }
    }


@app.get("/pricing", tags=["Info"])
def get_pricing():
    """Get current printing prices"""
    return {
        "currency": "PHP",
        "prices": {
            "black_white": {
                "price_per_page": PRICING[PrintType.BLACK_WHITE],
                "description": "Standard black and white printing"
            },
            "colored": {
                "price_per_page": PRICING[PrintType.COLORED],
                "description": "Full color printing"
            },
            "photo_paper": {
                "price_per_page": PRICING[PrintType.PHOTO_PAPER],
                "description": "High quality photo paper printing"
            }
        }
    }


@app.post("/orders", response_model=OrderResponse, tags=["Orders"])
def create_order(order_data: OrderCreate):
    """
    Create a new printing order.
    
    Automatically computes the total cost based on:
    - Print type (black_white, colored, photo_paper)
    - Number of pages
    
    Returns the created order with computed total cost.
    """
    # Get price per page based on print type
    price_per_page = PRICING[order_data.print_type]
    
    # Compute total cost
    total_cost = price_per_page * order_data.num_pages
    
    # Create order with generated ID and timestamp
    order = Order(
        id=str(uuid.uuid4())[:8].upper(),  # Short readable ID
        customer_name=order_data.customer_name,
        print_type=order_data.print_type,
        num_pages=order_data.num_pages,
        price_per_page=price_per_page,
        total_cost=total_cost,
        description=order_data.description,
        created_at=datetime.now().isoformat(),
        status="pending"
    )
    
    # Save to storage
    saved_order = storage.add_order(order)
    
    return OrderResponse(
        success=True,
        message=f"Order created successfully. Total cost: PHP {total_cost:.2f}",
        order=saved_order
    )


@app.get("/orders", response_model=OrderListResponse, tags=["Orders"])
def list_orders(
    print_type: Optional[PrintType] = Query(None, description="Filter by print type"),
    status: Optional[str] = Query(None, description="Filter by status (pending, completed, cancelled)")
):
    """
    Retrieve all orders with optional filtering.
    
    Can filter by:
    - print_type: black_white, colored, photo_paper
    - status: pending, completed, cancelled
    """
    orders = storage.get_all_orders()
    
    # Apply filters
    if print_type:
        orders = [o for o in orders if o.print_type == print_type]
    if status:
        orders = [o for o in orders if o.status == status]
    
    return OrderListResponse(
        success=True,
        total_orders=len(orders),
        orders=orders
    )


@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def get_order(order_id: str):
    """
    Retrieve a specific order by its ID.
    
    Returns the complete order details including computed total cost.
    """
    order = storage.get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID '{order_id}' not found"
        )
    
    return OrderResponse(
        success=True,
        message="Order retrieved successfully",
        order=order
    )


@app.patch("/orders/{order_id}/status", response_model=OrderResponse, tags=["Orders"])
def update_order_status(order_id: str, status: str = Query(..., description="New status: pending, completed, cancelled")):
    """
    Update the status of an order.
    
    Valid statuses: pending, completed, cancelled
    """
    valid_statuses = ["pending", "completed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    order = storage.update_order_status(order_id, status)
    
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID '{order_id}' not found"
        )
    
    return OrderResponse(
        success=True,
        message=f"Order status updated to '{status}'",
        order=order
    )


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: str):
    """
    Delete an order by its ID.
    
    This action cannot be undone.
    """
    success = storage.delete_order(order_id)
    
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID '{order_id}' not found"
        )
    
    return {
        "success": True,
        "message": f"Order '{order_id}' deleted successfully"
    }


@app.get("/stats", tags=["Info"])
def get_statistics():
    """
    Get order statistics and summary.
    """
    orders = storage.get_all_orders()
    
    total_revenue = sum(o.total_cost for o in orders)
    total_pages = sum(o.num_pages for o in orders)
    
    # Count by print type
    by_print_type = {}
    for pt in PrintType:
        count = len([o for o in orders if o.print_type == pt])
        by_print_type[pt.value] = count
    
    # Count by status
    status_counts = {
        "pending": len([o for o in orders if o.status == "pending"]),
        "completed": len([o for o in orders if o.status == "completed"]),
        "cancelled": len([o for o in orders if o.status == "cancelled"])
    }
    
    return {
        "total_orders": len(orders),
        "total_revenue": f"PHP {total_revenue:.2f}",
        "total_pages_printed": total_pages,
        "orders_by_print_type": by_print_type,
        "orders_by_status": status_counts
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
