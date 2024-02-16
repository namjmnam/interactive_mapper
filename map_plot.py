import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import simpledialog, Tk
import numpy as np
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

# Initialize Tkinter root
root = Tk()
root.withdraw()  # Hide the main window

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2, right=0.85)  # Adjust to make space for colorbar
cbar_ax = fig.add_axes([0.87, 0.15, 0.05, 0.7])  # Dedicated axes for colorbar, initially empty
cbar_ax.axis('off')  # Hide the colorbar axes until it's used
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title('Click to add a point with Z coordinate')

points = np.array([]).reshape(0, 3)  # Initialize an empty array for points
has_interpolated = False  # Track whether interpolation has been performed

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
    global has_interpolated, cbar_ax
    if len(points) > 3:  # Need at least 4 points for cubic interpolation
        # Clear the plot and conditionally the colorbar axes
        ax.clear()
        if has_interpolated:
            cbar_ax.clear()
        else:
            cbar_ax.axis('on')  # Show the colorbar axes for the first time

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Create grid and interpolate Z values
        grid_x, grid_y = np.mgrid[0:10:100j, 0:10:100j]
        grid_z = griddata(points[:, :2], points[:, 2], (grid_x, grid_y), method='cubic')
        
        # Display the interpolation
        contour = ax.imshow(grid_z.T, extent=(0, 10, 0, 10), origin='lower')
        ax.scatter(points[:, 0], points[:, 1], color='red')  # Re-plot points for visibility
        
        # Create a new colorbar in the dedicated axes
        fig.colorbar(contour, cax=cbar_ax)
        has_interpolated = True  # Update flag
        
        plt.draw()
    else:
        print("Need at least 4 points for cubic interpolation")

def plot_3d(event):
    fig_3d = plt.figure()
    ax_3d = fig_3d.add_subplot(111, projection='3d')
    xs, ys, zs = points[:,0], points[:,1], points[:,2]
    ax_3d.scatter(xs, ys, zs, color='b')
    plt.show()

# Buttons
ax_button_interpolate = plt.axes([0.7, 0.05, 0.2, 0.075])
btn_interpolate = Button(ax_button_interpolate, 'Interpolate')
ax_button_done = plt.axes([0.7, 0.15, 0.2, 0.075])
btn_done = Button(ax_button_done, 'Done')

# Connect events
btn_interpolate.on_clicked(interpolate_and_color)
btn_done.on_clicked(plot_3d)
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()