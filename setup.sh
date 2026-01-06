#!/bin/bash

echo "Setting up Superheroes API..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed database
echo "Seeding database..."
python seed.py

echo "Setup complete! Run 'python app.py' to start the server."