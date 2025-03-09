# Unit class has shared properties of PLayer and Mob classes

class Unit:
    # properties can and will be overridden
    def __init__(self, pos, speed = 5, max_health = 100):
        self._max_health = max_health
        self._current_health = max_health
        self._speed = speed
        self._pos = pos

    def move(self, dx, dy):
        self._pos.x += dx * self._speed
        self._pos.y += dy * self._speed

    def take_damage(self, amount):
        self._current_health -= amount
        if self._current_health <= 0:
            self._current_health = 0 

    @property
    def is_dead(self):
        return self._current_health <= 0