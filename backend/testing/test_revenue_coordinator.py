"""Test cases for coordinators/revenue_coordinator.py"""

import pytest
from unittest.mock import MagicMock, patch
from coordinators import revenue_coordinator

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_revenue_result():
    revenue = MagicMock()
    revenue.client_id = 10
    revenue.org_id = 1
    # By default, pretend it hasn't been received yet
    revenue.date_received = None
    return revenue

@pytest.fixture
def sample_revenue_create():
    revenue_create = MagicMock()
    revenue_create.org_id = 1
    return revenue_create

# ── add_revenue ───────────────────────────────────────────────────────────────

@patch("coordinators.revenue_coordinator.snapshot_service")
@patch("coordinators.revenue_coordinator.client_service")
@patch("coordinators.revenue_coordinator.revenue_service")
def test_add_revenue_without_date_received(mock_revenue_service, mock_client_service, mock_snapshot_service, mock_db, sample_revenue_create, mock_revenue_result):
    mock_revenue_service.add_revenue.return_value = mock_revenue_result
    
    result = revenue_coordinator.add_revenue(sample_revenue_create, mock_db)
    
    # Assert service was called
    mock_revenue_service.add_revenue.assert_called_once_with(sample_revenue_create, mock_db)
    
    # Assert reliability score was NOT updated
    mock_client_service.update_reliability_score.assert_not_called()
    
    # Assert snapshot refresh WAS called
    mock_snapshot_service.refresh_or_create.assert_called_once_with(mock_db, sample_revenue_create.org_id)
    assert result == mock_revenue_result

@patch("coordinators.revenue_coordinator.snapshot_service")
@patch("coordinators.revenue_coordinator.client_service")
@patch("coordinators.revenue_coordinator.revenue_service")
def test_add_revenue_with_date_received_triggers_reliability_scoring(mock_revenue_service, mock_client_service, mock_snapshot_service, mock_db, sample_revenue_create, mock_revenue_result):
    mock_revenue_result.date_received = "2025-06-01"
    mock_revenue_service.add_revenue.return_value = mock_revenue_result
    
    result = revenue_coordinator.add_revenue(sample_revenue_create, mock_db)
    
    # Assert both reliability scoring and snapshot refresh were invoked
    mock_client_service.update_reliability_score.assert_called_once_with(mock_db, 10)
    mock_snapshot_service.refresh_or_create.assert_called_once_with(mock_db, sample_revenue_create.org_id)

# ── update_revenue ────────────────────────────────────────────────────────────

@patch("coordinators.revenue_coordinator.snapshot_service")
@patch("coordinators.revenue_coordinator.client_service")
@patch("coordinators.revenue_coordinator.revenue_service")
def test_update_revenue_without_date_received(mock_revenue_service, mock_client_service, mock_snapshot_service, mock_db, mock_revenue_result):
    mock_revenue_service.update_revenue.return_value = mock_revenue_result
    mock_update_data = MagicMock()
    
    # Setup mock query for Clients
    mock_client_row = MagicMock()
    mock_client_row.organization_id = 1
    mock_db.query().filter().first.return_value = mock_client_row
    
    result = revenue_coordinator.update_revenue(1, mock_update_data, mock_db)
    
    mock_revenue_service.update_revenue.assert_called_once_with(1, mock_update_data, mock_db)
    mock_client_service.update_reliability_score.assert_not_called()
    mock_snapshot_service.refresh_or_create.assert_called_once_with(mock_db, 1)

@patch("coordinators.revenue_coordinator.snapshot_service")
@patch("coordinators.revenue_coordinator.client_service")
@patch("coordinators.revenue_coordinator.revenue_service")
def test_update_revenue_with_date_received(mock_revenue_service, mock_client_service, mock_snapshot_service, mock_db, mock_revenue_result):
    mock_revenue_result.date_received = "2025-06-01"
    mock_revenue_service.update_revenue.return_value = mock_revenue_result
    mock_update_data = MagicMock()
    
    mock_client_row = MagicMock()
    mock_client_row.organization_id = 1
    mock_db.query().filter().first.return_value = mock_client_row
    
    result = revenue_coordinator.update_revenue(1, mock_update_data, mock_db)
    
    mock_client_service.update_reliability_score.assert_called_once_with(mock_db, 10)
    mock_snapshot_service.refresh_or_create.assert_called_once_with(mock_db, 1)
