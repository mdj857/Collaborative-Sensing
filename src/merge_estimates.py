from __future__ import division
'''
This function returns a merged estimate of the state variables given the state estimates
for each sensor and the variance of each parameter for each sensor. 
The merged estimate for an arbitrary state parameter x0 is: 
a*x0_sensor1 + (1-a)*x0_sensor2

where a is: 

(var_x0_sensor1/(var_x0_sensor1 + var_x0_sensor2)

and 1 - a is: 

(var_x0_sensor2/(var_x0_sensor1 + var_x0_sensor2)

In this way, the sensor estimate with the least amount of uncertainty is "weighted" heavier 
and the coefficients for the estimates are normalized between [0,1] and we have that the sum of 
normalized coefficients = 1. 
Therefore in the "worst case" we just output the estimate for a single sensor. 
'''
def merge_estimates(w_sensor1, w_hat_sensor1, w_var_sensor1, w_hat_var_sensor1, 
					w_sensor2, w_hat_sensor2, w_var_sensor2, w_hat_var_sensor2): 

	
	# compute merged estimate for w
	a_w = (w_var_sensor1/(w_var_sensor1 + w_var_sensor2))
	merged_w = (1-a_w)*w_sensor1 + a_w*w_sensor2

	# compute merged estimate for w_hat
	a_w_hat = (w_var_sensor1/(w_var_sensor1 + w_var_sensor2))
	merged_w_hat = (1-a_w_hat)*w_hat_sensor1 + a_w_hat*w_hat_sensor2

	return(merged_w,merged_w_hat)


