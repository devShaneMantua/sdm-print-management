# SDM Print Management

## Mantua_SDMS Activity

A backend API for recording printing orders digitally to reduce human errors. It accepts order details, computes total cost based on pages and print type, and stores records in `orders.json`.

## Problem Statement

Manual handwritten order logs can lead to incorrect cost computation, duplicate entries, and difficulty tracking past orders.

## Objectives

- Digitize print order recording
- Accept and process printing orders
- Automatically compute total cost based on print type and pricing
- Allow viewing one or all orders
- Reduce errors in computation and order details

## Target Users

- Printing shop staff
- Shop owner or manager

## Tech Stack

| Technology | Version |
|------------|---------|
| Python | 3.10+ |
| FastAPI | >=0.109.0 |
| Uvicorn | >=0.27.0 |
| Pydantic | >=2.0.0 |

## Project Structure

```text
print_order_management_activity/
|- main.py
|- models.py
|- storage.py
|- orders.json
|- requirements.txt
`- README.md
```

## Pricing

- Black & White: PHP 2.00/page
- Colored: PHP 5.00/page
- Photo Paper: PHP 20.00/page

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the API server:

```bash
python -m uvicorn main:app --reload
```

3. Open docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Data Models

### PrintType

- `black_white`
- `colored`
- `photo_paper`

### OrderCreate (Request)

| Field | Type | Required |
|-------|------|----------|
| `customer_name` | string | Yes |
| `document_name` | string | Yes |
| `pages` | integer (>0) | Yes |
| `print_type` | enum | Yes |

### Order

| Field | Type |
|-------|------|
| `order_id` | string |
| `customer_name` | string |
| `document_name` | string |
| `pages` | integer |
| `print_type` | enum |
| `total_cost` | float |
| `status` | string (`pending` or `completed`) |

## API Endpoints

- `POST /orders`
- `GET /orders`
- `GET /orders/{order_id}`
- `PATCH /orders/{order_id}/status`
- `DELETE /orders/{order_id}`
- `GET /pricing`
- `GET /`

## API Examples

### Create Order

```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Juan Dela Cruz",
    "document_name": "School Project",
    "pages": 10,
    "print_type": "colored"
  }'
```

### List Orders

```bash
curl "http://localhost:8000/orders"
```

### Get One Order

```bash
curl "http://localhost:8000/orders/A1B2C3D4"
```

### Update Status

```bash
curl -X PATCH "http://localhost:8000/orders/A1B2C3D4/status?status=completed"
```

### Delete Order

```bash
curl -X DELETE "http://localhost:8000/orders/A1B2C3D4"
```

### Get Pricing

```bash
curl "http://localhost:8000/pricing"
```

## Error Handling

- `400` invalid status
- `404` order not found
- `422` request validation errors

## Data Storage

Orders are stored in `orders.json` using JSON list format.

## CORS

CORS is enabled for all origins in `main.py`.

## License

This project is for educational purposes.
