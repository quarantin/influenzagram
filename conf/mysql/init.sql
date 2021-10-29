CREATE DATABASE influenzagram CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER IF NOT EXISTS 'influenzagram'@'%' IDENTIFIED BY 'influenzagram';
GRANT ALL PRIVILEGES ON influenzagram.* TO 'influenzagram'@'%';
