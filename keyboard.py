class EditorKeyboardData:
    def __init__(self) -> None:
        self.data = {
            'arrow keys' : {
                            'left':0, 'right':0, 'up':0, 'down':0
                           },

            'regular keys' : {
                              'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0,
                              'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0,
                              'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0,
                              's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0,
                              'y':0, 'z':0, ' ':0, 'del':0, '1':0, '2':0,
                              '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, 
                              '9':0, '0':0
                             },
                             
            'special keys' : {
                              'esc':0
                             }
                            
        }

    def reset_key_status(self) -> None:
        self.data['regular keys'] = {key:0 for key in self.data['regular keys']}
        self.data['special keys'] = {key:0 for key in self.data['special keys']}