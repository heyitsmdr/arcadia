from evennia import Command

SYMBOLS = {
    None: '[ ]',
    'you': '[@]',
    'SECT_INSIDE': '[ ]'
}


class CmdMap(Command):
    """
    Toggles the map when looking at the current room.

    Usage: map
    """
    key = "map"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        if self.caller.db.map_enabled:
            self.caller.db.map_enabled = False
            self.caller.msg("Map is now disabled.")
        else:
            self.caller.db.map_enabled = True
            self.caller.msg("Map is now enabled.")


def median(num):
    lst = sorted(range(0, num))
    n = len(lst)
    m = n - 1
    return (lst[n // 2] + lst[m // 2]) / 2.0


class Map(object):
    def __init__(self, caller, max_width=7, max_length=7):
        self.caller = caller
        self.max_width = max_width
        self.max_length = max_length
        self.worm_has_mapped = {}
        self.curX = None
        self.curY = None

        if self.check_grid():
            self.grid = self.create_grid()
            self.draw_room_on_map(caller.location, ((min(max_width, max_length) - 1) / 2))

    def create_grid(self):
        """Creates an empty grid/display area."""
        board = []
        for row in range(self.max_width):
            board.append([])
            for column in range(self.max_length):
                board[row].append('   ')
        return board

    def check_grid(self):
        """Ensures max_l and max_w are odd numbers."""
        return True if self.max_length % 2 != 0 or self.max_width % 2 != 0 else False

    def draw_room_on_map(self, room, max_distance):
        self.draw(room)

        if max_distance == 0:
            return

        for exit in room.exits:
            if exit.name not in ("north", "south", "east", "west"):
                continue
            if self.has_drawn(exit.destination):
                continue

            self.update_pos(room, exit.name.lower())
            self.draw_room_on_map(exit.destination, max_distance - 1)

    def draw(self, room):
        if room == self.caller.location:
            self.start_loc_on_grid()
            self.worm_has_mapped[room] = [self.curX, self.curY]
        else:
            self.worm_has_mapped[room] = [self.curX, self.curY]
            self.grid[self.curX][self.curY] = SYMBOLS[room.db.sector_type]

    def start_loc_on_grid(self):
        x = median(self.max_width)
        y = median(self.max_length)
        # x and y are floats by default, can't index lists with float types
        x, y = int(x), int(y)

        self.grid[x][y] = SYMBOLS['you']
        self.curX, self.curY = x, y

    def has_drawn(self, room):
        return True if room in self.worm_has_mapped.keys() else False

    def update_pos(self, room, exit_name):
        """Ensures the coordinates stay up to date with where the worm is at."""
        self.curX, self.curY = self.worm_has_mapped[room][0], self.worm_has_mapped[room][1]

        # Move the pointer depending on which exit was found.
        if exit_name == 'east':
            self.curY += 1
        elif exit_name == 'west':
            self.curY -= 1
        elif exit_name == 'north':
            self.curX -= 1
        elif exit_name == 'south':
            self.curX += 1

    def show_map(self):
        map_string = ''
        for row in self.grid:
            map_string += " ".join(row)
            map_string += "\n"
        return map_string
