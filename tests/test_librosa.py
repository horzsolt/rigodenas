import sys
import pytest
import src.mirhelper

@pytest.mark.skip(reason="Slow test (> 1 min), skipping")
def test_get_beat():
    mirhelper.get_beat(None)