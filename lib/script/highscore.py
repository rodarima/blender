import time
import json
import os.path

HIGHSCORE_FILE = "highscore.json"

class Highscore:
	def __init__(self, dir_path):
		self.filename = os.path.join(dir_path, HIGHSCORE_FILE)
	
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
	
	def add_score(self, player, millis):
		t = time.time()
		entry = {'player':player, 'timestamp':t, 'millis': millis}

		data_file = self._read_file()
		try:
			highs = json.loads(data_file)
		except ValueError:
			highs = []

		highs.append(entry)
		
		self._write_file(json.dumps(highs))

if __name__ == "__main__":
	H = Highscore("")
	H.add_score('pepe', 1000)
