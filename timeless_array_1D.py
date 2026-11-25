import numpy as np
from operator import index as integer_index


class timeless_array_1D:

    def __init__(self, array):
        self.array = np.array(array, dtype=np.float32, copy=True)
        if (self.array.ndim != 1):
            raise ValueError("Expected a 1D array.")
        self.array_history = [self.array.copy()]

    #Insert one value, or ignore index and append it to the end.
    def add_to_array(self,value,index=None,to_end=False):
        size = self.array.size
        position = size if to_end else integer_index(index)
        if (position < -size or position > size):
            raise IndexError("Insertion index out of range.")
        if (np.ndim(value) != 0):
            raise ValueError("Expected one scalar value.")
        if (position < 0):
            position += size

        updated = np.empty(size + 1, dtype=self.array.dtype)
        updated[:position] = self.array[:position]
        updated[position] = value
        updated[position+1:] = self.array[position:]
        self.update_history(updated)
        self.array = updated

    def remove_from_array(self,index):
        updated = np.delete(self.array, integer_index(index))
        self.update_history(updated)
        self.array = updated

    #One step back selects the snapshot before the current one.
    def rewind(self,index=None,how_far_back=None,revert_entire_array=False):
        if (how_far_back is None):
            raise TypeError("Provide how_far_back.")
        steps = integer_index(how_far_back)
        if (steps < 0 or steps >= len(self.array_history)):
            raise IndexError("Requested history is out of range.")
        past = self.array_history[-1-steps]
        if (revert_entire_array):
            updated = past.copy()
            self.update_history(updated)
            self.array = updated
            return

        positions = np.asarray(index)
        if (positions.ndim != 1 or (positions.size and positions.dtype.kind not in 'iu')):
            raise TypeError("Expected a list of integer indices.")
        if (positions.size and (int(positions.min()) < -past.size or
                               int(positions.max()) >= past.size)):
            raise IndexError("Index does not exist in this past instance!")
        positions = positions.astype(np.intp, copy=False)
        self.array[positions] = past[positions]
        self.update_history(self.array)

    def update_history(self,new_array):
        snapshot = np.array(new_array, dtype=np.float32, copy=True)
        if (snapshot.ndim != 1):
            raise ValueError("Expected a 1D array.")
        self.array_history.append(snapshot)
