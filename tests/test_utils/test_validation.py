import pytest

from pystream.constants import PACKET_HEADER_SIZE, PACKET_MAX_SIZE
from pystream.exceptions import InvalidPacketSizeError, InvalidIPAddressError, InvalidPortError
from pystream.utils.validation import validate_ipv4_address, validate_port, validate_packet_size


@pytest.mark.parametrize("value", [None, 0, True, 3.14])
def test_validate_ipv4_address_with_invalid_type(value):
    with pytest.raises(InvalidIPAddressError):
        validate_ipv4_address(value)


@pytest.mark.parametrize("value", ["abc", "00.1.3", "f03rf", "-1.-1.-1.-1", "300.1.1.1"])
def test_validate_ipv4_address_with_invalid_format(value):
    with pytest.raises(InvalidIPAddressError):
        validate_ipv4_address(value)


@pytest.mark.parametrize("value", ["192.168.0.1", "8.8.8.8", "32.32.32.255"])
def test_validate_ipv4_address_with_valid_format(value):
    assert validate_ipv4_address(value) is None


@pytest.mark.parametrize("value", ["", 3.14, True, None])
def test_validate_port_with_invalid_type(value):
    with pytest.raises(InvalidPortError):
        validate_port(value)


@pytest.mark.parametrize("value", [-1, 65536])
def test_validate_port_with_invalid_range(value):
    with pytest.raises(InvalidPortError):
        validate_port(value)


@pytest.mark.parametrize("value", [0, 100, 1000, 10000])
def test_validate_port_with_valid_range(value):
    assert validate_port(value) is None


@pytest.mark.parametrize("value", ["", None, 3.14])
def test_validate_packet_size_with_invalid_type(value):
    with pytest.raises(InvalidPacketSizeError):
        validate_packet_size(value)


@pytest.mark.parametrize("value", [-1, 0, PACKET_MAX_SIZE])
def test_validate_packet_size_with_invalid_range(value):
    with pytest.raises(InvalidPacketSizeError):
        validate_packet_size(value)


@pytest.mark.parametrize("value", [1, 50000, PACKET_MAX_SIZE - PACKET_HEADER_SIZE])
def test_validate_packet_size_with_valid_range(value):
    assert validate_packet_size(value) is None
