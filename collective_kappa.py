# alter the ratio of rewards to long and short sub-stakes based on the total distribution temporally

small_stake_multiplier = 0.5
T_max = 12

def calc_c_kappa(T_med, T_s):
	if T_s > T_med:
		c_kappa = (min(T_s, T_max) - T_med) / float(T_max * 2) + small_stake_multiplier
	else:
		c_kappa =  (1 + ((min(T_s, T_max) - T_med) / float(T_max))) / 2

	return c_kappa

example_output = calc_c_kappa(T_med = 4, T_s = 11)

print(example_output)