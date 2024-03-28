
class Num :
	def __init__(self, i):
		self.i = i
	def __str__(self):
		return str(self.i)

list = [Num(0),Num(1),Num(2),Num(3),Num(4),Num(5)]

print("before: ")
for ele in list :
	print(ele)

for ele in list :
	ele.i = 9

print("after: ")
for ele in list :
	print(ele)