
import mysql.connector
from getpass import getpass

print("=" * 50)
print("       DS SALES MANAGEMENT SYSTEM")
print("            SALES ANALYSIS")
print("=" * 50)

password = getpass("Enter MySQL password: ")

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="ds_sales_management"
    )

    cursor = connection.cursor()

    print("\nMYSQL CONNECTION SUCCESSFUL!")

    # 1. TOTAL REVENUE

    cursor.execute("""
        SELECT SUM(s.quantity * p.price)
        FROM sales s
        JOIN products p
        ON s.product_id = p.product_id
    """)

    revenue = cursor.fetchone()[0]

    print("\n1. TOTAL REVENUE: Rs.", revenue)

    # 2. TOTAL PRODUCTS SOLD

    cursor.execute("""
        SELECT SUM(quantity)
        FROM sales
    """)

    total_quantity = cursor.fetchone()[0]

    print("2. TOTAL PRODUCTS SOLD:", total_quantity)

    # 3. TOTAL SALES RECORDS

    cursor.execute("""
        SELECT COUNT(*)
        FROM sales
    """)

    total_sales = cursor.fetchone()[0]

    print("3. TOTAL SALES RECORDS:", total_sales)

    # 4. AVERAGE SALES VALUE

    average = revenue / total_sales if total_sales else 0

    print("4. AVERAGE SALES VALUE: Rs.", round(average, 2))

    # 5. BEST SELLING PRODUCT

    cursor.execute("""
        SELECT p.product_name, SUM(s.quantity) AS total_sold
        FROM sales s
        JOIN products p
        ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_sold DESC
        LIMIT 1
    """)

    best_product = cursor.fetchone()

    print("\n5. BEST SELLING PRODUCT:")
    print("Product:", best_product[0])
    print("Quantity Sold:", best_product[1])

    # 6. CATEGORY WISE REVENUE

    cursor.execute("""
        SELECT p.category,
        SUM(s.quantity * p.price) AS category_revenue
        FROM sales s
        JOIN products p
        ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY category_revenue DESC
    """)

    categories = cursor.fetchall()

    print("\n6. CATEGORY WISE REVENUE")

    for category in categories:
        print(category[0], ":", "Rs.", category[1])

    print("\n" + "=" * 50)
    print("       SALES ANALYSIS COMPLETED")
    print("=" * 50)

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("\nDATABASE ERROR:", error)
