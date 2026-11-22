import numpy as np
class timeless_array_1D:

    '''----INITIAL OBJECT DEFINITION & BOOTUP----'''

    def __init__(self, array):
        self.array = np.float32(array) #Initial array
        if(self.array.ndim!=1):
            raise ValueError("Input must be a 1D array!")
        self.array_history = [self.array.copy()] #Starts the array history with the initial array


    '''----ARRAY MODIFICATION OPERATIONS----'''

    #Adds a new value at a specified index or directly to the end of the array.
    #Allocates the output once instead of using np.insert to minimize overhead.
    def add_to_array(self,value,index=None,to_end=False):
        arraySize = self.array.size
        if(to_end):
            index = arraySize
        elif(index is None):
            raise TypeError("An index is required unless to_end is True!")

        if(not isinstance(index,(int,np.integer)) or isinstance(index,(bool,np.bool_))):
            raise TypeError("index must be an integer!")
        if(index<0):
            index += arraySize
        if(index<0 or index>arraySize):
            raise IndexError("Index is outside the array!")

        newArray = np.empty(arraySize+1,dtype=np.float32)
        newArray[:index] = self.array[:index]
        newArray[index] = value
        newArray[index+1:] = self.array[index:]

        self.array = newArray
        self.update_history(newArray)


    #Removes a value at the specified index, shifting following values to the left.
    def remove_from_array(self,index):
        arraySize = self.array.size
        if(not isinstance(index,(int,np.integer)) or isinstance(index,(bool,np.bool_))):
            raise TypeError("index must be an integer!")
        if(index<0):
            index += arraySize
        if(index<0 or index>=arraySize):
            raise IndexError("Index is outside the array!")

        newArray = np.empty(arraySize-1,dtype=np.float32)
        newArray[:index] = self.array[:index]
        newArray[index:] = self.array[index+1:]

        self.array = newArray
        self.update_history(newArray)


    #Rewinds selected indices to values from a previous version of the array.
    #A depth of 1 retrieves the version immediately before the current one.
    def rewind(self,index,how_far_back):
        if(not isinstance(how_far_back,(int,np.integer)) or isinstance(how_far_back,(bool,np.bool_))):
            raise TypeError("how_far_back must be an integer!")
        if(how_far_back>=len(self.array_history)):
            raise IndexError("Requested history instance does not exist!")

        indices = np.asarray(index)
        if(indices.ndim!=1 or not np.issubdtype(indices.dtype,np.integer)):
            raise TypeError("index must be a 1D list of integers!")
        if(indices.size==0):
            return

        pastArray = self.array_history[-1-how_far_back]
        if(np.any(indices>=pastArray.size) or np.any(indices < -pastArray.size)):
            return "Index does not exist in this past instance!"
        if(np.any(indices>=self.array.size) or np.any(indices < -self.array.size)):
            raise IndexError("Index is outside the current array!")

        newArray = self.array.copy() #Never modify an earlier history instance in-place
        newArray[indices] = pastArray[indices]

        self.array = newArray
        self.update_history(newArray)


    '''----ARRAY HISTORY MANAGEMENT----'''

    #Adds the new array instance to the history. Every modification allocates a
    #new array, so the history can retain it without an additional full copy.
    def update_history(self,new_array):
        self.array_history.append(new_array)
