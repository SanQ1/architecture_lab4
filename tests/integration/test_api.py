import pytest
from src.infrastructure.models import ProductEntity

def test_create_order_api_success(client, auth_headers, db_session):
    with client.application.app_context():
        from src.infrastructure.models import UserEntity
        user = db_session.query(UserEntity).filter_by(id="test-user-id").first()
        assert user is not None, "User should be created by auth_headers fixture"

    payload = {"items": ["Mouse"]}
    response = client.post('/api/v1/orders', json=payload, headers=auth_headers)

    if response.status_code == 400:
        print(response.get_json())

    assert response.status_code == 201

def test_list_products_api(client, db_session):
    with client.application.app_context():
        product = ProductEntity(name="Keyboard", price=100.0)
        db_session.add(product)
        db_session.commit()
    
    response = client.get('/api/v1/products')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Keyboard"
