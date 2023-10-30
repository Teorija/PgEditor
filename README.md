# PgEditor
*note : all artwork and assets are drawn personally
### Project Intent

After taking a course in computer graphics using OpenGL I kept getting drawn towards the idea of creating a video game, albeit a simple one. However I wasn't intereseted in creating a 3D video game, rather I wanted to create something that reminded me about old flash games I used to play. Although I could create a 2D game using C++ and OpenGL I wanted to practice my python skills. Python has a library called PyGame which is a graphics framework. Since Python has a slower performance than C++ I decided a lower resolution pixel art game would be a good fit to maximize performance. 

While starting to write my game using Python and PyGame I decided to manage my maps using a tile based system. When I was writting the code to describe the map I came to the realization that hard coding the map would be tedious and time consuming. This lead me to develop my first sub-project for the game, a map maker/level editor. 

### Usage 
- to start the editor run the main.py file from within the respository directory  

[Screencast from 2023-10-30 04:09:25 PM.webm](https://github.com/Teorija/PgEditor/assets/81877767/3175e8f0-41b1-46ef-9d6c-47940c3d6dce)

### Version 1.0 - Current Features

- create new map
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/new%20map.png)
- save map
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/save.png)
- load map
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/load.png)
- draw
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/draw.png)
- erase
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/erase.png)
- clear map
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/clear.png)
- toggle grid
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/grid.png)
- reset map position
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/reset.png)
- zoom in
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/zoom%20in.png)
- zoom out
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/zoom%20out.png)
- scroll
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/drag.png)
- add layer
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/add%20layer.png)
- delete layer
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/delete%20layer.png)
- change layer up
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/layer%20up.png)
- change layer down
![alt text](https://github.com/Teorija/PgEditor/blob/main/assets/icons/toolbar/layer%20down.png)

### Version 1.0 - To Do List

- code cleanup and documentation
- error handling for incorrect map file selection (non json)
- add keyboard shortcuts for tool functionality
- optimize rendering so that a new frame is only rendered if it differs from the previous frame
- update tilemap rendering so that it only renders what is visible on the screen
- UI aesthetic overhaul

### Version 2.0 - Planned Features

- add a selection tool for auto fill, auto tiling, cut, copy and paste
- add general auto fill tool
- extend and improve capabilities of current GUI widget library 

### Version 2.0 - To Do List

- implement a fitting design pattern
