
class Action:
    def __init__(self, target, full, title, short):
        self.target = target
        self.full = full
        self.title = title
        self.short = short

    def __repr__(self):
        return '{"destructive":0, "full":"%s", "title":"%s", "short":"%s","identifier":"%s"}'%(self.title, self.full, self.short, self.target)
        
