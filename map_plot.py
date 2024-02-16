import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import simpledialog, Tk
import numpy as np
from scipy.interpolate import griddata

# Initialize Tkinter root
root = Tk()
root.withdraw()  # Hide the main window

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2, right=0.8)  # Make space for button and colorbar
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title('Click to add a point with Z coordinate')

points = np.array([]).reshape(0, 3)  # Initialize an empty array for points
colorbar_ax = None  # Track colorbar axes

def onclick(event):
    # Ensure click is within the plot and not on the button
    if event.inaxes == ax:
        if event.xdata is not None and event.ydata is not None:
            z = simpledialog.askfloat("Input", "Enter Z coordinate:", parent=root)
            if z is not None:  # Check if Z was input
                global points
                points = np.vstack([points, [event.xdata, event.ydata, z]])  # Add new point
                ax.plot(event.xdata, event.ydata, 'ko')  # Plot point
                ax.text(event.xdata, event.ydata, f'{z}', color='red')
                plt.draw()

def interpolate_and_color(event):
    global colorbar_ax
    if len(points) > 3:  # Need at least 4 points for cubic interpolation
        # Create grid
        grid_x, grid_y = np.mgrid[0:10:100j, 0:10:100j]
        # Interpolate Z values
        grid_z = griddata(points[:, :2], points[:, 2], (grid_x, grid_y), method='cubic')
        # Clear the plot to display interpolation
        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        contour = ax.imshow(grid_z.T, extent=(0, 10, 0, 10), origin='lower')
        ax.scatter(points[:, 0], points[:, 1], color='red')  # Re-plot points for visibility

        # Remove previous colorbar axes if exist
        if colorbar_ax:
            fig.delaxes(colorbar_ax)
            fig.subplots_adjust(right=0.8)  # Adjust subplot to make space for new colorbar
        colorbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])  # Create new axes for colorbar
        fig.colorbar(contour, cax=colorbar_ax)  # Create a new colorbar
        
        plt.draw()
    else:
        print("Need at least 4 points for cubic interpolation")

# Button
ax_button = plt.axes([0.7, 0.05, 0.2, 0.075])
btn = Button(ax_button, 'Interpolate')

# Connect events
btn.on_clicked(interpolate_and_color)
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
