from tkinter import *
import customtkinter, tkinter
from lcrsim import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk) 

# Global variables for the plots
fig1, ax1 = None, None
fig2, ax2 = None, None
canvas1 = None
toolbar1 = None

def plot_lcr():
    global fig1, ax1, fig2, ax2, canvas1, toolbar1
    
    try:
        # Get values from entries
        L = float(my_entry.get()) * 1e-3  # Convert to H
        C = float(my_entry2.get()) * 1e-6  # Convert to F
        R = float(my_entry3.get())  # Ω
        V = 220  # Voltage source (220 V)
        t_span = (0, 0.002)  # Time span
        y0 = [0, 0]  # Initial conditions [I(0), Q(0)]
        
        # Solve the LCR circuit
        sol = lcr_solve(L, C, R, V, t_span, y0)
        t_eval = np.linspace(t_span[0], t_span[1], 500)
        I, Q = sol.sol(t_eval)
        
        # Clear previous plots if they exist
        if ax1:
            ax1.clear()
        if ax2:
            ax2.clear()
            
        # Create figures if they don't exist
        if fig1 is None:
            fig1 = Figure(figsize=(5, 4), dpi=100)
            ax1 = fig1.add_subplot(111)
            canvas1 = FigureCanvasTkAgg(fig1, tab_1)
            canvas_widget = canvas1.get_tk_widget()
            canvas_widget.pack(side=TOP, fill=BOTH, expand=1)
            toolbar1 = NavigationToolbar2Tk(canvas1, tab_1)
            toolbar1.update()
            canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        # Plot current
        ax1.plot(t_eval, I)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Current")
        ax1.set_title('Current-Time')
        canvas1.draw()
        
        # You can add similar code for the second plot (Q) if needed
        
    except ValueError as e:
        print("Error:", e)
        # You might want to show an error message to the user

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    app = customtkinter.CTk()
    app.title("LCR Circuit Simulator")

    my_tab = customtkinter.CTkTabview(master=app, width=800, height=350, corner_radius=10)
    my_tab.pack(pady=20)

    tab_1 = my_tab.add("V-T")
    tab_2 = my_tab.add("Phasor")

    frame2 = customtkinter.CTkFrame(master=app, width=300, height=300, corner_radius=10)
    frame2.pack(side=RIGHT, padx=100, pady=10)

    my_entry = customtkinter.CTkEntry(master=frame2,
        placeholder_text="Enter Inductance(L) in mH")
    my_entry.pack(pady=10)
    my_entry.insert(0, "1")  # Default value

    my_entry2 = customtkinter.CTkEntry(frame2,
        placeholder_text="Enter Capacitance(C) in μF")
    my_entry2.pack(pady=10)
    my_entry2.insert(0, "1")  # Default value

    my_entry3 = customtkinter.CTkEntry(frame2,
        placeholder_text="Enter Resistance(R) in Ω")
    my_entry3.pack(pady=10)
    my_entry3.insert(0, "10")  # Default value

    button1 = customtkinter.CTkButton(frame2,
        text="Plot",
        command=plot_lcr,
        height=10,
        width=80,
        font=("Arial", 20))
    button1.pack(pady=20)

    frame1 = customtkinter.CTkFrame(master=app, width=300, height=300, corner_radius=10)
    frame1.pack(side=LEFT, padx=100, pady=10)

    def slider(value):
        text_var_r.set(f"{int(slider.get())}")

    slider = customtkinter.CTkSlider(master=frame1,
        from_=0,
        to=100,
        command=slider)
    slider.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    text_var_r = tkinter.StringVar(value="0")
    laber_r = customtkinter.CTkLabel(master=frame1,
        textvariable=text_var_r,
        width=120,
        height=25,
        fg_color=("black", "black"),
        text_color="white",
        font=('Arial', 40),
        corner_radius=8)
    laber_r.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

    text_2 = tkinter.StringVar(value="Forced Frequency")
    laber2 = customtkinter.CTkLabel(master=frame1,
        textvariable=text_2,
        width=100,
        height=25,
        fg_color=("black", "black"),
        text_color="white",
        font=('Arial', 20),
        corner_radius=8)
    laber2.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

    app.mainloop()