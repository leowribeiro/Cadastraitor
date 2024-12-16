
import zlib

file = open("config.ini", "r")
content = file.read()
file.close()

file = open("compressed.ini", "wb")
file.write(zlib.compress(content.encode("utf-8")))
file.close()

file = open("compressed.ini", "rb")
content = file.read()
print(zlib.decompress(content).decode("utf-8"))
file.close()

