# Mantua_SDMS Activity

## Printing Order Management System

A digital system that helps a printing business manage and record orders digitally to reduce human errors. It accepts order details and automatically computes the total cost based on number of pages and then stores order records for viewing.

This system helps printing businesses manage and record orders digitally to reduce human errors. It accepts order details and automatically computes the total cost based on number of pages, then stores order records for viewing and management.

### Problem Statement

Printing businesses that process orders manually often face:
- Errors in cost computation
- Incorrect order details
- Difficulty tracking past orders
- Lost or duplicated paper records

### Solution

This system digitizes the entire order workflow:
- Accept and process printing orders electronically
- Automatically compute total cost based on pages and pricing
- Store orders securely in JSON format
- Provide easy retrieval and filtering of orders

### Target Users

- Printing shop staff
- Shop owners or managers

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Runtime |
| FastAPI | ≥0.109.0 | Web framework |
| Uvicorn | ≥0.27.0 | ASGI server |
| Pydantic | ≥2.0.0 | Data validation |

---

## Project Structure

```
printing_system/
├── main.py           # FastAPI application & endpoints
├── models.py         # Pydantic models & pricing config
├── storage.py        # JSON file storage handler
├── orders.json       # Order data storage (auto-created)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Features

- ✅ Create printing orders with automatic cost calculation
- ✅ View all orders with filtering options (by print type, status)
- ✅ Retrieve specific order details by ID
- ✅ Update order status (pending, completed, cancelled)
- ✅ Delete orders
- ✅ View statistics and revenue summaries
- ✅ Local JSON file storage (no database required)
- ✅ CORS enabled for frontend compatibility

---

## Pricing

| Print Type | Code | Price per Page |
|------------|------|----------------|
| Black & White | `black_white` | PHP 2.00 |
| Colored | `colored` | PHP 5.00 |
| Photo Paper | `photo_paper` | PHP 20.00 |

---

## Installation

### Prerequisites

- Python 3.10 or higher

### Steps

1. **Clone or navigate to the project directory**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the server:**
```bash
uvicorn main:app --reload
```

4. **Access the application:**
   - API Root: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Optional: Run on custom host/port
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Data Models

### PrintType (Enum)

| Value | Description |
|-------|-------------|
| `black_white` | Standard black and white printing |
| `colored` | Full color printing |
| `photo_paper` | High quality photo paper printing |

### Order Status

| Status | Description |
|--------|-------------|
| `pending` | Order created, awaiting processing |
| `completed` | Order has been fulfilled |
| `cancelled` | Order was cancelled |

### OrderCreate (Request Body)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer_name` | string | ✅ | Name of the customer (min 1 char) |
| `print_type` | PrintType | ✅ | Type of printing |
| `num_pages` | integer | ✅ | Number of pages (must be > 0) |
| `description` | string | ❌ | Additional notes |

### Order (Full Model)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique 8-character order ID (auto-generated) |
| `customer_name` | string | Customer name |
| `print_type` | PrintType | Type of printing |
| `num_pages` | integer | Number of pages |
| `price_per_page` | float | Price per page based on print type |
| `total_cost` | float | Auto-computed (price_per_page × num_pages) |
| `description` | string | Optional notes |
| `created_at` | string | ISO 8601 datetime of creation |
| `status` | string | Order status (default: "pending") |

---

## API Endpoints

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/orders` | Create a new order |
| `GET` | `/orders` | List all orders (with optional filters) |
| `GET` | `/orders/{order_id}` | Get specific order details |
| `PATCH` | `/orders/{order_id}/status` | Update order status |
| `DELETE` | `/orders/{order_id}` | Delete an order |

### Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | System information & available endpoints |
| `GET` | `/pricing` | Current pricing information |
| `GET` | `/stats` | Order statistics and revenue summary |

---

## API Examples

### Create an Order

**Request:**
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Juan Dela Cruz",
    "print_type": "colored",
    "num_pages": 10,
    "description": "School project printout"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Order created successfully. Total cost: PHP 50.00",
  "order": {
    "id": "A1B2C3D4",
    "customer_name": "Juan Dela Cruz",
    "print_type": "colored",
    "num_pages": 10,
    "price_per_page": 5.0,
    "total_cost": 50.0,
    "description": "School project printout",
    "created_at": "2026-03-03T10:30:00.000000",
    "status": "pending"
  }
}
```

### List All Orders

**Request:**
```bash
curl "http://localhost:8000/orders"
```

**Response:**
```json
{
  "success": true,
  "total_orders": 2,
  "orders": [
    {
      "id": "A1B2C3D4",
      "customer_name": "Juan Dela Cruz",
      "print_type": "colored",
      "num_pages": 10,
      "price_per_page": 5.0,
      "total_cost": 50.0,
      "description": "School project printout",
      "created_at": "2026-03-03T10:30:00.000000",
      "status": "pending"
    }
  ]
}
```

### Filter Orders

**By print type:**
```bash
curl "http://localhost:8000/orders?print_type=colored"
```

**By status:**
```bash
curl "http://localhost:8000/orders?status=pending"
```

**Combined filters:**
```bash
curl "http://localhost:8000/orders?print_type=colored&status=completed"
```

### Get Specific Order

**Request:**
```bash
curl "http://localhost:8000/orders/A1B2C3D4"
```

**Response:**
```json
{
  "success": true,
  "message": "Order retrieved successfully",
  "order": {
    "id": "A1B2C3D4",
    "customer_name": "Juan Dela Cruz",
    "print_type": "colored",
    "num_pages": 10,
    "price_per_page": 5.0,
    "total_cost": 50.0,
    "description": "School project printout",
    "created_at": "2026-03-03T10:30:00.000000",
    "status": "pending"
  }
}
```

### Update Order Status

**Request:**
```bash
curl -X PATCH "http://localhost:8000/orders/A1B2C3D4/status?status=completed"
```

**Response:**
```json
{
  "success": true,
  "message": "Order status updated to 'completed'",
  "order": {
    "id": "A1B2C3D4",
    "status": "completed"
  }
}
```

### Delete Order

**Request:**
```bash
curl -X DELETE "http://localhost:8000/orders/A1B2C3D4"
```

**Response:**
```json
{
  "success": true,
  "message": "Order 'A1B2C3D4' deleted successfully"
}
```

### Get Pricing

**Request:**
```bash
curl "http://localhost:8000/pricing"
```

**Response:**
```json
{
  "currency": "PHP",
  "prices": {
    "black_white": {
      "price_per_page": 2.0,
      "description": "Standard black and white printing"
    },
    "colored": {
      "price_per_page": 5.0,
      "description": "Full color printing"
    },
    "photo_paper": {
      "price_per_page": 20.0,
      "description": "High quality photo paper printing"
    }
  }
}
```

### Get Statistics

**Request:**
```bash
curl "http://localhost:8000/stats"
```

**Response:**
```json
{
  "total_orders": 5,
  "total_revenue": "PHP 250.00",
  "total_pages_printed": 75,
  "orders_by_print_type": {
    "black_white": 2,
    "colored": 2,
    "photo_paper": 1
  },
  "orders_by_status": {
    "pending": 2,
    "completed": 2,
    "cancelled": 1
  }
}
```

---

## Error Handling

| Status Code | Description | Example |
|-------------|-------------|---------|
| `400` | Bad Request | Invalid status value |
| `404` | Not Found | Order ID doesn't exist |
| `422` | Validation Error | Missing required field, invalid data type |

**Example Error Response:**
```json
{
  "detail": "Order with ID 'INVALID' not found"
}
```

**Validation Error Response:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "customer_name"],
      "msg": "Field required"
    }
  ]
}
```

---

## Data Storage

Orders are stored locally in `orders.json` file.

### Storage Features

- **Auto-creation**: File is created automatically on first order
- **Format**: Pretty-printed JSON with 2-space indentation
- **Location**: Same directory as the application

### Storage Functions (storage.py)

| Function | Description |
|----------|-------------|
| `add_order(order)` | Add a new order |
| `get_all_orders()` | Retrieve all orders |
| `get_order_by_id(order_id)` | Get specific order |
| `update_order_status(order_id, status)` | Update order status |
| `delete_order(order_id)` | Delete an order |
| `get_order_count()` | Get total order count |

### Sample orders.json

```json
[
  {
    "id": "A1B2C3D4",
    "customer_name": "Juan Dela Cruz",
    "print_type": "colored",
    "num_pages": 10,
    "price_per_page": 5.0,
    "total_cost": 50.0,
    "description": "School project printout",
    "created_at": "2026-03-03T10:30:00.000000",
    "status": "completed"
  }
]
```

---

## CORS Configuration

The API has CORS enabled for all origins, making it compatible with any frontend application:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload on code changes.

### Testing the API

Use the interactive Swagger UI at http://localhost:8000/docs to test all endpoints directly in your browser.

---

## License

This project is for educational purposes.
