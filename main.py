from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uuid

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
    Automatically computes the total cost based on print type and number of pages.
    """
    price_per_page = PRICING[order_data.print_type]
    total_cost = price_per_page * order_data.pages

    order = Order(
        order_id=str(uuid.uuid4())[:8].upper(),
        customer_name=order_data.customer_name,
        document_name=order_data.document_name,
        pages=order_data.pages,
        print_type=order_data.print_type,
        total_cost=total_cost,
        status="pending"
    )

    saved_order = storage.add_order(order)

    return OrderResponse(
        success=True,
        message=f"Order created successfully. Total cost: PHP {total_cost:.2f}",
        order=saved_order
    )


@app.get("/orders", response_model=OrderListResponse, tags=["Orders"])
def list_orders():
    """Retrieve all orders."""
    orders = storage.get_all_orders()

    return OrderListResponse(
        success=True,
        total_orders=len(orders),
        orders=orders
    )


@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def get_order(order_id: str):
    """Retrieve a specific order by its ID."""
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
def update_order_status(order_id: str, status: str = Query(..., description="New status: pending, completed")):
    """
    Update the status of an order.
    Valid statuses: pending, completed
    """
    valid_statuses = ["pending", "completed"]
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
    """Delete an order by its ID."""
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
