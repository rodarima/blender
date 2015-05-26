ROOT = "../../.."
PATH_SCRIPT = "lib/script"
PATH_MAP = "lib/map"
MAP_NAME = "map.blend"

import sys
import os.path

# So we can find the bgui module
sys.path.append(os.path.join(ROOT, PATH_SCRIPT))

import bgui
import bgui.bge_utils
import bge

import username
import highscore

FILES_PAGE = 5
COLUMNS = 2
BEST_COUNT = 3

class BrowseLayout(bgui.bge_utils.Layout):
	"""A layout showcasing various Bgui features"""

	def __init__(self, sys, data):
		super().__init__(sys, data)

		self.win = bgui.Frame(self, size=[1.0, 1.0], sub_theme='black',
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			
		self.page = 0

		self.btn_maps = []
		self.lbl_player = []
		self.lbl_time = []
		for i in range(0, FILES_PAGE):
			pos = [0.1, 1 - 0.0 - (i+1)*0.8/FILES_PAGE]
			tpos = [pos[0]+ 0.3, pos[1] - 0.03]
			ppos = [pos[0]+ 0.4, tpos[1]]

			size = [0.8, 0.3/FILES_PAGE]
			btn_file = bgui.FrameButton(self.win, text='Fichero'+str(i), size=size,
				pos=pos, options = bgui.BGUI_DEFAULT)
			btn_file.on_click = self._file_selected
		
			self.btn_maps.append(btn_file)

			lbl_time = bgui.Label(self.win, text="TIME", pos=tpos,
				options = bgui.BGUI_DEFAULT)
			self.lbl_time.append(lbl_time)

			lbl_player = bgui.Label(self.win, text="PLAYER", pos=ppos,
				options = bgui.BGUI_DEFAULT)
			self.lbl_player.append(lbl_player)

		navx = .85
		navy = .02
		self.btn_next = bgui.FrameButton(self.win, text='Siguiente', size=[.1, .05], pos=[navx, navy],
			options = bgui.BGUI_DEFAULT)
		self.btn_next.on_click = self._next_page
		self.btn_next.frozen=1
		self.btn_next.visible=0

		self.btn_prev = bgui.FrameButton(self.win, text='Anterior', size=[.1, .05], pos=[1-navx-.1, navy],
			options = bgui.BGUI_DEFAULT)
		self.btn_prev.on_click = self._prev_page

		self.btn_back = bgui.FrameButton(self.win, text='Volver', size=[.1, .05], pos=[0.05, 1-0.02-.05],
			options = bgui.BGUI_DEFAULT)
		self.btn_back.on_click = self._back
	
	
		self._draw_page()
	
	def _get_files(self, page):
		maps = os.listdir(os.path.join(ROOT, PATH_MAP))
		maps.sort()

		count = len(maps)
		start = FILES_PAGE*page
		end = FILES_PAGE*(page+1)
		maps_page = maps[start:end]
		more = count > end
		less = start > 0
		return (maps_page, more, less)
	
	def _file_selected(self, w):
		map_name = os.path.join(ROOT, PATH_MAP, w.text, MAP_NAME)
		bge.logic.startGame("//"+map_name)
	
	def _back(self, w):
		bge.logic.startGame("//../username/gui.blend")
	
	def _next_page(self, w):
		self.page+=1
		self._draw_page()

	def _prev_page(self, w):
		self.page-=1
		self._draw_page()

	def _btn_off(self, w):
		w.frozen=1
		w.visible=0
		
	def _btn_on(self, w):
		w.frozen=0
		w.visible=1

	def _draw_page(self):
		(maps, more, less) = self._get_files(self.page)

		if more: self._btn_on(self.btn_next)
		else: self._btn_off(self.btn_next)
		
		if less: self._btn_on(self.btn_prev)
		else: self._btn_off(self.btn_prev)

		for i in range(len(self.btn_maps)):
			self._btn_off(self.btn_maps[i])
			self.lbl_player[i].text = ""
			self.lbl_time[i].text = ""

		for i in range(len(maps)):
			btn = self.btn_maps[i]
			btn.text = maps[i]
			self._btn_on(btn)
			self._draw_best(self.lbl_player[i], self.lbl_time[i], maps[i])
	
	def _draw_best(self, lbl_player, lbl_time, map_path):
		map_dir = os.path.join(ROOT, PATH_MAP, map_path)
		H = highscore.Highscore(map_dir)

		best_list = H.get_best(BEST_COUNT)
	
		time = ""
		player = ""
		for mark in best_list:
			time += highscore.Highscore.format_millis(mark['millis']) + '\n'
			player += mark['player'] + '\n'

		lbl_player.text = player
		lbl_time.text = time
		


def main(cont):
	own = cont.owner
	mouse = bge.logic.mouse

	if 'sys' not in own:
		# Create our system and show the mouse
		own['sys'] = bgui.bge_utils.System('../themes/default')
		own['sys'].load_layout(BrowseLayout, None)
		mouse.visible = True

	else:
		own['sys'].run()
