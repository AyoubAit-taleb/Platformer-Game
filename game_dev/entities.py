import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type   # Player Or enemy
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def update(self, tilemap, movement=(0, 0)):
        #Reset collision
        self.collisions = {'up': False, 
                           'down': False, 
                           'right': False, 
                           'left': False}
        
        # calculate frame movment
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        #Horizontal Movement and Collision Detection
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        #Vertical
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
       
        #Gravity and Vertical Velocity Adjustment
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        
        #Reset Vertical Velocity on Collision
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        

    #Drawing the entity onto a given surface 
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
        