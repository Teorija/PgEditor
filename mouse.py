class Mouse:
    def __init__(self) -> None:
        self.data = {
            'pos': (),
            'l_click': 0,
            'l_clicking': 0,
            'r_click': 0,
            'r_clicking': 0
        }
    
    def reset_click_status(self) -> None:
        self.data['l_click'] = 0
        self.data['r_click'] = 0