
CREATE DATABASE IF NOT EXISTS ds_sales_management;

USE ds_sales_management;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

INSERT IGNORE INTO customers
(customer_id, customer_name, email, city)
VALUES
(1,'Arun','arun@gmail.com','Chennai'),
(2,'Priya','priya@gmail.com','Madurai'),
(3,'Kumar','kumar@gmail.com','Coimbatore'),
(4,'Meena','meena@gmail.com','Salem'),
(5,'Ravi','ravi@gmail.com','Trichy');

INSERT IGNORE INTO products
(product_id, product_name, category, price)
VALUES
(1,'Laptop','Electronics',40000),
(2,'Mouse','Accessories',500),
(3,'Keyboard','Accessories',1000),
(4,'Monitor','Electronics',12000),
(5,'Headphones','Electronics',2000);

INSERT IGNORE INTO sales
(sale_id, customer_id, product_id, quantity, sale_date)
VALUES
(1,1,1,2,'2026-10-01'),
(2,2,2,5,'2026-10-03'),
(3,3,3,3,'2026-10-05'),
(4,4,4,1,'2026-10-08'),
(5,5,5,4,'2026-10-10');
