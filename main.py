"""
Floor Plan Chair Counter

A command-line tool that reads apartment floor plans and counts different types
of chairs per room.
"""

from collections import deque
import re

import click
import numpy as np
from scipy.ndimage import label as scipy_label


CHAIR_TYPES = ["W", "P", "S", "C"]
WALL_CHARS = {"+", "-", "|", "/"}


def parse_floor_plan(file_path: str) -> np.ndarray:
    """Read and parse a floor plan file into a 2D character array.

    Args:
        file_path: Path to the floor plan text file.

    Returns:
        2D numpy array of characters representing the floor plan.
    """
    with open(file_path) as f:
        lines = f.readlines()

    max_len = max(len(line.rstrip("\n")) for line in lines)
    grid = [list(line.rstrip("\n").ljust(max_len)) for line in lines]
    return np.array(grid)


def find_rooms(grid: np.ndarray) -> dict[str, tuple[int, int]]:
    """Find room names and their positions by searching for (name) patterns.

    Args:
        grid: 2D character array representing the floor plan.

    Returns:
        Dictionary mapping room names to their (row, col) positions.
    """
    rooms = {}
    for row_idx, row in enumerate(grid):
        line = "".join(row)
        for match in re.finditer(r"\(([^)]+)\)", line):
            rooms[match.group(1)] = (row_idx, match.start())
    return rooms


def flood_fill(array: np.ndarray, start: tuple[int, int], label: int) -> None:
    """Label a connected region using BFS flood fill.

    Args:
        array: 2D integer array where 1 = unlabeled walkable, 0 = wall.
        start: Starting position (row, col) for the flood fill.
        label: Integer label to assign to the connected region.
    """
    queue = deque([start])
    rows, cols = array.shape

    while queue:
        row, col = queue.popleft()  # use pop() for DFS instead
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and array[nr, nc] == 1:
                array[nr, nc] = label
                queue.append((nr, nc))


def label_rooms(walkable: np.ndarray, rooms: dict[str, tuple[int, int]]) -> np.ndarray:
    """Assign unique labels to each room region.

    Args:
        walkable: Boolean array where True = walkable space.
        rooms: Dictionary mapping room names to positions.

    Returns:
        Integer array with unique labels for each room.
    """
    labels = walkable.astype(int)
    current_label = 2
    for _, (row, col) in rooms.items():
        flood_fill(labels, (row, col), current_label)
        current_label += 1
    return labels


def count_chairs(
    room_array: np.ndarray, labels: np.ndarray, rooms: dict[str, tuple[int, int]]
) -> tuple[dict[str, int], dict[str, dict[str, int]]]:
    """Count chairs per room and total.

    Args:
        room_array: Original character grid.
        labels: Labeled regions array.
        rooms: Dictionary mapping room names to positions.

    Returns:
        Tuple of (total_counts, room_counts) dictionaries.
    """
    total = {ch: 0 for ch in CHAIR_TYPES}
    room_counts = {}

    for name, (row, col) in rooms.items():
        room_label = labels[row, col]
        mask = labels == room_label
        counts = {ch: int(np.sum(room_array[mask] == ch)) for ch in CHAIR_TYPES}
        room_counts[name] = counts
        for ch in CHAIR_TYPES:
            total[ch] += counts[ch]

    return total, room_counts


def format_counts(counts: dict[str, int]) -> str:
    """Format chair counts as comma-separated string."""
    return ", ".join(f"{ch}: {counts[ch]}" for ch in CHAIR_TYPES)


def print_debug(walkable: np.ndarray, labels: np.ndarray) -> None:
    """Print intermediate arrays for debugging."""
    print("Walkable areas (1 = walkable, 0 = wall):")
    for row in walkable.astype(int):
        print("".join(str(x) for x in row))
    print()
    print("Labeled regions:")
    for row in labels:
        print("".join(str(x) for x in row))
    print()


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--debug", is_flag=True, help="Print intermediate debug states")
def main(file: str, debug: bool) -> None:
    """Count chairs per room in an apartment floor plan.

    FILE: Path to a floor plan text file.
    """
    room_array = parse_floor_plan(file)
    rooms = find_rooms(room_array)
    walkable = np.isin(room_array, list(WALL_CHARS), invert=True)

    # scipy's efficient flood fill implementation
    # For completeness, I also implemented my own version:
    # labels = label_rooms(walkable, rooms)
    labels, _ = scipy_label(walkable, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])

    if debug:
        print_debug(walkable, labels)

    total, room_counts = count_chairs(room_array, labels, rooms)

    print("total:")
    print(format_counts(total))
    for name in sorted(room_counts.keys()):
        print(f"{name}:")
        print(format_counts(room_counts[name]))


if __name__ == "__main__":
    main()
