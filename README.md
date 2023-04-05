# ROS-challenge
ROSbot challenge
This project served as a learning tool for ROS kinetic
The challenge involved navigating an unknown environment using a Husarion ROSbot 1
The ROSbot is to navigate within the shortest time and distance without colliding with any obstacles

![image](https://user-images.githubusercontent.com/73953831/159933152-c4102aea-eb6a-47d8-ab07-9615177344a0.png)

The Scripts include:
An avoidance node which makes use of the onboard Lidar and Infrared sensors

![image](https://user-images.githubusercontent.com/73953831/159933574-ea7e36ef-ba54-4c72-a340-0479e237dbe8.png)
![image](https://user-images.githubusercontent.com/73953831/159933614-40505598-47b0-4d53-89be-8eaa3c79a8f6.png)

The avoidance node segments the Lidar into 8, 45 degree zones and determines which zone has no obsticales

![image](https://user-images.githubusercontent.com/73953831/159934082-015ba35d-4c2a-489c-9e2f-ced74ff0ef9f.png)

Once the ROSbot has successfully avoided, a Yaw correction node ensures the orientation is corrected

![image](https://user-images.githubusercontent.com/73953831/159935467-e178b25f-2712-4206-bfaf-dca5064898a7.png)

A planner node determines if the ROSbot should avoid, correct yaw or acelerate/decelerate 
