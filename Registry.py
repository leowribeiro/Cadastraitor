
import winreg
import sys

class WinRegistry :

	def __init__(self):
		name = sys.argv[0][2:-3]
		newName = ""
		if name[0].islower():
			newName = name[0].upper() + name[1:]
		else:
			newName = name
			
		self.key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + newName)
	
	def setKey(self, key, value) :
		if isinstance(value, int):
			winreg.SetValueEx(self.key, key, 0, winreg.REG_QWORD, value)
		elif isinstance(value, str):
			winreg.SetValueEx(self.key, key, 0, winreg.REG_SZ, value)
		else:
			winreg.SetValueEx(self.key, key, 0, winreg.REG_BINARY, value)	
			# raise Exception("Type of value given cannot be storaged in registry.")

	def getKey(self, key) :
		return winreg.QueryValueEx(self.key, key)[0]


# example of usage
# wr = WinRegistry()
# wr.setKey("Number", 777)
# print(wr.getKey("Number"))
# wr.setKey("String", "Hello")
# print(wr.getKey("String"))
