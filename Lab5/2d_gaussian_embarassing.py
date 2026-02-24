import time
import sys
import numpy as np
import matplotlib.pyplot as plt

STEP = 0.0011

def gaussian_2d(x, y, sigma):
    """Calculate 2D Gaussian value at (x, y)."""
    return (1 / (2 * np.pi * sigma**2)) * np.exp(
        -1 * (x**2 + y**2) / (2 * sigma**2)
    )

def plot(z):
    """Plot 2D Gaussian data."""
    plt.imshow(z.T)
    plt.gca().invert_yaxis()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{z.shape} points")
    plt.gca().set_aspect(1)

def main(xmin, xmax, ymin, ymax, sigma=1):
    """Generate and plot 2D Gaussian."""
    x = np.arange(float(xmin), float(xmax), STEP)
    y = np.arange(float(ymin), float(ymax), STEP)
    z = []
    for x_val in x:
        for y_val in y:
            z.append(gaussian_2d(x_val, y_val, sigma))
    zz = np.array(z).reshape(len(x), len(y))
    plot(zz)

if __name__ == "__main__":
    start = time.time()
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elapsed = time.time() - start
    print(f"Elapsed Time: {elapsed}s")
    plt.show()