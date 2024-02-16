import matplotlib.pyplot as plt
from tkinter import simpledialog, Tk
import numpy as np

# Initialize Tkinter root
root = Tk()
root.withdraw() # Hide the main window

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title('Click to add a point with Z coordinate')

points = []

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        # Prompt for Z coordinate
        z = simpledialog.askfloat("Input", "Enter Z coordinate:",
                                  parent=root,
                                  minvalue=-np.inf, maxvalue=np.inf)
        if z is not None: # Check if Z was input
            # Add point and Z value as text
            ax.plot(event.xdata, event.ydata, 'ko') # 'ko' creates a black dot
            ax.text(event.xdata, event.ydata, f'{z}', color='red')
            points.append((event.xdata, event.ydata, z))
            plt.draw()

# Connect the click event to the onclick function
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
