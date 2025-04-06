import random
import pygame

from src.event_manager import Event


class Background:
    TILE_SIZE = 16

    def __init__(self, game):
        self.game = game
        self.floor_tiles = []
        self.trees = []
        self.decor = []
        self.generated_floor_tiles = []
        self.generated_tree_tiles = []
        self.rows = game._world_height // self.TILE_SIZE
        self.columns = game._world_width // self.TILE_SIZE

        self.load_floor_tiles()
        self.load_trees()
        self.load_decor_items()

        self.generate_floor()
        # self.generate_foreground()
        self.sort_by_position(self.generated_tree_tiles)
        
        game._event_manager.listen_to(Event.PLAYER_MOVE, self.on_player_move)

    def load_floor_tiles(self):
        for i in range(3):
            self.floor_tiles.append(
                pygame.image.load(f"assets/background/floor_{i}.png").convert_alpha()
            )
    
    def load_trees(self):
        for i in range(2):
            self.trees.append(
                pygame.image.load(f"assets/background/tree_{i}.png").convert_alpha()
            )

    def load_decor_items(self):
        for i in range(2):
            self.decor.append(
                pygame.image.load(f"assets/background/decor_{i}.png").convert_alpha()
            )
    
    def generate_floor(self):
        for row in range(self.rows):
            for col in range(self.columns):
                x = (col * self.TILE_SIZE) -(self.game._world_width / 2)
                y = (row * self.TILE_SIZE) -(self.game._world_height / 2)
                self.generated_floor_tiles.append(self.generate_random_tile((x, y), self.floor_tiles))

    def generate_foreground(self):
        ...


    def generate_random_tile(self, position: tuple, tiles: list, weights=None):
        weights = weights or list(map(lambda x: 15 if x[0] == 0 else 1, enumerate(tiles)))

        return  {
            "position": pygame.Vector2(position),
            "tile": random.choices(tiles, weights=weights, k=1)[0]
        } 
    
    def sort_by_position(self, tiles):
        return sorted(tiles, key=lambda x: x["position"].y, reverse=True)

    def on_player_move(self, distance):
        for tile in self.generated_floor_tiles:
            tile["position"] -= pygame.Vector2(distance.data) * 2
        
        for tile in self.generated_tree_tiles:
            tile["position"] -= pygame.Vector2(distance.data) * 2

    def update(self):
        self.game._screen.fill("#3892C6")
        for tile in self.generated_floor_tiles:
            if self.game._screen.get_height() > tile["position"].y:
                self.game._screen.blit(tile["tile"], tile["position"])

        for tile in self.generated_tree_tiles:
            if self.game._screen.get_height() > tile["position"].y:
                self.game._screen.blit(tile["tile"], tile["position"])