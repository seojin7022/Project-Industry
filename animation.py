import pygame

class Animation:
    def __init__(self, obj) -> None:
        self.properties = {}
        self.property_alpha = {}
        self.property_time = {}
        self.property_start_time = {}
        self.properties_to_remove = []
        self.obj = obj

    def add_property(self, property, value, time, origin):
        self.properties.update({f"{property}": [value, origin]})
        self.property_alpha.update({f"{property}": 0})
        self.property_time.update({f"{property}": time})
        self.property_start_time.update({f"{property}": pygame.time.get_ticks()})
    def play(self):
        print("플레이")
        for property, value in self.properties.items():
            
            if self.property_alpha[property] >= 1:
                self.properties_to_remove.append(property)
                
                continue
            if property == "Alpha":
                
                self.obj.alpha =  min(max((value[0] - value[1]) * self.property_alpha[property] + value[1], 0), 255)
                
                self.property_alpha[property] = (pygame.time.get_ticks() - self.property_start_time[property]) / self.property_time[property]
            
        for property in self.properties_to_remove:
            self.properties.pop(property)
            self.property_alpha.pop(property)
            self.property_time.pop(property)
            self.property_start_time.pop(property)

        self.properties_to_remove.clear()

        if len(self.properties.keys()) == 0:
            return True
        
        return False

class AnimationController(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        pass

    def update(self):
        for sprite in self.sprites():
            sprite.animation: Animation

            isEmpty = sprite.animation.play()

            if isEmpty:
                self.remove(sprite)


