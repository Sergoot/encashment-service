from src.atm.utils import get_radius_range

import pytest


def test_default_radius():
    result = get_radius_range(55.7558, 37.6173)  # Coordinates for Moscow
    assert pytest.approx(result['lat_min'], rel=1e-4) == 55.7549
    assert pytest.approx(result['lat_max'], rel=1e-4) == 55.7567
    assert pytest.approx(result['long_min'], rel=1e-4) == 37.6164
    assert pytest.approx(result['long_max'], rel=1e-4) == 37.6182


def test_negative_coordinates():
    result = get_radius_range(-34.6037, -58.3816)  # Coordinates for Buenos Aires
    assert pytest.approx(result['lat_min'], rel=1e-4) == -34.6046
    assert pytest.approx(result['lat_max'], rel=1e-4) == -34.6028
    assert pytest.approx(result['long_min'], rel=1e-4) == -58.3825
    assert pytest.approx(result['long_max'], rel=1e-4) == -58.3807


def test_zero_radius():
    result = get_radius_range(40.7128, -74.0060, 0)  # New York with zero radius
    assert result['lat_min'] == result['lat_max'] == 40.7128
    assert result['long_min'] == result['long_max'] == -74.0060
