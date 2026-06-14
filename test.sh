#!/bin/bash

source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:.

echo "=== Тестування домену та команд. ==="
pytest tests/unit

echo "=== Тестування запитів. ==="
pytest tests/integration
