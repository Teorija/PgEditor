# PgEditor
### Project Intent

After taking a course in computer graphics using OpenGL I kept getting drawn towards the idea of creating a video game, albeit a simple one. However I wasn't intereseted in creating a 3D video game, rather I wanted to create something that reminded me about old flash games I used to play. Although I could create a 2D game using C++ and OpenGL I wanted to practice my python skills. Python has a library called PyGame which is a graphics framework. Since Python has a slower performance than C++ I decided a lower resolution pixel art game would be a good fit to maximize performance. 

While starting to write my game using Python and PyGame I decided to manage my maps using a tile based system. When I was writting the code to describe the map I came to the realization that hard coding the map would be tedious and time consuming. This lead me to develop my first sub-project for the game, a map maker/level editor. 

### Version 1.0 - Current Features

- create new map
- save map
- load map
- draw
- erase
- clear map
- toggle grid
- reset map position
- zoom in
- zoom out
- scroll
- add layer
- delete layer
- change layer up
- change layer down

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

### Version 2.0 - To Do List

- implement a fitting design pattern
