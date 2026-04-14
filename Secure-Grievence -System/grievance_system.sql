-- 1. Purana database delete karein (optional, fresh start ke liye)
DROP DATABASE IF EXISTS grievance_system;

-- 2. Naya Database banayein
CREATE DATABASE grievance_system;
USE grievance_system;

-- 3. Users Table banayein
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 4. Complaints Table banayein (Ab ye 'grievance_system' ke andar hi banega)
CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Submitted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;