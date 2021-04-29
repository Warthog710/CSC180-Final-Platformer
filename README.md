# CSC 180: Final Project - Panda Runner

![Panda Runner AI Run](./images/panda_runner.gif?raw=true "Panda Runner AI Run")<br>

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
To run the game, have all the necessary packages installed, place all game files/directories in the same folder and execute ``main.py``. The game is locked to a resolution of 1280x720. Also of note, while an AI model is acting as the player, the game runs at a pseudo 60fps. This allows ample processing time for model predictions. The unfortunate side effect of this strategy is the game appears to be played in slow motion. However, due to this approach, models can be directly loaded into *Keras* as described in the *<a href="#necessary-packages">Loading a Tensorflow Model</a>* section below.

##### Game Controls:
Listed below are the game controls. Please note, an AI player is only responsible for the W and S actions.
* **W**: Jump
* **S**: Slide
* **R**: Reset
* **P**: Print model summary and current scoring information to a text file in the model's directory
* **ESC**: Quit
##### Defining Your Own Level:
This game allows you to define your own level. By default two levels are provided. They can be found under the ``assets/maps/`` directory. Maps take the form of text files with obstacles defined within. Each obstacle is defined with 4 parameters, the chunk number, obstacle type name, X offset, and Y offset. For example if I wanted to define an obstacle of type coin at chunk 34 with a Y offset of -64 I would add the following line: ``34, coin, 0, -64``. Note that no comma follows the last argument. For your information, the game currently supports 4 obstacle types. These are the saw, coin, vine, and box. To change the level the game is using, change the *GAME_MAP_PATH* path to point to the file in ``constants.py``. Note, if a new map is defined with a different length than the default maps (160 chunks) you will need to also modify the *LEVEL_LENGTH* value in ``constants.py``. This value represents the number of pixels that you must travel before you reach the end of the level. The formula to calculate this is as follows: *``[NUM_CHUNKS (default 16) / SCREEN_WIDTH (default 1280)] * Length_Of_Map_In_Chunks (default 160)``*.

***Note:*** Minimal error checking occurs for the map file, if defined incorrectly the game will likely crash.

##### Creating Your Own Dataset:
This game is equipped with the ability to create its own dataset. To do this, merely set *RECORD_SCREENSHOTS* to True in ``constants.py`` and verify that *AI_PLAYER* is False in the same file. The *SCREENSHOT_FREQUENCY* boolean can be used to change the frequency that screenshots are taken in seconds. After this, play the game as normal.

All screenshots are recorded in a ``data/`` folder. If it does not exist, it will be created. Inside this folder each individual run is stored in the following format: ``run_<week_day> <month> <day> <HH.MM.SS> <year>``. Inside each folder individuals images are stored with the following format: ``<HH.MM.SS.MS>_<action>``. The action is the particular label for that image. This can be extracted with the following Python code: ``action = (imageName.split('_')[1]).split('.')[0]``

When recording, the performance of the game will take a noticeable hit. It is only recommended to use this feature when you are collecting data to train your models with.

***Note 1:*** Taking an action (Sliding or Jumping) will trigger a screenshot to be recorded.

***Note 2:*** If a run is reset (either manually or by hitting a saw obstacle) all data up to that point for that run will be deleted.
##### Loading a Tensorflow Model:
Once you have trained your model(s) you can plug them into the game by dropping the file(s) into the ``model/`` directory. After this, change the *MODEL_NAME* variable in ``aiPlayer.py`` to the name of your model file. Note, if the model you dropped in is of type ``.pb`` with folders for its assets and variables. Leave the model name blank ('') so as to point the model loader to the entire folder.

Once a model is placed in the desired location, the variable *AI_PLAYER* in ``constants.py`` must be set to TRUE so as to load the model.

When an AI is playing the game, the game is "tricked" into thinking its running at 60fps. This allows the model to have ample processing time as it must consider each image. This essentially makes the game look as if it is being played in slow motion.

A pre-trained model is provided in the model folder. This model should be capable of completing the first map (map.txt) but will fail miserably on the second map (map2.txt).

***Note 1:*** The game resizes each image sent to the model to 224x224, normalizing its features, and converting it to type "float32". To change this behavior you would need to edit the code in ``aiPlayer.predictAction()``.

***Note 2:*** When an AI is playing the game and finishes, a text file recording its score will be placed inside the models directory. This can also be performed by pressing the **P** at anytime during an AI run.
<hr>

#### Necessary packages:
* PyGame (v2.0.14)
* PIL (v7.2.0)
* Tensorflow (v2.4.1)
* Keras (v2.4.0)

<hr>

#### Asset Sources/Licenses:
* Vine Obstacle
    * Provided by <a href="https://opengameart.org/users/fabinhosc">FabinhoSC</a> and downloaded from <a href="https://opengameart.org/content/drawing-jungle-vines">OpenGameArt.org</a>, used under license: <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>.
* Player Sprites
    * Downloaded from <a href="https://craftpix.net/freebies/free-pixel-art-tiny-hero-sprites/">CraftPix.net</a>, used under <a href="https://craftpix.net/file-licenses/">license</a>.
* Mountain/Cloud Backgrounds
    * Provided by <a href="https://vnitti.itch.io/">Vnitti</a> and downloaded from <a href="https://vnitti.itch.io/glacial-mountains-parallax-background">Itch.io</a>, used under license: <a href="https://creativecommons.org/licenses/by/4.0/">CC4.0</a>.
    * **CHANGES**: Transperent backgrounds were filled in with either the color black or white. Otherwise, the assets were used as provided.
* Grass
    * Provided by <a href="https://thorney13.itch.io/">Max Thorne</a> and downloaded from <a href="https://thorney13.itch.io/grass">Itch.io</a>, used with permission.
* Coin
    * Provided by <a href="https://opengameart.org/users/morgan3d">Morgan3d</a> and downloaded from <a href="https://opengameart.org/content/spinning-gold-coin">OpenGameArt.org</a>, used under <a href="https://creativecommons.org/licenses/by/3.0/">CC3.0</a>.
* Box
    * Provided by <a href="https://gamesupply.itch.io/">GameSupplyGuy</a> and downloaded from <a href="https://gamesupply.itch.io/blocks-walls-obstacles">Itch.io</a>, used with permission.

* Hud Font
    * Provided by <a href="https://twitter.com/somepx">Eeve Somepx</a> and downloaded from <a href="https://somepx.itch.io/humble-fonts-free">Itch.io</a>, used under license:
    ~~~
    Common Sense License (CSL)

    You CAN use these assets in your own free or paid projects.    

    You CAN modify these assets for use in your own projects.

    You CANNOT distribute or resell these assets by themselves.

    You CANNOT sell a modified version of these assets by themselves.

    Attribution is not required, but would be appreciated.

    Eeve Somepx
    @somepx

    info@somepx.com
    ~~~

