
import mysql.connector
import matplotlib.pyplot as plt
from getpass import getpass

print("DS SALES MANAGEMENT SYSTEM")
print("SALES CHARTS AND VISUALIZATION")

password = getpass("Enter MySQL password: ")

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="ds_sales_management"
    )

    cursor = connection.cursor()

    # 1. CATEGORY WISE REVENUE

    cursor.execute("""
        SELECT p.category,
        SUM(s.quantity * p.price)
        FROM sales s
        JOIN products p
        ON s.product_id = p.product_id
        GROUP BY p.category
    """)

    category_data = cursor.fetchall()

    categories = [row[0] for row in category_data]
    revenues = [float(row[1]) for row in category_data]

    plt.figure(figsize=(8, 5))
    plt.bar(categories, revenues)
    plt.title("Category Wise Sales Revenue")
    plt.xlabel("Product Category")
    plt.ylabel("Revenue (Rs.)")
    plt.tight_layout()
    plt.savefig("category_revenue.png")
    plt.show()

    # 2. PRODUCT WISE QUANTITY SOLD

    cursor.execute("""
        SELECT p.product_name, SUM(s.quantity)
        FROM sales s
        JOIN products p
        ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
    """)

    product_data = cursor.fetchall()

    products = [row[0] for row in product_data]
    quantities = [int(row[1]) for row in product_data]

    plt.figure(figsize=(9, 5))
    plt.bar(products, quantities)
    plt.title("Product Wise Sales")
    plt.xlabel("Products")
    plt.ylabel("Quantity Sold")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("product_sales.png")
    plt.show()

    print("Charts created successfully!")

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("Database Error:", error)

except Exception as error:
    print("Error:", error)
