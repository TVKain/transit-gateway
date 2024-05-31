# File: test_example.py


def add(a, b):
    """Function to add two numbers."""
    return a + b


def test_addition():
    """Test the add function."""
    assert add(2, 2) == 4
