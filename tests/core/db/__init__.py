import pytest
from unittest.mock import AsyncMock, Mock
from app.core.db import DBConnection

@pytest.fixture
def mock_connection():
    mock_conn = Mock(spec=DBConnection)
    mock_conn.execute = AsyncMock()
    return mock_conn
