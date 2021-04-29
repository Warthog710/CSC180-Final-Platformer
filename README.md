# CSC 180: Final Project - Panda Runner

[![Panda-Runner Gif](https://s3.gifyu.com/images/Panda-Runner---AI-Run-3.38x-Speed.gif)](https://gifyu.com/image/tOzt)

#### Description:
This game was created by Quinn Roemer (Warthog710) and Logan Hollmer as a final project for <u>CSC 180 - Intelligent Systems</u> at Sacramento State University, taught by Dr. Haiquan Chen. In this project, our goal was to create an AI using a CNN image classifier that was capable of completing the game. To accomplish this, we created our own dataset using screenshots automatically captured while playing the game. These images were labelled with the correct action. This dataset was preprocessed by resizing all images to 224x224. These were then normalized, along with an OHE table of labels. Once finished a train/test split was performed. This dataset was used to train numerous custom CNN models along with many models using transfer learning from VGG16 and MobileNet. The hyper-parameters for these models were fine-tuned using a genetic algorithm with the DEAP Python library. This was done by creating a *chromosome* that represented certain hyper-parameter settings, the genetic algorithm modified this chromosome in an attempt to create the best model. Once training was complete, the best models (and some of the bad ones) were plugged into our game to see how they performed! The results of this can be seen below.
#### Results:
The custom CNN models performed well, with all top 5 models being able to complete the game successfully. However, while testing models in certain brackets we found that their ability to finish the level quickly diminished as their F1 Score fell below 0.7.  

![Custom CNN Performance Table](./images/custom_cnn_table.jpg?raw=true "Custom CNN Performance Table")<br>
***Note:*** All models with a score of >900 finished the level.

The transfer learning models also performed admirably with all but model ``[2, 0, 3, 0, 2, 5]`` able to complete the level. Like the custom CNN models, lower F1 scores tend to exhibit game halting behavior.

![Transfer Learning Performance Table](./images/transfer_learning_table.jpg?raw=true "Transfer Learning Performance Table")<br>
***Note:*** All models with a score of >900 finished the level.
#### Game Information:
To run the game, have all the necessary packages installed, place all game files/directories in the same folder and execute ``main.py``. The game is locked to a resolution of 1280x720. The controls to play the game are listed below:
* **W**: Jump
* **S**: Slide
* **R**: Reset
* **P**: Print model summary and current scoring information to a text file in the model's directory
* **ESC**: Quit

##### Creating Your Own Dataset:

##### Loading a Tensorflow Model:

##### Defining Your Own Level:

<hr>

#### Necessary packages:
* Pygame (v2.0.14)
* PIL (v7.2.0)
* Tensorflow (v2.4.1)
* Keras (v2.4.0)

<hr>

#### Asset Sources/Licenes:
