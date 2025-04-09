import pytest
import sys
import os
# Append the project root (one directory up from tests/) to sys.path.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_table_and_get_tables():
    # Create a new table
    response = client.post("/tables/", json={"name": "Table 1", "seats": 4, "location": "Window"})
    assert response.status_code == 200
    table = response.json()
    assert table["name"] == "Table 1"

    # Get all tables
    response = client.get("/tables/")
    assert response.status_code == 200
    tables = response.json()
    assert len(tables) > 0

def test_create_reservation_conflict():
    # Create a table for reservations
    response = client.post("/tables/", json={"name": "Table 2", "seats": 4, "location": "Terrace"})
    table = response.json()
    table_id = table["id"]

    # Create an initial reservation
    reservation_data = {
        "customer_name": "John Doe",
        "table_id": table_id,
        "reservation_time": "2025-04-10T12:00:00",
        "duration_minutes": 60
    }
    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 200

    # Try to create an overlapping reservation
    overlapping_data = {
        "customer_name": "Jane Smith",
        "table_id": table_id,
        "reservation_time": "2025-04-10T12:30:00",
        "duration_minutes": 60
    }
    response = client.post("/reservations/", json=overlapping_data)
    assert response.status_code == 400
    assert "Table is already booked" in response.json()["detail"]
