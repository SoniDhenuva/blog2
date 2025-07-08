class Fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.intensity = 1

    def grow(self, amount=1):
        self.intensity += amount
        print("🔥 Fire grew!")

    def shrink(self, amount=1):
        self.intensity = max(0, self.intensity - amount)
        print("💧 Fire shrank!")

    def move(self, direction, env):
        if direction == "west":
            self.x = max(0, self.x - 1)
        elif direction == "east":
            self.x = min(env.width - 1, self.x + 1)
        elif direction == "north":
            self.y = max(0, self.y - 1)
        elif direction == "south":
            self.y = min(env.height - 1, self.y + 1)
        print(f"🔥 Fire moved {direction}!")

    def location(self):
        return self.x, self.y


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.fire = Fire(width // 2, height // 2)
        self.ponds = []
        self.people = []

    def update_grid(self):
        self.grid = [['.' for _ in range(self.width)] for _ in range(self.height)]

        # Place fire
        fx, fy = self.fire.location()
        radius = self.fire.intensity
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                x = fx + dx
                y = fy + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y][x] = 'F'

        # Place ponds
        for (x, y) in self.ponds:
            self.grid[y][x] = 'W'

        # Place people (last, so they show up on top)
        for (x, y) in self.people:
            self.grid[y][x] = 'P'

    def display(self):
        self.update_grid()
        print("\n--- Environment ---")
        for row in self.grid:
            print(" ".join(row))
        print(f"\n🔥 Fire Intensity: {self.fire.intensity}")
        print(f"💧 Ponds at: {self.ponds}")
        print(f"🧍 People at: {self.people}")

    def place_pond(self, direction):
        fx, fy = self.fire.location()
        if direction == "west":
            new_x = max(0, fx - 1)
            new_y = fy
        elif direction == "east":
            new_x = min(self.width - 1, fx + 1)
            new_y = fy
        elif direction == "north":
            new_x = fx
            new_y = max(0, fy - 1)
        elif direction == "south":
            new_x = fx
            new_y = min(self.height - 1, fy + 1)
        else:
            print("❌ Invalid direction.")
            return

        radius = self.fire.intensity

        distance_x = abs(new_x - fx)
        distance_y = abs(new_y - fy)

        # Allow ponds on fire border, disallow inside
        if distance_x < radius and distance_y < radius:
            print("🚫 Can't place pond inside fire!")
            return

        if (new_x, new_y) not in self.ponds:
            self.ponds.append((new_x, new_y))
            print(f"🟦 Pond placed at ({new_x}, {new_y})")
        else:
            print("ℹ️ Pond already exists at that location.")


    def place_people(self, direction="all"):
        fx, fy = self.fire.location()
        radius = self.fire.intensity
        directions = {
            "north": (0, -1),
            "south": (0, 1),
            "west": (-1, 0),
            "east": (1, 0)
        }

        def is_on_fire(x, y):
            return abs(x - fx) <= radius and abs(y - fy) <= radius

        new_people = []

        # Place people just outside the fire radius (distance radius + 1)
        if direction == "all":
            for dx, dy in directions.values():
                x = fx + dx * (radius + 1)
                y = fy + dy * (radius + 1)
                if 0 <= x < self.width and 0 <= y < self.height:
                    if not is_on_fire(x, y):
                        new_people.append((x, y))
        elif direction in directions:
            dx, dy = directions[direction]
            x = fx + dx * (radius + 1)
            y = fy + dy * (radius + 1)
            if 0 <= x < self.width and 0 <= y < self.height:
                if not is_on_fire(x, y):
                    new_people.append((x, y))

        for p in new_people:
            if p not in self.people:
                self.people.append(p)

        print(f"🧍 People placed {direction} of the fire, outside fire area.")
        print("People coordinates:", self.people)


def parse_command(cmd, env):
    cmd = cmd.lower()

    # Fire growth
    if "fire" in cmd and ("increase" in cmd or "increasing" in cmd):
        env.fire.grow()
        return

    # Fire shrinking
    if "fire" in cmd and ("decrease" in cmd or "decreasing" in cmd):
        env.fire.shrink()
        return

    # Fire movement
    for direction in ["north", "south", "east", "west"]:
        if f"fire is moving {direction}" in cmd:
            env.fire.move(direction, env)
            return

    # People placement
    if "people near fire" in cmd:
        for direction in ["north", "south", "east", "west"]:
            if direction in cmd:
                env.place_people(direction)
                return
        env.place_people("all")
        return

    # Pond / water placement
    if "water is" in cmd or "pond is" in cmd:
        for direction in ["north", "south", "east", "west"]:
            if direction in cmd:
                env.place_pond(direction)
                return
        print("❌ Direction not recognized in water command.")
        return

    print("❓ Command not recognized.")


def run_simulation():
    env = Environment(width=30, height=15)  # Bigger grid
    env.display()

    while True:
        command = input("\n🗣️  Enter a command (type 'quit' to exit): ")
        if command.lower() in ["quit", "exit"]:
            print("👋 Exiting simulation.")
            break
        parse_command(command, env)
        env.display()


if __name__ == "__main__":
    run_simulation()
