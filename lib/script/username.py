import time
import json
import os.path

HIGHSCORE_FILE = "highscore.json"

USER_FILE = "user/name.json"
DEFAULT_JSON_NAME = 'anonymous'

class Username:
	def __init__(self, root):
		self.filename = os.path.join(root, USER_FILE)
	
	def _read_file(self):
		try:
			f = open(self.filename, 'r')
		except IOError:
			f = open(self.filename, 'w+')
		data = f.read()
		f.close()
		return data

	def _write_file(self, data):
		f = open(self.filename, 'w')
		f.write(data)
		f.close()
	
	def set(self, player):
		data_file = self._read_file()
		try:
			name = json.dumps(player)
		except ValueError:
			print("No se pudo emplear el nombre de usuario")
			name = json.dumps(DEFAULT_JSON_NAME)

		self._write_file(name)
	
	def get(self):
		data_file = self._read_file()
		try:
			return json.loads(data_file)
		except ValueError:
			return DEFAULT_JSON_NAME


if __name__ == "__main__":
	U = Username("../..")
	print(U.get())
	U.set("pepe")
	print(U.get())

