class Input:
    def __init__(self, text):
        self.text = text

# used only for article POST request
    def mapToJSON(self):
        return {
            "text": self.text 
        }
