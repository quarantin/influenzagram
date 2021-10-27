CREATE DATABASE influenzagram;
CREATE USER 'influenzagram'@'%' IDENTIFIED BY 'influenzagram';
GRANT ALL PRIVILEGES ON influenzagram.* TO 'influenzagram'@'%';
