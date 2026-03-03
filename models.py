"""
Pydantic models for the Printing Order Management System
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PrintType(str, Enum):
    """Types of printing available"""
    BLACK_WHITE = "black_white"
    COLORED = "colored"
    PHOTO_PAPER = "photo_paper"


# Pricing in PHP per page
PRICING = {
    PrintType.BLACK_WHITE: 2.00,
    PrintType.COLORED: 5.00,
    PrintType.PHOTO_PAPER: 20.00,
}


class OrderCreate(BaseModel):
    """Request model for creating a new order"""
    customer_name: str = Field(..., min_length=1, description="Name of the customer")
    print_type: PrintType = Field(..., description="Type of printing")
    num_pages: int = Field(..., gt=0, description="Number of pages to print")
    description: Optional[str] = Field(None, description="Additional notes or description")


class Order(BaseModel):
    """Complete order model with computed fields"""
    id: str = Field(..., description="Unique order ID")
    customer_name: str
    print_type: PrintType
    num_pages: int
    price_per_page: float
    total_cost: float
    description: Optional[str] = None
    created_at: str = Field(..., description="ISO format datetime when order was created")
    status: str = Field(default="pending", description="Order status")


class OrderResponse(BaseModel):
    """Response model for order operations"""
    success: bool
    message: str
    order: Optional[Order] = None


class OrderListResponse(BaseModel):
    """Response model for listing all orders"""
    success: bool
    total_orders: int
    orders: list[Order]
