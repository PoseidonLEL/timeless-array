# Timeless Array 1D

A lightweight, NumPy-based **versioned one-dimensional array** with selective historical restoration. Insert or remove elements, then rewind specific indices to values from an earlier array state without replacing the rest of the current array.

## Features

- Stores values as `numpy.float32`.
- Inserts values at a specified index or appends to the end.
- Removes values by index.
- Restores selected indices from a previous version.
- Preserves independent full-array snapshots after each supported modification.
- Uses preallocated NumPy arrays and slice assignments for insertions and deletions.

## Requirements

- Python 3
- NumPy

```bash
pip install numpy
```

## Quick start

Place `timeless_array_1D.py` in your project directory:

```python
from timeless_array_1D import timeless_array_1D

arr = timeless_array_1D([10, 20, 30])

arr.add_to_array(15, index=1)
# [10., 15., 20., 30.]

arr.remove_from_array(2)
# [10., 15., 30.]

arr.rewind([1], how_far_back=2)
# [10., 20., 30.]  (index 1 restored from the initial version)

print(arr.array)
print(len(arr.array_history))  # 4 snapshots
```

## API

| Method | Description |
| --- | --- |
| `timeless_array_1D(array)` | Initialize from a 1D array-like input, converted to `float32`. |
| `add_to_array(value, index=None, to_end=False)` | Insert one value at `index`, or append when `to_end=True`. |
| `remove_from_array(index)` | Remove one element at `index`. |
| `rewind(index, how_far_back)` | Restore the selected list of integer indices from an earlier snapshot. |
| `update_history(new_array)` | Append an array reference to the version history; intended for internal use. |

### Rewind semantics

`how_far_back=1` selects the version immediately preceding the current version. `how_far_back=2` selects the version before that.

```python
arr = timeless_array_1D([1, 2, 3])
arr.add_to_array(4, to_end=True)
arr.rewind([0, 2], how_far_back=1)
print(arr.array)  # [1. 2. 3. 4.]
```

- Rewind accepts a **1D collection of integer indices**, such as `[0, 2]`.
- If a selected index does not exist in the historical version, the method returns `"Index does not exist in this past instance!"` and leaves the array unchanged.
- An index outside the current array raises `IndexError`.
- A successful nonempty rewind creates another history version.
- Empty index collections return without creating a new version.
- Negative indices are supported according to the size of the relevant version.
- Indices refer to **positions**, not persistent element identities. Inserting or deleting elements can change what a position represents across versions.

## Storage and performance

Every modification stores a **complete independent array snapshot**, so historical restoration is exact for the stored `float32` values. Insertions, deletions, and nonempty rewinds allocate a new array and copy data.

Memory usage grows with the total size of all retained versions: approximately **4 bytes per stored element per version**, excluding Python overhead. The implementation validates a maximum rewind *depth* of 500 but **does not automatically limit the number of stored snapshots**.

For reliable history, use the provided methods rather than mutating `arr.array` or historical arrays in place. Direct mutation can bypass history tracking.

## Project status

An experimental, single-file implementation focused on straightforward version tracking and selective historical restoration.

## License

No license is included by default. Add a `LICENSE` file before distributing under specific reuse terms.
