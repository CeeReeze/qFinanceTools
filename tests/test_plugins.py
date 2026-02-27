from qfinancetools.core.plugins import discover_plugins


def test_discover_plugins_returns_snapshot() -> None:
    snapshot = discover_plugins()
    assert snapshot.plugins is not None
