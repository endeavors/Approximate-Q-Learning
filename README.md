#The Good Guy

##Approximate Q-Learning with Linear Function Approximation/Boltzmann Exploration Optimization/A* Search

![Alt text](https://cloud.githubusercontent.com/assets/10402322/15916830/713008d6-2dab-11e6-888b-5711098121e5.png)

### How do you run this game?
```Python
python GoodGuy.py
```

* **Why Approximate Q-Learning over Q-Learning?** 
	* Q-Learning is not feasile over very large grid spaces and moving rewards (eg. monsters on a grid space), meaning rewards whose location changes on every timestep. 

* **Linear Function Approximation**: A linear approach to calculating approximate Q-values for each (state, action) pair. Could it have been quadratic? Sure, but it depends on your case. Linearity works best here since the chosen features have a linear correspondence with each other.

* **Boltzman Exploration Optimization**: Calculates the probability of (action | state) with starting temperature of 30.0, which decreases by an decrement per episode. It simulates the process of simulated annealing. Sample the probabilities and you got yourself your next action from current state.

* **A\* Search**: What in the world! Why would you need A* in Approximate Q-Learning?
	* Manhattan distance doesn't account for walls in the grid space but A* does. We only use this when we detect walls in the Robot's sensing radius, otherwise it would be very expensive and lame. 

* GUI is built on Turlte Graphics. 
* You can customize the GUI however you like it. All features are connected, so changing one thing automatically adjusts the neighboring features (aka. responsive design)
