filename = "test.txt"

x = 5

with open(filename, "r") as file:
    for i in range(x):
        print(file.readlines()[i].strip())
        
# Output (Bad)

# England
# IndexError: list index out of range
        

with open(filename, "r") as file:
    lines = file.readlines()
    for i in range(x):
        print(lines[i].strip())
        
# Output (Good)

# England
# Spain  
# France 
# Germany
# Poland

