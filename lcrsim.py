import numpy as np
import scipy as sp
from scipy.integrate import solve_ivp
import math as m

# Case 1 : RLC Circuit - LC Oscillations, Damped, Underdamped, Overdamped

def lcr_eq(t,y,L,C,R,V):
	I, Q = y
	#V_t = V * np.sin(omega * t) #Sinusoidal
	dIdt = (V - R*I - Q / C) / L
	dQdt = I
	return [dIdt, dQdt]

def lcr_solve(L,C,R,V,t_span,y0):
	sol = solve_ivp(lcr_eq, t_span, y0, args=(L,C,R,V), dense_output=True)
	return sol



