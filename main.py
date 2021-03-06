# main.py 

import random
import gym 
import numpy as np 
import sdnc_sync_env 
#from ExpectedSarsaAgent import ExpectedSarsaAgent 
from QLearningAgent import QLearningAgent 
#from SarsaAgent import SarsaAgent 
from matplotlib import pyplot as plt 
import time

# Using the gym library to create the environment 
#env = gym.make('CliffWalking-v0') 
env = sdnc_sync_env

# Defining all the required parameters 
epsilon = 0.1
total_episodes = 100
max_steps = 100
alpha = 0.5
gamma = 1

episodeReward = 0
totalReward = {
	'silly':[], 
	'SarsaAgent': [], 
	'QLearningAgent': [], 
	'ExpectedSarsaAgent': [] 
} 

APC = {
	'silly':[], 
	'SarsaAgent': [], 
	'QLearningAgent': [], 
	'ExpectedSarsaAgent': [] 
} 


# Defining all the three agents 
#expectedSarsaAgent = ExpectedSarsaAgent( 
#	epsilon, alpha, gamma, env.observation_space.n, 
#	env.action_space.n, env.action_space) 

qLearningAgent = QLearningAgent( 
	epsilon, alpha, gamma, env.n_state_space, 
	len(env.action_space), env.action_space)

#qLearningAgent = QLearningAgent( 
#    epsilon, alpha, gamma, env.observation_space.n,  
#    env.action_space.n, env.action_space)  
#sarsaAgent = SarsaAgent( 
#	epsilon, alpha, gamma, env.observation_space.n, 
#	env.action_space.n, env.action_space) 

# Now we run all the episodes and calculate the reward obtained by 
# each agent at the end of the episode 

#print("action_space:",env.action_space)
#print("state_space size:",env.n_state_space)
agents = [qLearningAgent]

start = time.time()

for agent in agents:
	for e in range(total_episodes): 
		# Initialize the necesary parameters before 
		# the start of the episode 
		t = 0
		state1 = env.reset() 
		print("first_state:",state1)
		action1 = agent.choose_action(state1)
		print("action1",action1)
		#action1 = random.choice(env.action_space) 
		episodeReward = 0
		episodeAPCs = 0
		while t < max_steps: 

		# 	# Getting the next state, reward, and other parameters 
			state2, reward, done, info = env.step(action1)
			print("Ep",e,"t:",t+1,"next_state:",state2,"reward:",round(reward))
		# 	# Choosing the next action 
			action2 = agent.choose_action(state2) 
			#print("action:",action2)
			#action2 = random.choice(env.action_space)
			
		# 	# Learning the Q-value 
			agent.update(state1, state2, reward, action1, action2)
			state1 = state2
			action1 = action2 
			
		# 	# Updating the respective vaLues 
			t += 1
			episodeReward += reward 
			#sepisodeAPCs += info["APC"]
			
		# 	# If at the end of learning process 
			if done:
				break

		# Append the sum of reward at the end of the episode 
		totalReward[type(agent).__name__].append(episodeReward)
		#totalReward["silly"].append(round(episodeReward,2)) 
		#sAPC[type(agent).__name__].append(episodeAPCs) 


end = time.time()
print("total time: " + str(end-start))

# Calculate the mean of sum of returns for each episode 
#meanReturn = { 
#	'SARSA-Agent': np.mean(totalReward['SarsaAgent']), 
#	'Q-Learning-Agent': np.mean(totalReward['QLearningAgent']), 
#	'Expected-SARSA-Agent': np.mean(totalReward['ExpectedSarsaAgent']) 
#} 

# Print the results 
#print(f"SARSA Average Sum of Reward: {meanReturn['SARSA-Agent']}") 
#print(f"Q-Learning Average Sum of Return: {meanReturn['Q-Learning-Agent']}") 
#print(f"Expected Sarsa Average Sum of Return: {meanReturn['Expected-SARSA-Agent']}") 
print(totalReward)
#print(APC)


#plt.plot(totalReward["silly"])
plt.plot(totalReward["QLearningAgent"])
#splt.plot(APC[type(agent).__name__])
plt.show()
