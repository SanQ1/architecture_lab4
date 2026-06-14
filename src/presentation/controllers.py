from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.application.commands import (
    RegisterUserCommand,
    CreateOrderCommand,
    AddProductCommand,
    DeleteProductCommand,
    DeleteOrderCommand
)
from src.application.queries import GetUserByIdQuery, ListAllProductsQuery, LoginQuery
from src.application.command_handlers import (
    RegisterUserCommandHandler,
    CreateOrderCommandHandler,
    AddProductCommandHandler,
    DeleteProductCommandHandler,
    DeleteOrderCommandHandler
)
from src.application.query_handlers import (
    GetUserByIdQueryHandler,
    ListAllProductsQueryHandler,
    LoginQueryHandler
)
from src.domain.errors import DomainError

api_bp = Blueprint("api", __name__)



@api_bp.route("/users/register", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    
    command = RegisterUserCommand(
        username=data.get("username"),
        password=data.get("password")
    )
    
    handler = RegisterUserCommandHandler(
        uow=current_app.uow, 
        factory=current_app.user_factory
    )
    
    try:
        user_id = handler.handle(command)
        return jsonify({"id": user_id}), 201
    except DomainError as e:
        return jsonify({"message": str(e)}), 400


@api_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    query = LoginQuery(
        username=data.get('username'),
        password=data.get('password')
    )

    handler = LoginQueryHandler(session=current_app.db.session)

    try:
        read_model = handler.handle(query)
        return jsonify(access_token=read_model.access_token), 200
    except DomainError as e:
        return jsonify({"message": str(e)}), 401


@api_bp.route("/users/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    
    query = GetUserByIdQuery(user_id=user_id)
    
    handler = GetUserByIdQueryHandler(session=current_app.db.session)
    read_model = handler.handle(query)
    
    if not read_model:
        return jsonify({"message": "Користувача не знайдено"}), 404
        
    return jsonify({
        "id": read_model.id,
        "username": read_model.username
    }), 200


# ORDERS CONTROLLERS

@api_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    
    command = CreateOrderCommand(
        items=data.get("items", []),
        user_id=user_id
    )
    
    handler = CreateOrderCommandHandler(
        uow=current_app.uow, 
        factory=current_app.order_factory
    )
    
    try:
        order_id = handler.handle(command)
        return jsonify({"id": order_id}), 201
    except DomainError as e:
        return jsonify({"message": str(e)}), 400


@api_bp.route("/orders/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id: int):
    command = DeleteOrderCommand(order_id=order_id)
    
    handler = DeleteOrderCommandHandler(uow=current_app.uow)
    
    try:
        handler.handle(command)
        return jsonify({"message": "Замовлення успішно видалено"}), 200
    except DomainError as e:
        return jsonify({"message": str(e)}), 404


# PRODUCTS CONTROLLERS

@api_bp.route("/products", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json() or {}
    
    command = AddProductCommand(
        name=data.get("name"),
        price=data.get("price")
    )
    
    handler = AddProductCommandHandler(uow=current_app.uow)
    
    try:
        product_id = handler.handle(command)
        return jsonify({"id": product_id}), 201
    except DomainError as e:
        return jsonify({"message": str(e)}), 400


@api_bp.route("/products", methods=["GET"])
def get_products():
    query = ListAllProductsQuery()
    
    handler = ListAllProductsQueryHandler(session=current_app.db.session)
    products_list = handler.handle(query)
    
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price} 
        for p in products_list
    ]), 200


@api_bp.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id: int):
    command = DeleteProductCommand(product_id=product_id)
    
    handler = DeleteProductCommandHandler(uow=current_app.uow)
    
    try:
        handler.handle(command)
        return jsonify({"message": "Продукт успішно видалено"}), 200
    except DomainError as e:
        return jsonify({"message": str(e)}), 404
