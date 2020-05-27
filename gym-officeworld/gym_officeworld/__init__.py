from gym.envs.registration import register

register(
	id = 'officeworld-v0',
	entry_point='gym_officeworld.envs:OfficeWorld'
)
