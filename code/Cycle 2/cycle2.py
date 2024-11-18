""" 
Implement UI like shown in design
Implement Project class that does a bunch of stuff
"""
import shutil


class Project:
    def __init__(self, name: str, created: int, lastOpened: int, directory: str, type: str) -> None:
        self.__name = name
        self.__created = created
        self.__lastOpened = lastOpened
        self.__directory = directory
        self.__type = type
        
        
    def __setName__(self, name: str) -> None:
        self.__name = name
    
    
    def __setLastOpened__(self, opened: int) -> None:
        self.__lastOpened == opened
    
    
    def save(self) -> None:
        pass
    
    
    def export(self, destination: str) -> None:
        """ 
        Saves the directory of the project as a .zip file 
        to a given destination
        """
        # https://stackoverflow.com/a/25650295
        shutil.make_archive(self.__name, "zip", self.__directory, destination)
    
    
    def open(self) -> None:
        pass
    
    
    def close(self) -> None:
        pass
    
    # I think I would like to do some more on this



class FileQueue:
    def __init__(self, maxLength: int, location: str):
        self.__maxLength = maxLength
        self.__location = location
        
        self.front = 0
        self.rear = 0
        
        # counting the length to set the rear pointer. 
        # this needs to be set every time this is initially opened
        with open(location, "r") as file:
            for i in file:
                self.rear += 1
                
        # if the file has less than maxLength lines
        if self.rear <= maxLength:
            self.front = 0
        else:
            self.front = self.rear - maxLength
            
        # decrement by 1 to make it 0 indexed
        self.rear -= 1

        
    def length(self) -> int:
        """ Returns the amount of the elements in the FileQueue """
        return self.rear - self.front + 1
        
        
    def deq(self) -> str:
        """ Increments the front pointer and returns the element at the front of the FileQueue """
        
        # if the queue is empty raise an exception
        if self.length() == 0:
            raise Exception("Queue Underflow")
        
        
        self.front += 1
        
        value = ""
        
        with open(self.__location, "r") as file:
            value = file.readlines()[self.front - 1]
            
        
        # stripped to remove whitespace
        return value.strip()
    
    
    def enq(self, projectDir: str) -> None:
        """ Adds an item to the back of the FileQueue """
        # append the new project to the file
        # this happens regardless of pointers
        with open(self.__location, "a") as file:
            file.write(projectDir + "\n")
        
        
        # pointer logic
        # if the file has enough elements to be considered "full"
        if self.length() == self.__maxLength:
                
            # update front and rear pointers
            self.rear += 1
            self.front += 1
        
        else:
            
            # front does not always need to be considered  
            # eg maxLength = 4, rear = 1, front = 0
            # incrementing rear and front results in a queue of length 2 still (but should be 3)
            
            self.rear += 1
            
        # my only gripe with this implementation is that it allows for duplicates
            
            
    def drop(self) -> list:
        """ Returns all the elements in the FileQueue as a list """
        temp = []
        
        # if it is empty return an empty list
        if self.length() == 0:
            return temp
        
        
        # read from the file
        with open(self.__location, "r") as file:
            # problem with calling "file.readlines()" repeatedly
            lines = file.readlines()
            for i in range(self.front, self.rear + 1):
                # print(i)
                temp.append(lines[i].strip())
                
        return temp
