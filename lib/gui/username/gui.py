ROOT = "../../.."
SCRIPT_PATH = "lib/script"

import sys
import os.path

# So we can find the bgui module
sys.path.append(os.path.join(ROOT, SCRIPT_PATH))

import bgui
import bgui.bge_utils
import bge

import username



class SimpleLayout(bgui.bge_utils.Layout):
	"""A layout showcasing various Bgui features"""

	def __init__(self, sys, data):
		super().__init__(sys, data)

		self.u = username.Username(ROOT)
		user = self.u.get()
		
		self.win = bgui.Frame(self, size=[1.0, 1.0], sub_theme='black',
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			
		self.lbl = bgui.Label(self.win, text="Jugador", pos=[0.5-0.2, 0.57-0.02],
			options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

		self.input = bgui.TextInput(self.win, text=user, size=[.4, .04], pos=[0.5-0.2, 0.5-0.02],
			input_options = bgui.BGUI_INPUT_SELECT_ALL, options = bgui.BGUI_DEFAULT)

		self.lbl = bgui.Label(self.win, text="Pulsa Enter para continuar", pos=[0.5-0.2, 0.45-0.02],
			options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX, sub_theme='small')

		self.input.activate()
		self.input.on_enter_key = self.on_input_enter

	def on_input_enter(self, widget):
		print("Jugador: "+widget.text)
		self.u.set(widget.text)
		bge.logic.startGame("//../browse/gui.blend")

def main(cont):
	own = cont.owner
	mouse = bge.logic.mouse

	if 'sys' not in own:
		# Create our system and show the mouse
		own['sys'] = bgui.bge_utils.System('../themes/default')
		own['sys'].load_layout(SimpleLayout, None)
		mouse.visible = True

	else:
		own['sys'].run()
