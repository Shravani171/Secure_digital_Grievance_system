-- Create the database
CREATE DATABASE IF NOT EXISTS grievance_portal;

-- Use the database
USE grievance_portal;

-- Create User table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Create Complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    phone_no VARCHAR(15),
    location VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    status VARCHAR(50) DEFAULT 'Submitted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;