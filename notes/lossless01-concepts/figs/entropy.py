import numpy as np
import matplotlib.pyplot as plt

def main():
    # Define the range of x values for each graph
    x1 = np.arange(0.01, 1.01, 0.01)
    x2 = np.arange(0.001, 1.00, 0.001)

    # Calculate y values for the graphs
    y1 = -np.log2(x1)
    y2 = -x2 * np.log2(x2) - (1 - x2) * np.log2(1 - x2)

    # Create a figure with two subplots, side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the first graph
    ax1.plot(x1, y1)
    ax1.set_title('Informācijas saturs')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y = -log2(x)')
    ax1.grid(True, which='both', linestyle='--', lw=0.5)
    ax1.scatter([1], [0])

    # Plot the second graph
    ax2.plot(x2, y2)
    ax2.set_title('Entropija')
    ax2.set_xlabel('x')
    ax2.set_ylim(-0.05, ax2.get_ylim()[1])  # Set the y-axis limit
    ax2.set_ylabel('y = -x*log2(x) - (1-x)*log2(1-x)')
    ax2.grid(True, which='both', linestyle='--', lw=0.5)

    # Add filled dots at (0,0) and (1,0) in the same dark blue color
    ax2.scatter([0, 1], [0, 0])

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()