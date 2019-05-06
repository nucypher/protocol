

min_kappa = 0.25
T_max = 12

def calc_c_kappa(T_med, T_s):
	if T_s < T_med + 1:
		c_kappa = 0.25
	else:
		c_kappa =  min_kappa + (T_s-T_med)/float(16-T_med)

	return c_kappa

example_output1  = calc_c_kappa(T_med = 2, T_s = 3)
print(example_output1)
#0.32
example_output2  = calc_c_kappa(T_med = 10, T_s = 11)
print(example_output2)
#0.42
example_output3  = calc_c_kappa(T_med = 4, T_s = 11)
print(example_output3)
#0.83