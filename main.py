
import mysql.connector
from getpass import getpass

print("DS SALES MANAGEMENT SYSTEM")
print("==========================")

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

    query = """
    SELECT
        s.sale_id,
        c.customer_name,
        p.product_name,
        p.category,
        s.quantity,
        p.price,
        s.quantity * p.price AS total_amount,
        s.sale_date
    FROM sales s
    JOIN customers c
        ON s.customer_id = c.customer_id
    JOIN products p
        ON s.product_id = p.product_id
    ORDER BY s.sale_id;
    """

    cursor.execute(query)

    records = cursor.fetchall()

    print("\nSALES DETAILS")
    print("=" * 90)

    for row in records:
        print(
            "Sale ID:", row[0],
            "| Customer:", row[1],
            "| Product:", row[2],
            "| Quantity:", row[4],
            "| Total:", row[6]
        )

    print("\nTotal Sales Records:", len(records))

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("Error:", error)
