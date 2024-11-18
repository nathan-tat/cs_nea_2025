from cycle2 import FileQueue


q = FileQueue(4, "q.txt")

q.enq("Hello")
q.enq("World")
q.enq("!!!")
q.enq("Nathan")
q.enq("Ta")

q.deq()
q.deq()



print(q.drop())