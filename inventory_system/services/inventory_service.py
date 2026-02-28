from database.connection import get_connection

class InventoryService:
    def add_product(self, name, quantity, price):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
            (name, quantity, price)
        )
        conn.commit()
        conn.close()

    def view_products(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_product(self, product_id, quantity, price):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET quantity=?, price=? WHERE id=?",
            (quantity, price, product_id)
        )
        conn.commit()
        conn.close()

    def delete_product(self, product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
