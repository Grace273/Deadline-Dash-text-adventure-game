
"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str],
                 unlock_location_points: int) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id, unlock_location_points)

        initial_location = self._game.get_location()
        initial_location_id_desc = initial_location.descriptions[1]
        first_event = Event(id_num=initial_location_id,
                            description=initial_location_id_desc)

        self._events.add_event(event=first_event, command=None)

        self.generate_events(commands=commands, current_location=initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            next_location_id = current_location.available_commands[command]
            next_location_id_desc = self._game.get_location(next_location_id).descriptions[1]

            next_event = Event(id_num=next_location_id,
                               description=next_location_id_desc)
            self._events.add_event(event=next_event, command=command)

            current_location = self._game.get_location(next_location_id)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        print("==========BEGIN SIMULATION==========")
        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next
        print("==========END OF SIMULATION==========")


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    # # A list of all user inputs needed to walk through our game to win it. Follow the input in adventure.py to test.
    win_full_demo = ["go east", "go upstairs", "pick up: key", "go downstairs", "go east", "go east",
                       "talk to sadia", "go north", "go to dorm", "get usb drive", "2", "pick up: usb drive",
                       "go downstairs", "go south", "go south", "pick up: mug", "go west", "go west",
                       "go upstairs", "get laptop charger", "1", "1", "1", "pick up: laptop charger",
                       "go downstairs", "go east", "go south", "pick up: presto card", "get on the streetcar",
                       "buy potion", "go back to campus", "go north", "go west", "go north", "go west",
                       "put down items to submit work"]

    expected_log_win_full = [1, 2, 20, 20, 2, 4, 8, 8, 7, 70, 70, 70, 7, 8, 9, 9, 5, 3, 30, 30, 30, 3, 5, 6, 6, 11,
                             11, 6, 5, 3, 2, 1]

    # A simplified walkthrough between locations of a winning routine
    win_demo = ["go east", "go upstairs", "go downstairs", "go east", "go east", "talk to sadia", "go north",
                "go to dorm", "go downstairs", "go south", "go south", "go west", "go west", "go east", "go south",
                "go north", "go west", "go north", "go west", "put down items to submit work"]

    expected_log_win = [1, 2, 20, 2, 4, 8, 8, 7, 70, 7, 8, 9, 5, 3, 5, 6, 5, 3, 2, 1, 1]

    win_sim = AdventureGameSimulation('game_data.json', 1, win_demo, 10)
    win_sim.run()

    assert expected_log_win == win_sim.get_id_log()

    # A list of all the commands needed to walk through our game to reach a 'game over' state
    lose_demo = ["go east", "go east", "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east", "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east", "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east", "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east", "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east", "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east"]

    expected_log_lose = [1, 2, 4, 8, 7, 8, 4, 2,
                         1, 2, 4, 8, 7, 8, 4, 2,
                         1, 2, 4, 8, 7, 8, 4, 2,
                         1, 2, 4, 8, 7, 8, 4, 2,
                         1, 2, 4, 8, 7, 8, 4, 2,
                         1, 2, 4, 8, 7, 8, 4, 2,
                         1, 2, 4]

    lose_sim = AdventureGameSimulation('game_data.json', 1, lose_demo, 10)
    lose_sim.run()

    assert expected_log_lose == lose_sim.get_id_log()

    # inventory demo, including pick up and drop. Follow to input to test out inventory function
    inventory_demo = ["go east", "go upstairs", "pick up: key", "drop: key"]

    expected_log_inventory = [1, 2, 20, 20, 20]

    # demo for score
    score_demo = ["go east", "go east", "go east", "go south", "go north", "go under the bridge",
                  "ford, ford, teleport"]

    expected_log_score = [1, 2, 4, 8, 9, 8, 10, 10]  # expected score: 80

    score_sim = AdventureGameSimulation('game_data.json', 1, score_demo, 10)
    score_sim.run()

    assert expected_log_score == score_sim.get_id_log()

    # demo of special event - teleport
    teleportation_demo = ["go east", "go east", "go east", "go under the bridge", "ford, ford, teleport"]

    expected_log_teleportation = [1, 2, 4, 8, 10, 10]  # next user input determines which place to teleport

    teleportation_sim = AdventureGameSimulation('game_data.json',
                                                1, teleportation_demo, 10)
    teleportation_sim.run()

    assert expected_log_teleportation == teleportation_sim.get_id_log()

    # demo of minigame puzzle. Input the following commands in order in adventure.py to test out minigame
    minigame_demo = ["go east", "go upstairs", "go upstairs", "pick up: key", "go downstairs", "go east", "go east",
                     "go north", "go to dorm", "get usb drive", "2", "pick up: usb drive"]

    # demo of mug puzzle. Input the following commands in order in adventure.py to test out.
    mug_puzzle_demo = ["go east", "go east", "go east", "go south", "pick up: mug", "go west", "go south",
                        "pick up presto card", "get on street car", "pick up: potion"]

    # demo of laptop charger puzzle. Input the following commands in order in adventure.py to test out.
    lc_puzzle_demo = ["go east", "go east", "go east", "talk to sadia", "go under the bridge", "ford, ford, teleport",
                      "3", "go upstairs", "get laptop charger", "1", "1", "1", "pick up: laptop charger"]

    #demo of undoing pick/drop. Input the following commands in order in adventure.py to test out.
    undo_demo = ["go east", "go upstairs", "pick up: key", "undo", "pick up: key", "drop: key", "undo", "inventory"]

    #demo of hotdog item. Input the following commands in order in adventure.py to test out.
    hotdog_demo = ["go east", "go east", "buy hotdog"]
