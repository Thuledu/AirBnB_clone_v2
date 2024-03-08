#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static.

# Install Nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
  sudo apt update
  sudo apt install nginx -y
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
sudo chown -R ubuntu:ubuntu /data

# Create a fake HTML file for testing
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Update Nginx configuration
config="server {
    listen 80;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current;
    }
}"
echo "$config" | sudo tee /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

# Exit successfully
exit 0
