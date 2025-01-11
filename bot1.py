import random
from game_message import *
from typing import List, Tuple, Dict, Set
import heapq


class Bot:
    def __init__(self):
        self.last_direction = None
        self.current_path = {}
        self.safe_zones = None
        print("Initializing your super mega duper bot")
        self.player_items_locations: Set[Tuple[int, int]] = set()
        self.enemy_items_locations: Set[Tuple[int, int]] = set()

    def predict_threat_movements(self, threat, game_message: TeamGameState) -> Set[Tuple[int, int]]:
        """Predict possible future positions of a threat based on its personality and direction"""
        dangerous_positions = set()
        tx, ty = threat.position.x, threat.position.y

        # Predict next 3 moves based on personality
        if threat.personality == "AGGRESSIVE":
            # Aggressive threats move more directly
            predict_range = 4
            speed_multiplier = 1.5
        else:
            # Other threats have more variable movement
            predict_range = 3
            speed_multiplier = 1.0

        for i in range(predict_range):
            if threat.direction == "LEFT":
                dangerous_positions.add((tx - int(i * speed_multiplier), ty))
            elif threat.direction == "RIGHT":
                dangerous_positions.add((tx + int(i * speed_multiplier), ty))
            elif threat.direction == "UP":
                dangerous_positions.add((tx, ty - int(i * speed_multiplier)))
            elif threat.direction == "DOWN":
                dangerous_positions.add((tx, ty + int(i * speed_multiplier)))

            # Add adjacent positions to account for possible turns
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dangerous_positions.add((tx + dx, ty + dy))

        return dangerous_positions

    def findAllItemLocation(self, game_message: TeamGameState) -> dict:
        """Identify mineral positions on neutral territory on the map"""
        mineral_locations = {}

        for item in game_message.items:
            mineral_locations[f"x:{item.position.x}, y:{item.position.y}"] = item.type
        print(f"mineral_locations:{mineral_locations}")
        return mineral_locations

    def find_blitziums_neutral(self, game_message: TeamGameState) -> Set[Tuple[int, int]]:
        """Identify mineral positions on neutral territory on the map"""
        all_neutral_minerals = set()

        # Calculate dangerous zones from all threats
        for item in game_message.items:
            position = item.position
            if game_message.teamZoneGrid[position.x][position.y] == "" and item.type.startswith("blitzium"):
                all_neutral_minerals.add((position.x, position.y))

        return all_neutral_minerals
    def find_blitziums_hostile(self, game_message: TeamGameState) -> Set[Tuple[int, int]]:
        """Identify mineral positions on neutral territory on the map"""
        all_hostile_minerals = set()

        # Calculate dangerous zones from all threats
        for item in game_message.items:
            position = item.position
            if game_message.teamZoneGrid[position.x][position.y] != "" and game_message.teamZoneGrid[position.x][position.y] != game_message.currentTeamId and (
                    item.type.startswith("blitzium")):
                all_hostile_minerals.add((position.x, position.y))

        return all_hostile_minerals
    def find_minerals_friendly(self, game_message: TeamGameState):
        """Identify mineral positions on neutral territory on the map"""
        all_friendly_minerals = set()

        for item in game_message.items:
            position = item.position
            if game_message.teamZoneGrid[position.x][position.y] == game_message.currentTeamId:
                all_friendly_minerals.add((position.x, position.y))

        self.player_items_locations = all_friendly_minerals

    def find_minerals_enemy(self, game_message: TeamGameState):
        """Identify mineral positions on neutral territory on the map"""
        all_friendly_minerals = set()

        for item in game_message.items:
            position = item.position
            if game_message.teamZoneGrid[position.x][position.y] != game_message.currentTeamId and \
                    game_message.teamZoneGrid[position.x][position.y] != "":
                all_friendly_minerals.add((position.x, position.y))

        self.enemy_items_locations = all_friendly_minerals

    def find_radiant_hostile(self, game_message: TeamGameState) -> Set[Tuple[int, int]]:
        """Identify mineral positions on neutral territory on the map"""
        all_hostile_minerals = set()

        # Calculate dangerous zones from all threats
        for item in game_message.items:
            position = item.position
            if game_message.teamZoneGrid[position.x][position.y] == game_message.currentTeamId and (
                    item.type.startswith("radiant")):
                all_hostile_minerals.add((position.x, position.y))

        return all_hostile_minerals

    def find_player_empty_squares(self, game_message: TeamGameState) -> Set[Tuple[int, int]]:
        """Identify mineral positions on neutral territory on the map"""
        player_zones = set()
        print("looking for player squares")
        # get all friendly cordiantes
        for i in range(0, len(game_message.teamZoneGrid)):
            for j in range(0, len(game_message.teamZoneGrid[i])):
                if (game_message.teamZoneGrid[i][j] == game_message.currentTeamId and
                        game_message.map.tiles[i][j] == TileType.EMPTY and ((i, j) not in self.player_items_locations)):
                    player_zones.add((i, j))

        return player_zones

    def find_enemy_empty_squares(self, game_message: TeamGameState) -> Set[Tuple[int, int]]:
        """Identify mineral positions on neutral territory on the map"""
        enemy_zones = set()
        print("looking for enemy squares")
        # get all friendly cordiantes
        for i in range(0, len(game_message.teamZoneGrid)):
            for j in range(0, len(game_message.teamZoneGrid[i])):
                if (game_message.teamZoneGrid[i][j] != "" and game_message.teamZoneGrid[i][
                    j] != game_message.currentTeamId and
                        game_message.map.tiles[i][j] == TileType.EMPTY and ((i, j) not in self.enemy_items_locations)):
                    enemy_zones.add((i, j))

        return enemy_zones

    def find_safe_zones(self, game_message: TeamGameState) -> Set[Tuple[int, int]]:
        """Identify safe zones on the map based on threat positions and predictions"""
        safe_zones = set()
        all_dangerous_zones = set()

        # Calculate dangerous zones from all threats
        for threat in game_message.otherCharacters:
            dangerous_positions = (threat.position.x, threat.position.y)
            all_dangerous_zones.update(dangerous_positions)

        # Find safe zones (areas not in dangerous zones and not near walls)
        for x in range(game_message.map.width):
            for y in range(game_message.map.height):
                if (game_message.map.tiles[x][y] != TileType.WALL and
                        (x, y) not in all_dangerous_zones):

                    # Check if position has escape routes
                    escape_routes = 0
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < game_message.map.width and
                                0 <= ny < game_message.map.height and
                                game_message.map.tiles[nx][ny] != TileType.WALL and
                                (nx, ny) not in all_dangerous_zones):
                            escape_routes += 1

                    if escape_routes >= 2:  # Position needs at least 2 escape routes to be considered safe
                        safe_zones.add((x, y))

        return safe_zones

    def calculate_path_safety(self, path: List[Tuple[int, int]], game_message: TeamGameState) -> float:
        """Calculate safety score for a given path"""
        safety_score = 0

        for pos in path:
            x, y = pos

            # Base safety score
            position_safety = 100

            # Reduce safety for positions near threats
            for threat in game_message.otherCharacters:
                tx, ty = threat.position.x, threat.position.y
                distance = abs(tx - x) + abs(ty - y)
                position_safety -= 50 / (distance + 1)

            # Reduce safety for positions near walls
            wall_distance = min(
                x, y,
                game_message.map.width - x - 1,
                game_message.map.height - y - 1
            )
            position_safety += wall_distance * 2

            safety_score += position_safety

        return safety_score / len(path)

    def find_optimal_path(self, start: Tuple[int, int],
                          game_message: TeamGameState, target_zone: Tuple[int, int]) -> List[Tuple[int, int]]:
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        def heuristic(pos, goal):
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

        # A* pathfinding
        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == target_zone:
                break

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)

                if (0 <= next_pos[0] < game_message.map.width and
                        0 <= next_pos[1] < game_message.map.height and
                        game_message.map.tiles[next_pos[0]][next_pos[1]] != TileType.WALL):

                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + heuristic(next_pos, target_zone)
                        heapq.heappush(frontier, (priority, next_pos))
                        came_from[next_pos] = current

        # Reconstruct path
        path = []
        current = target_zone
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        print(f"path from {start} to {target_zone}  path:{path}")
        return path

    def find_optimal_path_mineral(self, start: Tuple[int, int], target_zones: Set[Tuple[int, int]],
                                  game_message: TeamGameState) -> List[Tuple[int, int]]:
        """Find the safest path to the nearest safe zone using A* algorithm"""
        if not target_zones:
            return []

        def heuristic(pos, goal):
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

        # Find nearest safe zone
        nearest_mineral = min(target_zones, key=lambda sz: heuristic(start, sz))
        print(f"nearest_mineral:{nearest_mineral}")
        return self.find_optimal_path(start, game_message, nearest_mineral)

    def find_optimal_path_team_zone(self, start: Tuple[int, int], target_zones: Set[Tuple[int, int]],
                                    game_message: TeamGameState) -> List[Tuple[int, int]]:
        """Find the safest path to the nearest safe zone using A* algorithm"""
        if not target_zones:
            return []

        # Find nearest safe zone
        sorted_coordinates = sorted(
            target_zones,
            key=lambda coord: (coord[0] - start[0]) ** 2 + (coord[1] - start[1]) ** 2
        )
        if len(sorted_coordinates) > 4:
            return self.find_optimal_path(start, game_message, sorted_coordinates[4])
        else:
            return self.find_optimal_path(start, game_message, sorted_coordinates[(len(sorted_coordinates) - 1)])

    def checkSafteyOfPath(self, current_path: List, safe_zones: List):
        for step in current_path:
            if step not in safe_zones:
                return False
        return True
    def remove_current_path(self, character:Character):
        if character.id in self.current_path:
            del self.current_path[character.id]
    def get_next_move(self, game_message: TeamGameState):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []
        for character in game_message.yourCharacters:
            print(f"character:{character.id} turn")
            current_pos = (character.position.x, character.position.y)
            neutral_minerals = self.find_blitziums_neutral(game_message)
            red_minerals = self.find_radiant_hostile(game_message)
            hostile_minerals = self.find_blitziums_hostile(game_message)
            self.find_minerals_friendly(game_message)
            self.find_minerals_enemy(game_message)
            if character.numberOfCarriedItems > 0 and (
                    (character.id not in self.current_path) or len(self.current_path[character.id]) < 2):
                print(f"dropping item")
                if character.carriedItems[0].type.startswith("blitzium") and game_message.teamZoneGrid[current_pos[0]][
                    current_pos[1]] == game_message.currentTeamId:
                    actions.append(DropAction(characterId=character.id))
                    self.remove_current_path(character)
                    self.player_items_locations.add((current_pos[0], current_pos[1]))
                    print(f"blitzium droped")
                elif character.carriedItems[0].type.startswith("radiant") and (
                        game_message.teamZoneGrid[current_pos[0]][current_pos[1]] != "" and
                        game_message.teamZoneGrid[current_pos[0]][current_pos[1]] != game_message.currentTeamId):
                    actions.append(DropAction(characterId=character.id))
                    self.remove_current_path(character)
                    self.enemy_items_locations.add((current_pos[0], current_pos[1]))
                    print(f"blitzium radiant")
            else:
                item_locations = self.findAllItemLocation(game_message)
                coordinates = f"x:{current_pos[0]}, y:{current_pos[1]}"
                print(f"possible grab")
                if coordinates in item_locations and game_message.teamZoneGrid[current_pos[0]][
                    current_pos[1]] == game_message.currentTeamId and item_locations[coordinates].startswith("radiant"):
                    actions.append(GrabAction(characterId=character.id))
                    self.remove_current_path(character)
                    print(f"radiant grabed")
                    self.player_items_locations.remove((current_pos[0], current_pos[1]))

                    enemy_zones = self.find_enemy_empty_squares(game_message)
                    print(f"enemy_zones:{enemy_zones}")
                    self.current_path[character.id] = self.find_optimal_path_team_zone(current_pos, enemy_zones,
                                                                                       game_message)
                elif coordinates in item_locations and item_locations[coordinates].startswith("blitzium") and \
game_message.teamZoneGrid[current_pos[0]][current_pos[1]] != game_message.currentTeamId:
                    actions.append(GrabAction(characterId=character.id))
                    self.remove_current_path(character)
                    print(f"blitzium grabed")

                    player_zones = self.find_player_empty_squares(game_message)
                    print(f"player_zones:{player_zones}")
                    self.current_path[character.id] = self.find_optimal_path_team_zone(current_pos, player_zones,
                                                                                       game_message)

                    if game_message.teamZoneGrid[current_pos[0]][current_pos[1]] != game_message.currentTeamId and \
                            game_message.teamZoneGrid[current_pos[0]][current_pos[1]] != "":
                        self.enemy_items_locations.remove((current_pos[0], current_pos[1]))
                else:
                    print(f"moving")
                    if character.id not in self.current_path or len(self.current_path[character.id])<2:
                        if len(neutral_minerals) > 0 or character.numberOfCarriedItems > 0 and character.carriedItems[0].type.startswith("blitzium"):
                            print("fetching blitzium")
                            if character.numberOfCarriedItems > 0 and character.carriedItems[0].type.startswith("blitzium"):
                                player_zones = self.find_player_empty_squares(game_message)
                                print(f"transporting blitzium to friendly zone")
                                self.current_path[character.id] = self.find_optimal_path_team_zone(current_pos,
                                                                                                   player_zones,
                                                                                                   game_message)
                            else:
                                self.current_path[character.id] = self.find_optimal_path_mineral(current_pos,
                                                                                                 neutral_minerals,
                                                                                                 game_message)
                        elif len(red_minerals) > 0 or character.numberOfCarriedItems > 0 and character.carriedItems[0].type.startswith("radiant"):
                            print("fetching radiant")
                            if character.numberOfCarriedItems > 0 and character.carriedItems[0].type.startswith("radiant"):
                                print(f"transporting radiant to enemy zone")
                                enemy_zones = self.find_enemy_empty_squares(game_message)
                                self.current_path[character.id] = self.find_optimal_path_team_zone(current_pos, enemy_zones,
                                                                                                   game_message)
                            else:
                                print("don't have radiant")
                                # print(f"location of radiants on player territory:{red_minerals}")
                                self.current_path[character.id] = self.find_optimal_path_mineral(current_pos, red_minerals,
                                                                                                game_message)
                        elif len(hostile_minerals) > 0 or character.numberOfCarriedItems > 0 and character.carriedItems[0].type.startswith("blitzium"):
                            print("stealing blitzium")
                            if character.numberOfCarriedItems > 0 and character.carriedItems[0].type.startswith("blitzium"):
                                player_zones = self.find_player_empty_squares(game_message)
                                print(f"transporting blitzium to friendly zone")
                                self.current_path[character.id] = self.find_optimal_path_team_zone(current_pos,
                                                                                                   player_zones,
                                                                                                   game_message)
                            else:
                                self.current_path[character.id] = self.find_optimal_path_mineral(current_pos,
                                                                                                 hostile_minerals,
                                                                                                 game_message)
                        print(f"current_path for {character.id}:{self.current_path[character.id]}")

                    if character.id not in self.current_path or len(self.current_path[character.id]) < 2:
                        # Calculate immediate safety scores for adjacent positions
                        best_score = float('-inf')
                        best_move = None
                        print(f"Evasive action!!!")
                        for direction, (dx, dy) in {
                            'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0)
                        }.items():
                            next_x, next_y = current_pos[0] + dx, current_pos[1] + dy

                            if (0 <= next_x < game_message.map.width and
                                    0 <= next_y < game_message.map.height and
                                    game_message.map.tiles[next_x][next_y] != TileType.WALL):

                                safety = self.calculate_path_safety([(next_x, next_y)], game_message)

                                # Prefer continuing in same direction if similarly safe
                                if direction == self.last_direction:
                                    safety += 10

                                if safety > best_score:
                                    best_score = safety
                                    best_move = direction

                        if best_move:
                            self.last_direction = best_move
                            print(f"sticking with last direction:{self.last_direction}")
                            if best_move == 'u':
                                actions.append(MoveUpAction(characterId=character.id))
                            elif best_move == 'd':
                                actions.append(MoveDownAction(characterId=character.id))
                            elif best_move == 'l':
                                actions.append(MoveLeftAction(characterId=character.id))
                            elif best_move == 'r':
                                actions.append(MoveRightAction(characterId=character.id))
                    else:
                        print(f"Sticking on path")
                        # Follow the optimal path
                        next_pos = self.current_path[character.id][1]
                        dx = next_pos[0] - current_pos[0]
                        dy = next_pos[1] - current_pos[1]
                        del self.current_path[character.id][0]
                        if dx == 1:
                            self.last_direction = 'r'
                            actions.append(MoveRightAction(characterId=character.id))
                        elif dx == -1:
                            self.last_direction = 'l'
                            actions.append(MoveLeftAction(characterId=character.id))
                        elif dy == 1:
                            self.last_direction = 'd'
                            actions.append(MoveDownAction(characterId=character.id))
                        elif dy == -1:
                            self.last_direction = 'u'
                            actions.append(MoveUpAction(characterId=character.id))

        # You can clearly do better than the random actions above! Have fun!
        return actions
