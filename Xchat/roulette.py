#!/usr/bin/python2
__module_name__	= "roulette.py"
__module_version__	= "1.00"
__module_description__	= "Russian Roulette plugin"
__module_author__	= "Ferus"

import xchat
import random

channels = {'#roulette':'kill'}
gunlist = ['Smith & Wesson','Armsel Striker','Colt Anaconda', 'Colt Python', 'Magnum', 'Nagant M1895', 'Reichsrevolver', 'Smith & Wesson Centennial', 'Smith & Wesson Ladysmith', 
		'Walker Colt']
reasons = ['Head blown off by a {0}', 'Shot themself to death with a {0}', 'Lodged lead in their greymatter with a {0}', 'Blew their mind (literally) with a {0}', 
		'Sprayed brain goop all over the walls with a {0}', 'Took the easy way out with a {0}']

class Gun():
	def __init__(self, name, chambers, bullets=0, version=1):
		'''Create name and chambers, default to version 1.'''
		self.name = name
		self.chambers = chambers
		self.version = version
		self.bullets = bullets

		if self.bullets > 0: 
			'''If we are starting with bullets: Add them now and spin.'''
			self.load(self.bullets)				

		if self.version == 1:
			if self.bullets == 0:
				'''We are starting empty, this isnt good, add a bullet.'''
				self.load(1)

	def load(self, bullet_amount=0):
		'''Load our gun, If version 1, return a spun chamber only.'''
		if self.version == 2:
			bullet_amount = 1

		for x in range(0, len(self.chambers)):
			if all(self.chambers):
				break
			if bullet_amount == 0:
				break
			if self.chambers[x]:
				continue
			else:
				self.chambers[x] = not self.chambers[x]
				bullet_amount -= 1
				self.bullets += 1
				if self.bullets > 1:
					say("Adding a bullet; There are \x02{0}\x02 bullets in the \x02{1}\x02, with \x02{2}\x02 chambers.".format(self.bullets, self.name, len(self.chambers)))
				else:
					say("Adding a bullet; There is \x02{0}\x02 bullet in the \x02{1}\x02, with \x02{2}\x02 chambers.".format(self.bullets, self.name, len(self.chambers)))
		self.spin()
		
	def shoot(self):
		'''Shoot the gun, Automatically reloads/spins.'''
		if self.version == 1:
			if self.chambers[0]:
				'''Remove the bullet from the chamber, and decrease our bullet count.'''
				self.chambers[0] = not self.chambers[0]
				self.bullets -= 1
				self.load()
				return True
			else:
				say("\x02*click*\x02...")
				self.load()
		else:
			self.load()
			if self.chambers[0]:
				'''Remove the bullet from the chamber, and decrease our bullet count.'''
				self.chambers[0] = not self.chambers[0]
				self.bullets -= 1
				return True
			else:
				say("\x02*click*\x02...")

	def spin(self):
		'''Randomize our bullets list'''
		random.shuffle(self.chambers)
		say("Spinning Chamber...")		
	
	def action(self, channel):
		if channels[channel] == 'kill':
			return True
		else:
			return False

	def reset(self):
		'''Changes the gun instance's variables to create a 'new' gun'''
		self.name = random_gun()
		self.chambers = create_chambers()
		self.bullets = 0


def create_chambers():
	'''Returns a list of False to show number of empty chambers'''
	rand = random.randint(5,8)
	chambers = []
	for x in range(0, rand):
		chambers.append(False)
	return chambers

#def random_bullets():
#	'''Return a random number of bullets to start with'''
#	pass

def random_gun():
	'''Picks a random gun name from the gunlist'''
	r = random.choice(gunlist)
	return r

def random_reason(name):
	r = (random.choice(reasons)).format(name)
	return r



def shoot(person):
	if g.shoot():	
		reason = random_reason(g.name)
		channel = (xchat.get_context()).get_info("channel")
		person = xchat.strip(person)
		if g.action(channel):
			xchat.command("raw kill {0} {1} ({2})".format(person, reason, channel))
		else:
			xchat.command("kickban {0} {1}".format(person, reason))
			xchat.command("invite {0} {1}".format(person, channel))
		g.reset()
		g.load(1)

def shoot2(person):
	if g2.shoot():	
		reason = random_reason("\x02{0}\x02".format(g2.name))
		channel = (xchat.get_context()).get_info("channel")
		person = xchat.strip(person)
		if g2.action(channel):
			xchat.command("raw kill {0} {1} (\x02{2}\x02/\x02{3} Bullets\x02 - {4})".format(person, reason, g2.bullets+1, len(g2.chambers), channel))
		else:
			xchat.command("kickban {0} {1}".format(person, reason))
			xchat.command("invite {0} {1}".format(person, channel))
		g2.reset()
#		g2.load()

		
def debug():
	print "{0}\n{1}\n{2}".format(g2.name, g2.chambers, g2.bullets)

#def duel_ver1(person):
#	pass
#def duel_ver2(person):
#	pass

def isChan():
	if (xchat.get_context()).get_info("channel") in channels.keys():
		return True

def say(m):
	xchat.command("SAY {0}".format(m))

def parse(word, word_eol, userdata):
	if isChan():
#		if xchat.strip(word[0]) != 'Ferus':
#			pass
#		else:
		msg = word[1].split()
		if '!shoot' == msg[0]:
			shoot(word[0])
		if '!shoot2' == msg[0]:
			shoot2(word[0])

say("Loaded Russian Roulette Plugin, Creating Gun.")			
g = Gun(random_gun(), create_chambers())
g2 = Gun(random_gun(), create_chambers(), 0, 2)
xchat.hook_print('Channel Message', parse)

print ("Loaded " + __module_author__ +"'s " + __module_description__)

# `!duel person` starts a new gun instance between two people.
# if ^ was duel: declare winner
#[18:09] <+stal> portal gun:
#[18:09] <+stal> it saparts you from the channel and sajoins you to another
#<&hambanner> Or you could make the gunpowder in the cannon fail to detonate.
