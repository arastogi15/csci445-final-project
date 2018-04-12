#CSCI 445 Final Project

##Week 1 Assignments:

##Person 1: Jacob
marker odometry adjustment
rotating about the marker


##Person 2: Preston
interacting with yml file and building path-following
human does path decision-making on house image
obstacle avoidance?

##Person 3: Ankur
integrating localization + camera data together and moving robot along some specified path..
softer assignment of obstacle avoidance?

Obstacle avoidance:
paths that exist
do calculations for which paths are affected and how
maybe determine robot’s course of action in these situations



## Scratch Notes
Knowns:
paths/lines + colors
obstacle locations

Some Functionalities We need to build:
Rotating about marker
Localization + Camera Integration
this is pretty big...
Positioning marker based on odometry
How to draw a line and bezier curve
go to goals…
assess obstacles
Planning-stage;
how do you select for the order of line segments/paths…
Translating path positions into odometry positions.



Case 1: Let’s think about the basic case: 4 line segments, a rectangle, all in field of vision of camera, and no color changes.

We need to:
(assess the line segments and decide on an order of points.)


Move to the start of the segment sequence.
Draw along the segment sequence.
NOTE: rotations are important here 

Case 2: Let’s think about the basic case: 4 line segments, a rectangle, all in field of vision of camera, and no color changes.


obstacle avoidance








Specific issues:
rotating about a marker point
Thinking about going backwards
dealing with obstacles