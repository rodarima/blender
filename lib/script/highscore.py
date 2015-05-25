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
	
	def get_best(self, n):
		data_file = self._read_file()
		try:
			highs = json.loads(data_file)
		except ValueError:
			highs = []

		highs_sort = sorted(highs, key=lambda k: k['millis']) 
		best = highs_sort[0:n]
		
		return best

	def format_millis(t):
		cent = int(t/10 % 100)
		segundos = int(t/1000)%60
		minutos = int(t/(1000*60))
		s = "{m:02d}:{s:02d}:{c:02d}".format(
			m=minutos, s=segundos, c=cent)
		return s

		

if __name__ == "__main__":
	H = Highscore("")
	H.add_score('pepe', 1000)
	H.add_score('juan', 2000)
	H.add_score('pedro', 3000)
	print(H.get_best(3))
