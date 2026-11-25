
from flask import Flask, render_template_string, send_from_directory
import mysql.connector
from getpass import getpass
import os

app = Flask(__name__)

# MySQL password
DB_PASSWORD = getpass("Enter MySQL password: ")

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD,
        database="ds_sales_management"
    )


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DS Sales Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f5f9;
            margin: 0;
            padding: 25px;
        }

        h1 {
            color: #17365d;
            text-align: center;
        }

        .container {
            max-width: 1100px;
            margin: auto;
        }

        .cards {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px #ccc;
            text-align: center;
        }

        .card h2 {
            color: #2471a3;
        }

        .card p {
            font-size: 24px;
            font-weight: bold;
        }

        table {
            width: 100%;
            background: white;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 13px;
            border: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #17365d;
            color: white;
        }

        .charts {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 25px;
        }

        .charts img {
            width: 100%;
            max-width: 480px;
            background: white;
            border-radius: 10px;
        }
    </style>
</head>

<body>
<div class="container">

    <h1>DS SALES MANAGEMENT SYSTEM</h1>
    <h3 style="text-align:center">
        Sales Management Dashboard
    </h3>

    <div class="cards">

        <div class="card">
            <h2>Total Revenue</h2>
            <p>₹{{ revenue }}</p>
        </div>

        <div class="card">
            <h2>Total Customers</h2>
            <p>{{ customers }}</p>
        </div>

        <div class="card">
            <h2>Total Products</h2>
            <p>{{ products }}</p>
        </div>

        <div class="card">
            <h2>Total Sales</h2>
            <p>{{ sales }}</p>
        </div>

    </div>

    <h2>Sales Details</h2>

    <table>
        <tr>
            <th>Sale ID</th>
            <th>Customer</th>
            <th>Product</th>
            <th>Quantity</th>
            <th>Total Amount</th>
            <th>Date</th>
        </tr>

        {% for row in records %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>₹{{ row[4] }}</td>
            <td>{{ row[5] }}</td>
        </tr>
        {% endfor %}
    </table>

    <h2>Sales Charts</h2>

    <div class="charts">
        {% if category_chart %}
        <img src="/charts/category_revenue.png">
        {% endif %}

        {% if product_chart %}
        <img src="/charts/product_sales.png">
        {% endif %}
    </div>

</div>
</body>
</html>
"""


@app.route("/")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT SUM(s.quantity * p.price)
            FROM sales s
            JOIN products p
            ON s.product_id = p.product_id
        """)
        revenue = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM customers")
        customers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sales")
        sales = cursor.fetchone()[0]

        cursor.execute("""
            SELECT s.sale_id, c.customer_name,
                   p.product_name, s.quantity,
                   s.quantity * p.price, s.sale_date
            FROM sales s
            JOIN customers c
            ON s.customer_id = c.customer_id
            JOIN products p
            ON s.product_id = p.product_id
            ORDER BY s.sale_id
        """)

        records = cursor.fetchall()

        return render_template_string(
            HTML,
            revenue=f"{float(revenue):,.2f}",
            customers=customers,
            products=products,
            sales=sales,
            records=records,
            category_chart=os.path.exists("category_revenue.png"),
            product_chart=os.path.exists("product_sales.png")
        )

    finally:
        cursor.close()
        connection.close()


@app.route("/charts/<filename>")
def chart_file(filename):
    return send_from_directory(
        os.getcwd(), filename
    )


if __name__ == "__main__":
    print("Starting DS Sales Management System...")
    app.run(debug=False)
