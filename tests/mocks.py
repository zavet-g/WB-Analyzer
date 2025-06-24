from collections.abc import Callable


class MockObject:
    """MockObject."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clear(self):
        """clear."""
        pass


class MockDependencyObject(MockObject):
    """MockDependencyObject."""

    data: Callable

    def dependency(self, *args, **kwargs):
        """dependency."""
        return self.data
