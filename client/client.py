import requests

URL = "http://127.0.0.1:8000"

def view():
    response = requests.get(f"{URL}/orders")
    data = response.json()
    orders = data.get("orders", [])

    print("\nList of Orders")
    if not orders:
        print("No orders yet.")
        return

    for order in orders:
        print(f"ID: {order['order_id']} | Name: {order['customer_name']} | Doc: {order['document_name']} | Type: {order['print_type']} | Pages: {order['pages']} | Status: {order['status']} | Total: PHP {order['total_cost']:.2f}")


def search(order_id):
    response = requests.get(f"{URL}/orders/{order_id}")
    if response.status_code != 200:
        print("Not Found")
        return

    order = response.json().get("order", {})
    print(f"Name: {order.get('customer_name')} | Doc: {order.get('document_name')} | Type: {order.get('print_type')} | Pages: {order.get('pages')} | Total: PHP {order.get('total_cost')} | Status: {order['status']}")


def create(customer_name, document_name, print_type, pages):
    payload = {
        "customer_name": customer_name,
        "document_name": document_name,
        "print_type": print_type,
        "pages": int(pages),
    }
    response = requests.post(f"{URL}/orders", json=payload)
    data = response.json()

    if response.status_code == 200:
        order = data.get("order", {})
        print(f"Document Name: {order.get('document_name')} | Total: PHP {order.get('total_cost')}")
    else:
        print(data.get("detail", "Oh no... it failed :("))


def update(order_id, status):
    response = requests.patch(f"{URL}/orders/{order_id}/status", params={"status": status})
    if response.status_code == 200:
        print("Status updated")
    else:
        print(response.json().get("detail", "Update failed"))


def remove(order_id):
    response = requests.delete(f"{URL}/orders/{order_id}")
    if response.status_code == 200:
        print("Deleted")
    else:
        print(response.json().get("detail", "Delete failed"))


def menu():
    while True:
        print("\n=== Print Client ===")
        print("1. View orders")
        print("2. Search order by ID")
        print("3. Create order")
        print("4. Update order status")
        print("5. Delete order")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            view()
        
        elif choice == "2":
            order_id = input("Order ID: ").strip()
            search(order_id)
        
        elif choice == "3":
            name = input("Customer name: ").strip()
            doc = input("Document name: ").strip()
            ptype = input("Type (black_white/colored/photo_paper): ").strip()
            pages = input("Pages: ").strip()
            try:
                create(name, doc, ptype, pages)
            except ValueError:
                print("Invalid pages")
        
        elif choice == "4":
            order_id = input("Order ID: ").strip()
            status = input("Status (pending/completed): ").strip()
            update(order_id, status)
        
        elif choice == "5":
            order_id = input("Order ID: ").strip()
            remove(order_id)
        
        elif choice == "0":
            break
        
        else:
            print("Invalid choice")


def main():
    menu()


if __name__ == "__main__":
    main()

