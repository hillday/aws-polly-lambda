## Example3
[aws-deepracer](https://www.linkedin.com/pulse/samples-reward-functions-aws-deepracer-bahman-javadi?trk=public_profile_article_view)

### Reward Function
```python
def reward_function(params):
    center_variance = params["distance_from_center"] / params["track_width"]
    #racing line
    left_lane = [23,24,50,51,52,53,61,62,63,64,65,66,67,68]#Fill in the waypoints
    center_lane = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,54,55,56,57,58,59,60,69,70]#Fill in the waypoints
    right_lane = [29,30,31,32,33,34]#Fill in the waypoints
    #Speed
    fast = [0,1,2,3,4,5,6,7,8,9,25,26,27,28,29,30,31,32,51,52,53,54,61,62,63,64,65,66,67,68,69,70] #3
    moderate = [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,55,56,57,58,59,60] #2
    slow = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24] #1

    reward = 30

    if params["all_wheels_on_track"]:
        reward += 10
    else:
        reward -= 10

    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.4:
        reward += 10
    else:
        reward -= 10

    if params["closest_waypoints"][1] in fast:
        if params["speed"] > 1.5 :
            reward += 10
        else:
            reward -= 10

    elif params["closest_waypoints"][1] in moderate:
        if params["speed"] > 1 and params["speed"] <= 1.5 :
            reward += 10
        else:
            reward -= 10
    elif params["closest_waypoints"][1] in slow:
        if params["speed"] <= 1 :
            reward += 10
        else:
            reward -= 10

    return float(reward)
```

### Action space
> Speed: [ 0.9 : 2.5 ] m/s

> Steering angle: [ -30 : 30 ] °

### Hyperparameter
	
> Gradient descent batch size	64

> Entropy	0.01

> Discount factor	0.999

> Loss type	Huber

> Learning rate	0.0003

> Number of experience episodes between each policy-updating iteration	20

> Number of epochs	10