import time
import os
from dataclasses import dataclass
from typing import Set, FrozenSet, List, Optional
from collections import deque

State = FrozenSet[str]

@dataclass(frozen=True)
class Action:
    name: str
    pre: Set[str]
    add: Set[str]
    delete: Set[str]

    def applicable(self, s: State) -> bool:
        return self.pre.issubset(s)

    def apply(self, s: State) -> State:
        if not self.applicable(s):
            raise ValueError(f"Acción {self.name} no aplicable.")
        new = set(s)
        for p in self.delete:
            new.discard(p)
        for p in self.add:
            new.add(p)
        return frozenset(new)

def goal_satisfied(s: State, goal: Set[str]) -> bool:
    return goal.issubset(s)

def bfs_plan(initial: State, goal: Set[str], actions: List[Action]) -> Optional[List[Action]]:
    frontier = deque([(initial, [])])
    visited = {initial}
    while frontier:
        state, plan = frontier.popleft()
        if goal_satisfied(state, goal):
            return plan
        for a in actions:
            if a.applicable(state):
                succ = a.apply(state)
                if succ not in visited:
                    visited.add(succ)
                    frontier.append((succ, plan + [a]))
    return None

# ----- Configuración del nivel -----
actions = [
    Action("MoveToMushroom", pre={"pos_0"}, add={"pos_2"}, delete={"pos_0"}),
    Action("TakeMushroom", pre={"pos_2"}, add={"big_mario"}, delete=set()),
    Action("MoveToKey", pre={"pos_2"}, add={"pos_4"}, delete={"pos_2"}),
    Action("GetKey", pre={"pos_4", "big_mario"}, add={"has_key"}, delete=set()),
    Action("MoveToDoor", pre={"pos_4"}, add={"pos_6"}, delete={"pos_4"}),
    Action("OpenDoor", pre={"pos_6", "has_key"}, add={"door_open"}, delete=set()),
    Action("EnterDoor", pre={"pos_6", "door_open"}, add={"level_completed"}, delete=set()),
]

initial = frozenset({"pos_0"})  # Mario empieza en posición 0
goal = {"level_completed"}

# Generar plan determinista
plan = bfs_plan(initial, goal, actions)

# ----- Visualización simple tipo grid -----
def print_world(mario_pos, has_mushroom, has_key, door_open):
    grid = ["M", " ", "🍄", " ", "🔑", " ", "🚪"]
    # posiciones: 0,1,2,3,4,5,6
    display = []
    for i, cell in enumerate(grid):
        if i == mario_pos:
            display.append("M")
        else:
            if cell == "🍄" and not has_mushroom:
                display.append("🍄")
            elif cell == "🔑" and not has_key:
                display.append("🔑")
            elif cell == "🚪" and not door_open:
                display.append("🚪")
            elif cell == "🚪" and door_open:
                display.append("🚪✅")
            else:
                display.append(" ")
    print(" | ".join(display))

# ----- Simulación paso a paso -----
if plan is None:
    print("No se encontró un plan para completar el nivel.")
else:
    print("Plan determinista encontrado:")
    for i, a in enumerate(plan, 1):
        print(f"{i}. {a.name}")

    print("\nSimulación gráfica:")
    mario_pos = 0
    has_mushroom = False
    has_key = False
    door_open = False

    print_world(mario_pos, has_mushroom, has_key, door_open)
    time.sleep(1)

    for action in plan:
        if action.name == "MoveToMushroom":
            mario_pos = 2
        elif action.name == "TakeMushroom":
            has_mushroom = True
        elif action.name == "MoveToKey":
            mario_pos = 4
        elif action.name == "GetKey":
            has_key = True
        elif action.name == "MoveToDoor":
            mario_pos = 6
        elif action.name == "OpenDoor":
            door_open = True
        elif action.name == "EnterDoor":
            print("🎉 ¡Nivel completado B)! 🎉")
            break

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Acción: {action.name}")
        print_world(mario_pos, has_mushroom, has_key, door_open)
        time.sleep(1)
