"""Tests for floor plan chair counter."""

import numpy as np

from main import format_output, process_floor_plan


def test_format_output_single_room():
    """Test formatting output for a single room."""
    total = {"W": 1, "P": 1, "S": 1, "C": 0}
    room_counts = {"office": {"W": 1, "P": 1, "S": 1, "C": 0}}

    result = format_output(total, room_counts)

    expected = """total:
W: 1, P: 1, S: 1, C: 0
office:
W: 1, P: 1, S: 1, C: 0"""

    assert result == expected


def test_format_output_alphabetical_sorting():
    """Test that rooms are sorted alphabetically."""
    total = {"W": 2, "P": 0, "S": 0, "C": 2}
    room_counts = {
        "zoo": {"W": 2, "P": 0, "S": 0, "C": 0},
        "bar": {"W": 0, "P": 0, "S": 0, "C": 2},
    }

    result = format_output(total, room_counts)

    expected = """total:
W: 2, P: 0, S: 0, C: 2
bar:
W: 0, P: 0, S: 0, C: 2
zoo:
W: 2, P: 0, S: 0, C: 0"""

    assert result == expected


def test_process_floor_plan_simple():
    """Test processing a simple floor plan."""
    floor_plan = """+-------------+
|             |
| (office)    |
|             |
|   W  P  S   |
|             |
+-------------+"""

    lines = floor_plan.split("\n")
    max_len = max(len(line) for line in lines)
    grid = np.array([list(line.ljust(max_len)) for line in lines])

    result = process_floor_plan(grid)

    expected = """total:
W: 1, P: 1, S: 1, C: 0
office:
W: 1, P: 1, S: 1, C: 0"""

    assert result == expected


def test_process_floor_plan_two_rooms():
    """Test processing floor plan with two rooms."""
    floor_plan = """+-------+-------+
|       |       |
| (zoo) | (bar) |
|       |       |
|  W W  |  C C  |
|       |       |
+-------+-------+"""

    lines = floor_plan.split("\n")
    max_len = max(len(line) for line in lines)
    grid = np.array([list(line.ljust(max_len)) for line in lines])

    result = process_floor_plan(grid)

    # Rooms should be alphabetically sorted (bar before zoo)
    assert "bar:" in result
    assert "zoo:" in result
    assert result.index("bar:") < result.index("zoo:")
    assert "W: 2" in result
    assert "C: 2" in result
