import pytest
from src.infrastructure.models import ProductEntity
from src.application.query_handlers import ListAllProductsQueryHandler
from src.application.queries import ListAllProductsQuery

def test_list_products_query_handler(db_session):
    p1 = ProductEntity(name="Gaming Laptop", price=25000.0)
    p2 = ProductEntity(name="Mouse", price=500.0)
    db_session.add_all([p1, p2])
    db_session.commit()
    
    handler = ListAllProductsQueryHandler(session=db_session)
    result = handler.handle(ListAllProductsQuery())
    
    assert len(result) == 2
    assert result[0].name == "Gaming Laptop"
    assert result[1].price == 500.0
