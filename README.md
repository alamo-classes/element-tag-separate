# element-tag-separate
LEGO Element Image Based Sorting Smart Assistant

# Purpose
The element sorter allows is an automated system to identify and respectively sort
LEGO elements using an image recoginition neural network. The automated system will
then run a servo subroutine to place the part in a respective bin. By running the LEGO
elements through multiple passes under different profiles, it will be possible to sort
bulk elements into discreet categories.

# System Layout
![Schematic of Mechanical Layout](images/schematic_1.jpg)
---
# Getting Started
TODO: Add pages for the wiki and how to set them up
---
# Process
## Tag
When fed from the bulk feeder, the part will tagged with a confidence interval by the Tensorflow image recognition
neural network. If the element is recognized with an appropriate confidence interval the LEGO element 
will be sorted based on its part number and color, cross referenced by category.
## Separate
The automated servos will sort the LEGO element into a category bin based on the current sorting profile. By using
successive sorting profiles, it will become possible to sort elements into more discreet groups.
## Three Pass System
1. Category - Sort the bulk lego into successively more discreet categories.
2. Part Number - Once divided into a sufficient category, the part may then be sorted by part number.
3. Color - Once divided into the respective part number, the part may be further sorted by color.
---
# GUI Interface (TODO)
* Learning for adding parts
* Mode for Separate (Category, Part Number, Color)
* Advanced Mode for Set Detection
