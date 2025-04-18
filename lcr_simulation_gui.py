import numpy as np
from scipy.integrate import solve_ivp
import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Global variables
forced_mode = False
current_fig, current_ax = None, None
charge_fig, charge_ax = None, None

def unforced_lcr_solve(L, C, R, V, t_span, y0):
    """Solve unforced LCR circuit (step response)"""
    def rhs(t, y):
        I, Q = y
        dIdt = (-R*I - Q/C + V)/L
        dQdt = I
        return [dIdt, dQdt]
    return solve_ivp(rhs, t_span, y0, dense_output=True)

def forced_lcr_solve(L, C, R, V, omega, t_span, y0):
    """Solve forced LCR circuit (AC response)"""
    def rhs(t, y):
        I, Q = y
        V_t = V * np.sin(omega * t)
        dIdt = (V_t - R*I - Q/C)/L
        dQdt = I
        return [dIdt, dQdt]
    return solve_ivp(rhs, t_span, y0, dense_output=True)

def toggle_mode():
    global forced_mode
    forced_mode = mode_switch.get()
    if forced_mode:
        freq_frame.pack(fill=tk.X, pady=5)
    else:
        freq_frame.pack_forget()
    update_plot()

def on_freq_change(value):
    freq_value.set(f"{float(value):.1f} Hz")
    update_plot()

def update_plot():
    global current_fig, current_ax, charge_fig, charge_ax
    
    try:
        # Get parameters from UI
        L = float(l_entry.get()) * 1e-3  # mH to H
        C = float(c_entry.get()) * 1e-6  # μF to F
        R = float(r_entry.get())         # Ω
        V = float(v_entry.get())         # V
        
        if forced_mode:
            f = float(freq_slider.get())  # Hz
            omega = 2 * np.pi * f         # rad/s
            # Adjust time span based on frequency
            t_span = (0, 5/f) if f > 0 else (0, 0.1)
        else:
            omega = 0
            t_span = (0, 0.002)  # Fixed time span for unforced case
            
        t_eval = np.linspace(t_span[0], t_span[1], 1000)
        
        # Solve the circuit
        if forced_mode:
            sol = forced_lcr_solve(L, C, R, V, omega, t_span, [0, 0])
        else:
            sol = unforced_lcr_solve(L, C, R, V, t_span, [0, 0])
            
        I, Q = sol.sol(t_eval)
        
        # Update current plot
        current_ax.clear()
        current_ax.plot(t_eval, I, 'b', linewidth=1)
        current_ax.set_xlabel("Time (s)")
        current_ax.set_ylabel("Current (A)")
        
        if forced_mode:
            title = f"Forced Response (f = {f:.1f} Hz, ω = {omega:.1f} rad/s)"
            if f == 0:
                title += " (DC Case)"
        else:
            title = "Natural Response (No Forcing)"
            
        current_ax.set_title(title)
        current_canvas.draw()
        
        # Update charge plot
        charge_ax.clear()
        charge_ax.plot(t_eval, Q, 'r', linewidth=1)
        charge_ax.set_xlabel("Time (s)")
        charge_ax.set_ylabel("Charge (C)")
        charge_ax.set_title("Charge vs Time")
        charge_canvas.draw()
        
    except ValueError as e:
        print(f"Error: {e}")

# Main window setup
root = ctk.CTk()
root.title("LCR Circuit Simulator")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Main container
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left panel - Controls
control_frame = ctk.CTkFrame(main_frame, width=300)
control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

# Circuit parameters
ctk.CTkLabel(control_frame, text="Circuit Parameters", font=("Arial", 14, "bold")).pack(pady=5)

# Create parameter entries
def create_param_entry(frame, label, default, unit):
    param_frame = ctk.CTkFrame(frame)
    param_frame.pack(fill=tk.X, pady=2)
    ctk.CTkLabel(param_frame, text=f"{label} ({unit})", width=120).pack(side=tk.LEFT)
    entry = ctk.CTkEntry(param_frame)
    entry.insert(0, default)
    entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    return entry

l_entry = create_param_entry(control_frame, "Inductance", "1", "mH")
c_entry = create_param_entry(control_frame, "Capacitance", "1", "μF")
r_entry = create_param_entry(control_frame, "Resistance", "10", "Ω")
v_entry = create_param_entry(control_frame, "Voltage", "220", "V")

# Operation mode switch
mode_switch = ctk.CTkSwitch(
    control_frame, 
    text="Forced Oscillation", 
    command=toggle_mode
)
mode_switch.pack(pady=10)

# Frequency control frame (initially hidden)
freq_frame = ctk.CTkFrame(control_frame)
freq_label = ctk.CTkLabel(freq_frame, text="Forced Frequency (Hz)")
freq_label.pack(pady=5)

freq_value = tk.StringVar(value="50.0 Hz")
freq_display = ctk.CTkLabel(freq_frame, textvariable=freq_value, font=('Arial', 20))
freq_display.pack(pady=5)

freq_slider = ctk.CTkSlider(
    freq_frame, from_=0, to=1000, command=on_freq_change
)
freq_slider.set(50)
freq_slider.pack(fill=tk.X, padx=10, pady=5)

# Update button
update_btn = ctk.CTkButton(
    control_frame, text="Update Plot", command=update_plot
)
update_btn.pack(pady=10)

# Right panel - Plots
plot_frame = ctk.CTkFrame(main_frame)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Tab view for different plots
tabview = ctk.CTkTabview(plot_frame)
tabview.pack(fill=tk.BOTH, expand=True)

current_tab = tabview.add("Current-Time")
charge_tab = tabview.add("Charge-Time")

# Current plot setup
current_fig = Figure(figsize=(6, 4), dpi=100)
current_ax = current_fig.add_subplot(111)
current_canvas = FigureCanvasTkAgg(current_fig, current_tab)
current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
NavigationToolbar2Tk(current_canvas, current_tab).update()

# Charge plot setup
charge_fig = Figure(figsize=(6, 4), dpi=100)
charge_ax = charge_fig.add_subplot(111)
charge_canvas = FigureCanvasTkAgg(charge_fig, charge_tab)
charge_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
NavigationToolbar2Tk(charge_canvas, charge_tab).update()

# Initial plot
update_plot()

root.mainloop()