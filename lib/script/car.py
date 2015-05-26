# #############################
# Vehicle Physics Demo
# #############################
# This file is part of the book:
# "Game Development with Blender"
# by Dalai Felinto and Mike Pan
#
# Published by "CENGAGE Learning" in 2013
#
# You are free to use-it, modify it and redistribute
# as long as you keep the original credits when pertinent.
#
# File tested with Blender 2.66
#
# Copyright - February 2013
# This work is licensed under the Creative Commons
# Attribution-Share Alike 3.0 Unported License
# #############################

# Más info:
# http://www.blender.org/api/249PythonDoc/GE/GameTypes.KX_VehicleWrapper-class.html

## First, we import all the python module
from bge import constraints
from bge import logic
from bge import events
from bge import render

import mathutils
import math
import time
import os.path

import highscore
import username

scale = 1

## Set specific vehicle characteristics ##
wheel_radius = 0.197/2		# Radio de las ruedas
#tire1Radius = tireList["TireFD"].localScale[2]/2
suspensionLength = scale*0.08		#0.8
wheel_height = -0.0

mass = 200.0

stiffness 	= 200.0    #20.0	Dureza del amortiguador
#tire1Radius = tireList["TireFD"].localScale[2]/2
expansion	= 0.9*2*math.sqrt(stiffness)	#2.0	Suavizado de la amortiguación
compresion	= 0.4*2*math.sqrt(stiffness)	#4.0	Resistencia a la compresión

Stability 	= 0.00	#0.05
force 		= 300.0		#15.0
rear_force 	= 0.3			# Porción de fuerza aplicada atrás


CHASSIS_NAME = "car_chassis"
START_PROP = 'start'
HUD_SCENE = 'HUD'
TEXT_TIME = 'text-time'
TEXT_FINISH = 'text-finish'
DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(DIR, "../.."))
BLEND_BROWSE = os.path.abspath(os.path.join(ROOT, "lib/gui/browse/gui.blend"))

def car_friction(vehicle, front=None, back=None):
	if front != None:
		vehicle.setTyreFriction(front,0)
		vehicle.setTyreFriction(front,1)
	if back != None:
		vehicle.setTyreFriction(back,2)
		vehicle.setTyreFriction(back,3)

def car_influence(vehicle, front=None, back=None):
	if front != None:
		vehicle.setRollInfluence(front, 0)
		vehicle.setRollInfluence(front, 1)
	if back != None:
		vehicle.setRollInfluence(back, 2)
		vehicle.setRollInfluence(back, 3)

def car_brake(vehicle, front=None, back=None):
	if front != None:
		vehicle.applyBraking(front, 0)
		vehicle.applyBraking(front, 1)
	if back != None:
		vehicle.applyBraking(back, 2)
		vehicle.applyBraking(back, 3)

def car_power(vehicle, front=None, back=None):
	if front != None:
		vehicle.applyEngineForce(front, 0)
		vehicle.applyEngineForce(front, 1)
	if back != None:
		vehicle.applyEngineForce(back, 2)
		vehicle.applyEngineForce(back, 3)
	
def car_steer(vehicle, steering):
	vehicle.setSteeringValue(steering, 0)
	vehicle.setSteeringValue(steering, 1)
	

def car_logic_init():
	## setup aliases for Blender API access ##
	cont = logic.getCurrentController()
	logic.scene = logic.getCurrentScene()
	owner = cont.owner
	chassis = owner[CHASSIS_NAME]

	logic.car = logic.scene.objects[chassis]
	#logic.car.mass = mass

#	set_start_position(logic.car)
	car_init()
	reset_track(logic.car)
#	set_start_position(logic.car)

	print(username.Username(ROOT).get())



def set_start_position(car):
	#constraints.removeConstraint(car["cid"])
	for obj in logic.scene.objects:
		if 'finish' in obj:
			print("Encontre finish")
	for obj in logic.scene.objects:
		if START_PROP in obj:
			print("Encontre start")
			 	
			#car.suspendDynamics()
			#car.restoreDynamics()
			p = obj.worldPosition
			car.worldPosition = [p[0], p[1], p[2]+0.3]
			car.worldOrientation = obj.worldOrientation
			#car.setLinearVelocity([0,0,0])
			#car.setAngularVelocity([0,0,0])
			#car.linearVelocity = [0, 0, 0]
			car.worldAngularVelocity = mathutils.Vector([0, 0, 0])
			car.localAngularVelocity = mathutils.Vector([0, 0, 0])
			car.worldLinearVelocity = mathutils.Vector([0, 0, 0])
			car.localLinearVelocity = mathutils.Vector([0, 0, 0])
			#car.applyForce([0,0,0])
			#car.applyTorque([0,0,0])
			print(obj.worldPosition)
			print(obj.worldOrientation)
			print(obj.getReactionForce())
			return
	
	print("Falta la pieza de inicio")
	#end_game()

def reset_time(car):
	car["start_time"] = int(time.time()*1000)

def reset_track(car):
	set_start_position(car)
	reset_time(car)
	#car_init()

def end_game():
	logic.endGame()

def set_text_time(string):
	scenes = logic.getSceneList()
	for scene in scenes:
		if scene.name == HUD_SCENE:
			scene.objects[TEXT_TIME]['Text'] = string

def set_text_finish(string):
	scenes = logic.getSceneList()
	for scene in scenes:
		if scene.name == HUD_SCENE:
			scene.objects[TEXT_FINISH]['Text'] = string

	#logic.scene.objects["text-time"]["Text"] = "hola!"

## This is called from the car object
## is run once at the start of the game
def car_init():

	## setup aliases for Blender API access ##
	cont = logic.getCurrentController()
	logic.scene = logic.getCurrentScene()
	#logic.car  = cont.owner


	logic.car["start_time"] = 0
	#print("{} - {}".format(time.time(), logic.car["start_time"]))

	## setup general vehicle characteristics ##
	wheelAttachDirLocal = [0,0,-1]
	wheelAxleLocal = [-1,0,0]

	## setup vehicle physics ##
	vehicle = constraints.createConstraint(
		logic.car.getPhysicsId(), 0, constraints.VEHICLE_CONSTRAINT)
	

	if(vehicle.getConstraintId() == 0): end_game()
	
	logic.car["cid"] = vehicle.getConstraintId()
	vehicle = constraints.getVehicleConstraint(logic.car["cid"])


	## initialize temporary variables ##
	logic.car["dS"] = 0.0
	logic.car["force"]  = 0.0
	logic.car["steer"]  = 0.0
	logic.car["jump"]  = 0.0
	logic.car["steer_val"] = 0.0
	logic.car["steer_s"] = 0.0
	logic.car["km_h"] = 0.0
	logic.car["braking_time"] = 0.0
	logic.car["steeringR"] = 0.0
	logic.car["steeringL"] = 0.0
	logic.car["steering"] = False
	logic.car["theta"] = 0.0
	logic.car["time"] = 0
	
	logic.car["braking"] = False
	logic.car["ended"] = False

	car_pos = logic.car.worldPosition

	## attached wheel based on actuator name ##

	wheels = ['w0l', 'w0r', 'w1l', 'w1r']
	wheels_engine = [1, 1, 0, 0]

	for i in range(len(wheels)):
		wheel_name = wheels[i]
		wheel = logic.scene.objects[wheel_name]
		wheel_pos = wheel.worldPosition
		wheel_local = wheel_pos - car_pos - mathutils.Vector((0.0, 0.0, wheel_height))#wheel_height - suspensionLength))

		vehicle.addWheel(
			wheel,
			wheel_local,
			wheelAttachDirLocal,
			wheelAxleLocal,
			suspensionLength,
			wheel_radius,
			wheels_engine[i])
		
		## set vehicle roll tendency ##
		#vehicle.setRollInfluence(influence, i)
		## set vehicle suspension hardness ##
		vehicle.setSuspensionStiffness(stiffness, i)
		## set vehicle suspension dampness ##
		vehicle.setSuspensionDamping(expansion, i)
		## set vehicle suspension compression ratio ##
		vehicle.setSuspensionCompression(compresion, i)


def draw_vec(pos, vec, color=[1,1,1]):
    render.drawLine(pos, pos+vec, color)


def update_steer(vehicle):
	PI = math.pi

	# Configuración del giro de volante dependiendo de la velocidad
	v0 = 0
	theta0 = 20/360*2*PI
	v1 = 150
	theta1 = 15/360*2*PI
	
	# Tiempo que tarda en alcanzar el ángulo máximo de giro
	ts = 0.2
	Ki = 0.01


	speed = math.fabs(logic.car["speed"])
	K1 = (v1*theta1 - v0*theta0) / (theta0 - theta1)
	K2 = (v0 + K1) * theta0
	theta_max = K2 / (speed + K1)

	#print("Ángulo máximo de giro {}".format(theta_max))

	Kfps = 60.0
	steering = logic.car["steering"]
	stR = logic.car["steeringR"]
	stL = logic.car["steeringL"]
	theta = logic.car["theta"]
	tR = stR / Kfps
	tL = stL / Kfps

	stmax = ts*Kfps
	if stR > stmax: logic.car["steeringR"] = stmax
	if stL > stmax: logic.car["steeringL"] = stmax

	Ktheta = theta_max / ts**2

	if steering:
		if stR > 0.0:
			inc_theta = 2 * Ktheta * tR / Kfps + Ki
			theta = max(theta - inc_theta, -theta_max)
			#logic.car["steeringL"] = max(0, stL-1)
			logic.car["steeringL"] = 0
		elif stL > 0.0:
			inc_theta = 2 * Ktheta * tL / Kfps
			theta = min(theta + inc_theta, theta_max)
			#logic.car["steeringR"] = max(0, stR-1)
			logic.car["steeringR"] = 0
	else:
		#logic.car["steeringR"] = max(0, stR-1)
		#logic.car["steeringL"] = max(0, stL-1)
		logic.car["steeringR"] = 0
		logic.car["steeringL"] = 0
		theta *= 0.6

	logic.car["theta"] = theta
			


	car_steer(vehicle, theta)


def is_braking():
	cont = logic.getCurrentController()
	on = cont.actuators["turn_on"]
	off = cont.actuators["turn_off"]

	try:
		if "braking" in logic.car and logic.car["braking"]:
			cont.activate(on)
			cont.deactivate(off)

		else:
			cont.activate(off)
			cont.deactivate(on)
	except:
		cont.activate(off)
		cont.deactivate(on)
		

## called from main car object
## is run once at the start of the game
def car_update():

	#print("car update")
	vehicle = constraints.getVehicleConstraint(logic.car["cid"])

	## calculate speed by using the back wheel rotation speed ##
	S = vehicle.getWheelRotation(2)+vehicle.getWheelRotation(3)
	logic.car["speed"] = (S - logic.car["dS"])*10.0

	wheel_v = logic.scene.objects['w1l'].getLinearVelocity(True)
	pos = logic.car.worldPosition
	lpos = logic.car.localPosition
	vel = logic.car.getLinearVelocity(False)
	#draw_vec(pos+mathutils.Vector((0,0,1)), vel)
	#draw_vec(pos+mathutils.Vector((0,0,1)), mathutils.Vector((1,0,0)))
	#draw_vec(pos+mathutils.Vector((0,0,1)), mathutils.Vector(rf), [1,0,0])
#	draw_vec(pos, mathutils.Vector((1,0,)))
	#draw_vec(pos, wheel_v)
	#print(wheel_v)
	#print(logic.car.worldOrientation.to_euler())
	#print("------------------------")
	

	if logic.car["start_time"] == 0:
		logic.car["start_time"] = int(time.time()*1000)

	if not logic.car["ended"]:
		now = time.time()
		tiempo = int(now*1000) - logic.car["start_time"]
		cent = int(tiempo/10 % 100)
		segundos = int(tiempo/1000)%60
		minutos = int(tiempo/(1000*60))
		set_text_time("{m:02d}:{s:02d}:{c:02d}".format(
			m=minutos, s=segundos, c=cent))
		set_text_finish("")
		
		logic.car["time"] = tiempo
	else:
		set_text_finish("META")
		now = time.time()
		esperado = int(now*1000 - logic.car["start_time"] - logic.car["time"])
		if esperado > 3 * 1000:
			game_back()
	

	#f = mathutils.Vector(logic.car.getReactionForce()) * 3
	#print(f)
	#draw_vec(mathutils.Vector((0,0,0)), f)
	velm = math.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2)
	#print(linSum)



	## brake back wheels
	if logic.car["braking"]:
		logic.car["braking_time"] += 1
		braking_time = logic.car["braking_time"]

		car_friction(vehicle, 1.45, 0.28)
		car_influence(vehicle, 1, 1)
		car_power(vehicle, logic.car["force"], 0)
		car_brake(vehicle, 0, 1.45)
	else:
		logic.car["braking_time"] = 0
		car_friction(vehicle, 1.9, 2)
		car_influence(vehicle, 0.9, 0.8)
		car_power(vehicle, logic.car["force"], logic.car["force"] * rear_force)
		car_brake(vehicle, 0, 0)

	## calculate steering with varying sensitivity ##

	speed = math.fabs(logic.car["speed"])
	log_speed = math.log(speed * 0.06 + 1)
	#s = 2 - log_speed
	s = 2 - math.pow(speed * 0.06, 1/3)
	if s < 0.03: s = 0.03

	steer_val = logic.car["steer"] * 1 * s

	log_steer = max(1-math.log(speed+30)/5, 0.03)
	#print(steer_val)
	logic.car["steer_val"] = log_steer
	logic.car["steer_s"] = log_steer
	logic.car["km_h"] = velm

#	if math.fabs(logic.car["speed"])<15.0: s = 2.0
#	elif math.fabs(logic.car["speed"])<28.0: s=1.5
#	elif math.fabs(logic.car["speed"])<40.0: s=1.0
#	else: s=0.5

	## steer front wheels
	#vehicle.setSteeringValue(logic.car["steer"] * s,0)
	#car_steer(vehicle, steer_val)

	## align car to Z axis to prevent flipping ##
	logic.car.alignAxisToVect([0.0,0.0,1.0], 2, Stability)
	
	## store old values ##
	logic.car["dS"] = S

	logic.car["jump"] += 0.1
	update_steer(vehicle)

## called from main car object
def key_update():
	#print('key update')
	cont = logic.getCurrentController()
	keys = cont.sensors["key"].events
	#logic.car["braking"] = False
	#print(keys)
	logic.car["steering"] = False
	logic.car["force"]  = 0
	for key in keys:
		## up arrow
		if key[0] == events.UPARROWKEY:
			if key[1] in (logic.KX_INPUT_JUST_ACTIVATED, logic.KX_INPUT_ACTIVE):
				logic.car["force"]  = -force
			elif key[1] == logic.KX_INPUT_JUST_RELEASED:
				logic.car["force"]  = 0
		## down arrow
		elif key[0] == events.DOWNARROWKEY:
			if key[1] in (logic.KX_INPUT_JUST_ACTIVATED, logic.KX_INPUT_ACTIVE):
				logic.car["force"]  = force
			elif key[1] == logic.KX_INPUT_JUST_RELEASED:
				logic.car["force"]  = 0
		## right arrow
		elif key[0] == events.RIGHTARROWKEY:
			if key[1] in (logic.KX_INPUT_JUST_ACTIVATED, logic.KX_INPUT_ACTIVE):
				logic.car["steeringR"] += 1
				logic.car["steering"] = True
		## left arrow
		elif key[0] == events.LEFTARROWKEY:
			if key[1] in (logic.KX_INPUT_JUST_ACTIVATED, logic.KX_INPUT_ACTIVE):
				logic.car["steeringL"] += 1
				logic.car["steering"] = True
		## Reverse
		elif key[0] == events.BACKSPACEKEY:
			if key[1] == logic.KX_INPUT_JUST_ACTIVATED:
				reset_track(logic.car)
				# re-orient car
				#if logic.car["jump"] > 0.2:
				#	pos = logic.car.worldPosition
				#	logic.car.position = (pos[0], pos[1], pos[2]+10.0)
				#	logic.car.alignAxisToVect([0.0,0.0,1.0], 2, 1.0)
				#	#logic.car.setLinearVelocity([0.0,0.0,0.0],1)
				#	logic.car.setAngularVelocity([0.0,0.0,0.0],1)
				#	logic.car["jump"] = 0
		#elif key[0] == events.BKEY:
		elif key[0] == events.ESCKEY:
			game_back()
		## Spacebar
		#elif key[0] == events.SPACEKEY:
		#	# hackish Brake
		#	if logic.car["speed"] > 2.0:
		#		logic.car["force"]  = force
		#	if logic.car["speed"] < -2.0:
		#		logic.car["force"]  = -force
		elif key[0] in (events.LEFTCTRLKEY, events.RIGHTCTRLKEY):
			#logic.car["braking"] = True
			if key[1] == logic.KX_INPUT_JUST_ACTIVATED:
				logic.car["braking"] = True
			elif key[1] == logic.KX_INPUT_JUST_RELEASED:
				logic.car["braking"] = False
	
	
#def on_collide():
	#print("collide")

## called from shadow lamp
def shadow():
	cont = logic.getCurrentController()
	ownpos = [-5.0,0.0,8.0]
	pos = logic.car.worldPosition
	cont.owner.worldPosition = [pos[0]+ownpos[0], pos[1]+ownpos[1], pos[2]+ownpos[2]]

def get_username():
	p = os.path.join(logic.expandPath("//"), "../../../user/name")
	f = open(p, "r")
	name = f.readline().rstrip()
	f.close()
	return name

# Cuando colisiona con la meta
def finish_line():
	if not logic.car["ended"]:
		print("META!!!")
		name = username.Username(ROOT).get()
		map_time = logic.car["time"]
		H = highscore.Highscore(logic.expandPath("//"))
		H.add_score(name, map_time)
		print("{} completó en {}".format(name, map_time))
		logic.car["ended"] = True

def game_back():
	logic.startGame(BLEND_BROWSE)

