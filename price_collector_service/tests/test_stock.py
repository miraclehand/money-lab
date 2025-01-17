import pytest
from unittest.mock import patch
from app import fetch_and_save_stock_data, collection

@patch('app.requests.get')
def test_fetch_and_save_stock_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'stock': 'data'}
    
    fetch_and_save_stock_data()
    assert collection.count_documents({}) > 0

@patch('app.requests.get')
def test_fetch_fail(mock_get):
    mock_get.return_value.status_code = 500
    fetch_and_save_stock_data()
    assert collection.count_documents({}) == 0

