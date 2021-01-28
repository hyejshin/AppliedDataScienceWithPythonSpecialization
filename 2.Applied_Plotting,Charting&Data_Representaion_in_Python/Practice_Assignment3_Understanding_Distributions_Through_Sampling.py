# Understanding Distributions Through Sampling

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

%matplotlib notebook

# generate 4 random variables from the random, gamma, exponential, and uniform distributions
x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000)+7
x4 = np.random.uniform(14,20, 10000)

# plot the histograms
plt.figure(figsize=(9,3))
plt.hist(x1, normed=True, bins=20, alpha=0.5)
plt.hist(x2, normed=True, bins=20, alpha=0.5)
plt.hist(x3, normed=True, bins=20, alpha=0.5)
plt.hist(x4, normed=True, bins=20, alpha=0.5);
plt.axis([-7,21,0,0.6])

plt.text(x1.mean()-1.5, 0.5, 'x1\nNormal')
plt.text(x2.mean()-1.5, 0.5, 'x2\nGamma')
plt.text(x3.mean()-1.5, 0.5, 'x3\nExponential')
plt.text(x4.mean()-1.5, 0.5, 'x4\nUniform')

#################


n = 300
x = np.random.randn(n)

def animate(curr):
    if curr == n:
        a.event_source.stop()
    plt.cla()
    bins = np.arange(-7, 21, 0.1)
    plt.hist(x1[:curr], normed=True, bins=10, alpha=0.5)
    plt.hist(x2[:curr], normed=True, bins=10, alpha=0.5)
    plt.hist(x3[:curr], normed=True, bins=10, alpha=0.5)
    plt.hist(x4[:curr], normed=True, bins=10, alpha=0.5);
    plt.axis([-7,21,0,0.6])
    
    plt.text(x1.mean()-1.5, 0.5, 'x1\nNormal')
    plt.text(x2.mean()-1.5, 0.5, 'x2\nGamma')
    plt.text(x3.mean()-1.5, 0.5, 'x3\nExponential')
    plt.text(x4.mean()-1.5, 0.5, 'x4\nUniform')

    plt.annotate('n = {}'.format(curr), [0,0.6])

fig = plt.figure()
a = animation.FuncAnimation(fig, animate, interval=10)

# # Set up formatting for the movie files
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)

# # create animation using the animate() function with no repeat
# myAnimation = animation.FuncAnimation(fig, animate, frames=300, interval=20, blit=True, repeat=False)
# myAnimation.save('myAnimation.mp4', writer=writer)