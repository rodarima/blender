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

## Set specific vehicle characteristics ##
wheel_radius = 0.65/2		# Radio de las ruedas
wheel_wide = 1.0		# Separación entre ruedas (ancho)
wheel_height = -0.2
wheelFrontOffset = 1.25
wheelBackOffset = -1.25
#AttachHeightLocal = 0.6		#0.2
suspensionLength = 0.3		#0.8

mass = 50.0

influence = 0.05	#0.02
stiffness = 50.0    #20.0	Dureza del amortiguador
damping = 5	#2.0	Suavizado de la amortiguación
compression = 10.0	#4.0	Resistencia a la compresión
friction = 100.0		#10.0
Stability = 0.02	#0.05
force = 400.0		#15.0
ease_steer = 0.9	#0.6
ease_force = 0.5	#0.9
steer_inc = 0.03	#0.05
rear_force = 0.2			# Porción de fuerza aplicada atrás
brake_force = force*0.3
brake_friction = friction * 0.5


CHASSIS_NAME = "car_chassis"



def car_logic_init():
	## setup aliases for Blender API access ##
	cont = logic.getCurrentController()
	logic.scene = logic.getCurrentScene()
	owner = cont.owner
	chassis = owner[CHASSIS_NAME]

	logic.car = logic.scene.objects[chassis]
	#logic.car.mass = mass

	car_init()







## This is called from the car object
## is run once at the start of the game
def car_init():

	## setup aliases for Blender API access ##
	cont = logic.getCurrentController()
	logic.scene = logic.getCurrentScene()
	#logic.car  = cont.owner

	## setup general vehicle characteristics ##
	wheelAttachDirLocal = [0,0,-1]
	wheelAxleLocal = [-1,0,0]

	## setup vehicle physics ##
	vehicle = constraints.createConstraint(
		logic.car.getPhysicsId(), 0, constraints.VEHICLE_CONSTRAINT)
	
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
	
	logic.car["braking"] = False

	car_pos = logic.car.worldPosition

	## attached wheel based on actuator name ##

	wheels = ['w0l', 'w0r', 'w1l', 'w1r']
	wheels_engine = [1, 1, 0, 0]

	for i in range(len(wheels)):
		wheel_name = wheels[i]
		wheel = logic.scene.objects[wheel_name]
		wheel_pos = wheel.worldPosition
		wheel_local = wheel_pos - car_pos - mathutils.Vector((0.0, 0.0, wheel_height))

		vehicle.addWheel(
			wheel,
			wheel_local,
			wheelAttachDirLocal,
			wheelAxleLocal,
			suspensionLength,
			wheel_radius,
			wheels_engine[i])
		
		## set vehicle roll tendency ##
		vehicle.setRollInfluence(influence, i)
		## set vehicle suspension hardness ##
		vehicle.setSuspensionStiffness(stiffness, i)
		## set vehicle suspension dampness ##
		vehicle.setSuspensionDamping(damping, i)
		## set vehicle suspension compression ratio ##
		vehicle.setSuspensionCompression(compression, i)


def draw_vec(pos, vec):
    render.drawLine(pos, pos+vec, [1,1,1])

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
	vel = logic.car.getLinearVelocity(False)
	draw_vec(pos, vel)
	#draw_vec(pos, wheel_v)
	#print(wheel_v)

	#f = mathutils.Vector(logic.car.getReactionForce()) * 3
	#print(f)
	#draw_vec(mathutils.Vector((0,0,0)), f)
	velm = math.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2)
	#print(linSum)

	## apply engine force ##
	vehicle.applyEngineForce(logic.car["force"],0)
	vehicle.applyEngineForce(logic.car["force"],1)

	## calculate steering with varying sensitivity ##

	speed = math.fabs(logic.car["speed"])
	s = 2 - math.pow(speed * 0.06, 1/3)
	if s < 0.07: s = 0.07

	steer_val = logic.car["steer"] * 1# * s
	print(steer_val)
	logic.car["steer_val"] = steer_val
	logic.car["steer_s"] = s
	logic.car["km_h"] = velm

#	if math.fabs(logic.car["speed"])<15.0: s = 2.0
#	elif math.fabs(logic.car["speed"])<28.0: s=1.5
#	elif math.fabs(logic.car["speed"])<40.0: s=1.0
#	else: s=0.5

	## steer front wheels
	#vehicle.setSteeringValue(logic.car["steer"] * s,0)
	vehicle.setSteeringValue(steer_val, 0)
	vehicle.setSteeringValue(steer_val, 1)

	## brake back wheels
	if logic.car["braking"]:
		#vehicle.applyBraking(brake_force, 2)
		#vehicle.applyBraking(brake_force, 3)
		vehicle.setTyreFriction(brake_friction,2)
		vehicle.setTyreFriction(brake_friction,3)
		vehicle.applyEngineForce(-brake_force,2)
		vehicle.applyEngineForce(-brake_force,3)
		logic.car["braking"] = False
		#print("braking {}".format(brake_force))
	else:
		vehicle.setTyreFriction(friction,2)
		vehicle.setTyreFriction(friction,3)
		vehicle.applyEngineForce(logic.car["force"] * rear_force,2)
		vehicle.applyEngineForce(logic.car["force"] * rear_force,3)


	## slowly ease off gas and center steering ##
	logic.car["steer"] *= ease_steer
	logic.car["force"] *= ease_force

	## align car to Z axis to prevent flipping ##
	logic.car.alignAxisToVect([0.0,0.0,1.0], 2, Stability)
	
	## store old values ##
	logic.car["dS"] = S

	logic.car["jump"] += 0.1



## called from main car object
def key_update():
	#print('key update')
	cont = logic.getCurrentController()
	keys = cont.sensors["key"].events
	#print(keys)
	for key in keys:
		## up arrow
		if key[0] == events.UPARROWKEY:
			logic.car["force"]  = -force
		## down arrow
		elif key[0] == events.DOWNARROWKEY:
			logic.car["force"]  = force
		## right arrow
		elif key[0] == events.RIGHTARROWKEY:
			logic.car["steer"] -= steer_inc
		## left arrow
		elif key[0] == events.LEFTARROWKEY:
			logic.car["steer"] += steer_inc
		## Reverse
		elif key[0] == events.RKEY:
			if key[1] == 1:
				# re-orient car
				if logic.car["jump"] > 0.2:
					pos = logic.car.worldPosition
					logic.car.position = (pos[0], pos[1], pos[2]+10.0)
					logic.car.alignAxisToVect([0.0,0.0,1.0], 2, 1.0)
					#logic.car.setLinearVelocity([0.0,0.0,0.0],1)
					logic.car.setAngularVelocity([0.0,0.0,0.0],1)
					logic.car["jump"] = 0
		## Spacebar
		elif key[0] == events.SPACEKEY:
			# hackish Brake
			if logic.car["speed"] > 2.0:
				logic.car["force"]  = force
			if logic.car["speed"] < -2.0:
				logic.car["force"]  = -force
		elif key[0] in (events.LEFTCTRLKEY, events.RIGHTCTRLKEY):
			logic.car["braking"] = True
			#if key[1] == logic.KX_INPUT_JUST_ACTIVATED
			#	logic.car["braking"] = True
			#else:
			#	logic.car["braking"] = False
	
#def on_collide():
	#print("collide")

## called from shadow lamp
def shadow():
	cont = logic.getCurrentController()
	ownpos = [-5.0,0.0,8.0]
	pos = logic.car.worldPosition
	cont.owner.worldPosition = [pos[0]+ownpos[0], pos[1]+ownpos[1], pos[2]+ownpos[2]]



