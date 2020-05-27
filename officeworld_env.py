"""
Program Name: officeworld_env.py
Programmer: Adi Ojha
Description:
This file creates the office world RL environment to be a subclass of gym.Env. This way researchers can use OpenAI baselines' algorithms on this RL environment via the gym library
"""
import gym
from enum import Enum
import random
from reward_machines.reward_machine import RewardMachine
"""
This class was given to me in the previous implementation of office world.
I am using it because I do not see a reason to delete it as of 5/24/2020 3:45 pm
"""
class Actions(Enum):
	up = 0
	right = 1
	down = 2
	left = 3
	#I only supported these four actions because they are the only one's used in office world (5/24/2020 3:45)

"""
This class details Office world. In order to be a gym.env it must have four classes as follows:
1. init method
	This method sets the initial state of the RL problem
	parameters = None
	output = None
2. Step method
	This method takes an action and delivers 4 things: 
		a) Next State of environment
		b) Reward for current state
		c) Boolean of whether episode is done
		d) Additional information (As of 5/24/2020 I do not know what this should be)
	parameters = action of type Actions (see above)
	output = [next_state,reward,boolean_episode_done,additional_information]
		
3. Reset method
	This method makes the object revert to the intial state.
	parameters: none
	output: None
4. Render method
	this method allows one to visualize the model
	parameters: none
	output: No return type but will print out the board
	
"""


class OfficeWorld(gym.Env):
	def __init__(self):#This method should set up the initial state of our problem
		self._load_map() #setup the map to initial state
		self.env_game_over = False #The game is not over; so I set this variable to False
		
	def step(self, action):
		#first check if action is valid: one sec give me a moment 
		str_to_action = {"w":Actions.up.value,"d":Actions.right.value,"s":Actions.down.value,"a":Actions.left.value}
		t = "/home/adiojha629/drone_research_summer2020/officeworld_gym/gym-officeworld/gym_officeworld/envs/reward_machines/t1.txt" #directory for text file that sets up reward machine
		self.rm = RewardMachine(t)#create the reward machine
		u1 = rm.get_state()
		s1 = self.get_state()
		if action in str_to_action:
			self.execute_action(str_to_action[action])
			events = self.get_true_propositions()#get conditions of the game
		        u2 = rm.get_next_state(u1, events)#get the next state
		        s2 = self.get_state()
		        r = rm.get_reward(u1,u2,s1,action,s2)#use the reward machine to generate the rewards
			reward, next_state = rm.get_rewards_and_next_states(s1, a, s2, events)
			
			boolean_episode_done = self.env_game_over or rm.is_terminal_state(u2) #if the game is over or we're at the teriminal state then the episode is over	
		additional_information = []
		
		return [next_state,reward,boolean_episode_done,additional_information]

	def reset(self):
		self.load_map()#put the map objects back where they were, and put the agent back at (2,1)
	
	def render(self):#This code is the show() method in the old office world implementation
		for y in range(8,-1,-1): #iterate from 8 to 0 (8,7,6 ... 2,1,0)
		    if y % 3 == 2: #if y is 2 5 8
		        for x in range(12):#iterate through 0 to 11
		            if x % 3 == 0: #print "_" if divisible by 3: 0,3,6,9
		                print("_",end="")
		                if 0 < x < 11:#if x = 3 6 9 print another "_"
		                    print("_",end="")
		            if (x,y,Actions.up) in self.forbidden_transitions:#if its forbidden to go up, then put another "_"
		                print("_",end="")
		            else:#if not forbidden then put a space
		                print(" ",end="")
		        print()#newline                
		    for x in range(12):#interate from 0 to 11
		        if (x,y,Actions.left) in self.forbidden_transitions:#if forbidden to go left, put a "|"
		            print("|",end="")
		        elif x % 3 == 0:#if 0,3,6,9 put a " "
		            print(" ",end="")
		        if (x,y) == self.agent:#if the current x,y is where the agent is then print A there
		            print("A",end="")
		        elif (x,y) in self.objects:#other wise if the x,y is in self.objects print the object here
		            print(self.objects[(x,y)],end="")
		        else:#if not the agent or an object print a " "
		            print(" ",end="")
		        if (x,y,Actions.right) in self.forbidden_transitions: #if going right is forbidden then you print a "|"
		            print("|",end="")
		        elif x % 3 == 2:# if x is 2 5 8 put a space
		            print(" ",end="")
		    print()  #newline    
		    if y % 3 == 0:  #if y is 0,3,6,9   
		        for x in range(12):#iterate from 0 to 11
		            if x % 3 == 0:#if x = 0,3,6,9 print "_"
		                print("_",end="")
		                if 0 < x < 11: #if its 3 6 9 you're printing two "_"
		                    print("_",end="")
		            if (x,y,Actions.down) in self.forbidden_transitions:
		                print("_",end="") #put a "_" if its forbidden to go down
		            else:
		                print(" ",end="")#if not forbidden print a space
		        print()           #print a new line
		        
		   
	def get_state(self):
		return None
	def _load_map(self):
		# Creating the map
		self.objects = {}
		self.objects[(1,1)] = "a"#put some objects in specific locations. What objects are a b and c refering to
		self.objects[(10,1)] = "b"
		self.objects[(1, 3)] = "c"
		self.objects[(7,4)] = "e"  # MAIL
		self.objects[(3,5)] = "f"  # COFFEE
		self.objects[(4,4)] = "g"  # OFFICE

		# Adding walls
		self.forbidden_transitions = set()#create empty set
		# general grid
		for x in range(12):
		    for y in [0,3,6]:
		        self.forbidden_transitions.add((x,y,Actions.down)) #Can't go down when y = 0,3,6
		        self.forbidden_transitions.add((x,y+2,Actions.up)) #Can't go up when y = 2,5,8
		for y in range(9):
		    for x in [0,3,6,9]:
		        self.forbidden_transitions.add((x,y,Actions.left)) #can't go left when x is 0,3,6,9
		        self.forbidden_transitions.add((x+2,y,Actions.right)) #Can't go right when x is 2,5,8,11
		# adding 'doors' Add doors to specific areas
		for y in [1,7]:
		    for x in [2,5,8]:
		        self.forbidden_transitions.remove((x,y,Actions.right))
		        self.forbidden_transitions.remove((x+1,y,Actions.left))
		for x in [1,4,7,10]:
		    self.forbidden_transitions.remove((x,5,Actions.up))
		    self.forbidden_transitions.remove((x,6,Actions.down))
		for x in [1,10]:
		    self.forbidden_transitions.remove((x,2,Actions.up))
		    self.forbidden_transitions.remove((x,3,Actions.down))
		# Adding the agent
		self.agent = (2,1) #Agent starts at 2,1
		self.actions = [Actions.up.value,Actions.right.value,Actions.down.value,Actions.left.value]
		
	def execute_action(self,a):
		x,y = self.agent
		self.agent = self.xy_MDP_slip(a,0.9) # progresses in x-y system what in the world is 'a'
	def xy_MDP_slip(self,a,p):
		x,y = self.agent
		slip_p = [p,(1-p)/2,(1-p)/2]
		check = random.random()
		# up    = 0
		# right = 1 
		# down  = 2 
		# left  = 3
		if(check <= slip_p[0]):
			a_new = a
		elif (check>slip_p[0]) & (check<=(slip_p[0]+slip_p[1])):#if the probability < random number <= probability + ((1-probability)/2)
			#decrement a but 0 changes to 3
			if(a == 0):
				a_new = 3
			else:
				a_new = a - 1
		else: #random number is > prob + (1-prob)/2
            		#increment a but 3 changes to 0
            		if(a == 3):
            			a_new = 0
            		else:
            			a_new = a + 1
            	action_new = Actions(a_new)
            	if (x,y,action_new) not in self.forbidden_transitions:#if the action is possible (ie no wall etc)
		    if action_ == Actions.up:#Update x and y accordingly
		        y+=1
		    if action_ == Actions.down:
		        y-=1
		    if action_ == Actions.left:
		        x-=1
		    if action_ == Actions.right:
		        x+=1

		self.a_new = a_new
		return (x,y)
	def get_true_propositions(self):
		"""
		Returns the string with the propositions that are True in this state
		"""
		ret = ""
		if self.agent in self.objects:
		    ret += self.objects[self.agent]
		return ret

