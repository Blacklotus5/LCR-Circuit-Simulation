import numpy as np
import scipy as sp
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
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

def plot_lcr(sol, t_eval):
  I,Q = sol.sol(t_eval)
  X = t_eval
  Y1,Y2 = I,Q
  fig1, ax = plt.subplots()
  ax.plot(X,Y1)
  ax.set_xlabel("Time")
  ax.set_ylabel("Current")
  ax.set_title('Current-Time')
  fig2, bx = plt.subplots()
  bx.plot(X,Y2)
  bx.set_xlabel("Time")
  bx.set_ylabel("Charge")
  bx.set_title('Current-Time')
  plt.show()

if __name__ == "__main__":
  L = 1e-3  # Inductance (1 mH)
  C = 1e-6  # Capacitance (1 μF)
  R = 2 * ((L / C)**0.5)    # Resistance (10 Ω)
  print(R)
  R = 0



  V = 220    # Voltage source (5 V)
  t_span = (0, 0.002) # Time span
  y0 = [0, 0]  # Initial conditions [I(0), Q(0)]

  sol = lcr_solve(L, C, R, V, t_span, y0)
  t_eval = np.linspace(t_span[0], t_span[1], 500)
  plot_lcr(sol, t_eval)
