## Distance Process

### Reward Function
```python
# best reward function
def progress_reward(params):
    progress = params['progress']
    return 1 - ((100 - progress) / 100)**0.4
def completion_reward(params):
    steps = params['steps']
    if params['progress'] >= 99.99:
        if steps > 600: # 40 seconds
            return 1.
        elif steps < 150: # 10 seconds
            return 2.0
        else:
            return 2 - (steps-150)/450
    return 0.
def reward_function(params):
    complete = completion_reward(params)
    if complete:
        return complete
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    # Calculate 3 markers that are increasingly further away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 0.  # likely crashed/ close to off track
    return progress_reward(params) * reward
```

### Action space
> Speed: [ 1.2 : 2.5 ] m/s

> Steering angle: [ -20 : 30 ] °

### Hyperparameter
	
> Gradient descent batch size	64

> Entropy	0.01

> **Discount factor**	0.99

> Loss type	Huber

> Learning rate	0.0003

> **Number of experience episodes between each policy-updating iteration**	40

> Number of epochs	10