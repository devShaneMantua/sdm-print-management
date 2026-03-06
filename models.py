from pydantic import BaseModel, Field
from typing import Optional
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
    document_name: str = Field(..., min_length=1, description="Name of the document")
    pages: int = Field(..., gt=0, description="Number of pages to print")
    print_type: PrintType = Field(..., description="Type of printing")


class Order(BaseModel):
    """Complete order model"""
    order_id: str = Field(..., description="Unique order ID")
    customer_name: str
    document_name: str
    pages: int
    print_type: PrintType
    total_cost: float
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
