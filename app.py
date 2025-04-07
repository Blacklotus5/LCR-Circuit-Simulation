from tkinter import *
import customtkinter,tkinter
from lcrsim import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk) 

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
	canvas = FigureCanvasTkAgg(fig1, tab_1)
	canvas_widget = canvas.get_tk_widget()
	canvas_widget.pack()
	toolbar = NavigationToolbar2Tk(canvas, 
								master=window) 
	toolbar.update() 


if __name__ == "__main__":
  L = 1e-3  # Inductance (1 mH)
  C = 1e-6  # Capacitance (1 μF)
  R = 2 * ((L / C)**0.5)    # Resistance (10 Ω)
  print(R)
  R = 10



  V = 220    # Voltage source (5 V)
  t_span = (0, 0.002) # Time span
  y0 = [0, 0]  # Initial conditions [I(0), Q(0)]

  sol = lcr_solve(L, C, R, V, t_span, y0)
  t_eval = np.linspace(t_span[0], t_span[1], 500)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
#customtkinter.set_window_scaling(1.5)
#customtkinter.set_widget_scaling(1.5)
app = customtkinter.CTk()

my_tab = customtkinter.CTkTabview(master=app,width=800,height=350,corner_radius=10) # Adding tabs
my_tab.pack(pady=20)

tab_1 = my_tab.add("V-T")

tab_2 = my_tab.add("Phasor")

frame2 = customtkinter.CTkFrame(master=app,width=300,height=300,corner_radius=10)
frame2.pack(side=RIGHT,padx=100,pady=10)

my_entry = customtkinter.CTkEntry(master=frame2,
	placeholder_text = "Enter Inductance(L)",
	)
my_entry.pack(pady=20)
L = my_entry.get()
my_entry2 = customtkinter.CTkEntry(frame2,
	placeholder_text = "Enter Capacitance(C)",
	)
my_entry2.pack(pady=20)
C = my_entry2.get()

my_entry3 = customtkinter.CTkEntry(frame2,
	placeholder_text = "Enter Resistance(R)",
	)
my_entry3.pack(pady=20)
R = my_entry3.get()

button1 = customtkinter.CTkButton(frame2,
	text = "Set",
	command = lambda: plot_lcr(sol,t_eval),
	height=10,
	width=80,
	font=("Arial", 20)
	)
button1.pack(pady=20)

frame1 = customtkinter.CTkFrame(master=app,width=300,height=300,corner_radius=10)
frame1.pack(side=LEFT,padx=100,pady=10)



def slider(value):							# Slider function
	text_var_r.set(f"{int(slider.get())}")

slider = customtkinter.CTkSlider(master=frame1,	# Slider function
	from_=0,
	to=100,
	command=slider)

slider.place(relx=0.5,rely=0.4,anchor=tkinter.CENTER)

text_var_r = tkinter.StringVar(value="")

laber_r = customtkinter.CTkLabel(master=frame1,
	textvariable = text_var_r,
	width = 120,
	height = 25,
	fg_color=("black", "black"),
	text_color="white",
	font=('Arial',40),
	corner_radius=8)

laber_r.place(relx=0.5,rely=0.6,anchor=tkinter.CENTER)

text_2 = tkinter.StringVar(value="Forced Frequency")

laber2 = customtkinter.CTkLabel(master=frame1,
	textvariable = text_2,
	width = 100,
	height = 25,
	fg_color=("black", "black"),
	text_color="white",
	font=('Arial',20),
	corner_radius=8)

laber2.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)


app.mainloop()



