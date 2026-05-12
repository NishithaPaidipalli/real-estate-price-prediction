from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_prediction_logic():
    # Test with sample data
    payload = {
        "Area": 1500, "Bedrooms": 3, "Bathrooms": 2, 
        "Age": 10, "Location": "Suburb", "Property_Type": "House"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "Price_Estimate" in response.json()
