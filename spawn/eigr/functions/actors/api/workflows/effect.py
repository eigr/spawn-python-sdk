
class Effect:
    def __init__(self, action: str, system: str, actor: str, parent: str, payload: any = None):
        self.action = action
        self.actor = actor
        self.system = system
        self.parent = parent
        self.payload = payload
