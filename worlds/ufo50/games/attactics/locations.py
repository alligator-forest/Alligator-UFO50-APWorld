from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Location, Item, ItemClassification
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class LocationInfo(NamedTuple):
    id_offset: int
    region_name: str


location_table: dict[str, LocationInfo] = {

    # All Campaign Levels
    "First Encounter": LocationInfo(1, "Levels 1, 21"),
    "Arrow Defense": LocationInfo(2, "Levels 2, 3"),
    "Attrition": LocationInfo(3, "Levels 2, 3"),
    "Under Fire": LocationInfo(4, "Levels 4"),
    "Here They Come": LocationInfo(5, "Levels 5, 6"),
    "Escalation": LocationInfo(6, "Levels 5, 6"),
    "Protect Yourself": LocationInfo(7, "Levels 7, 8"),
    "What's the Point?": LocationInfo(8, "Levels 7, 8"),
    "Porcupine Style": LocationInfo(9, "Levels 9"),
    "So It Goes": LocationInfo(10, "Levels 10, 15"),
    "Knives Out": LocationInfo(11, "Levels 11"),
    "Poke and Dagger": LocationInfo(12, "Levels 12"),
    "Stem The Tide": LocationInfo(13, "Levels 13, 14"),
    "Ready Or Not": LocationInfo(14, "Levels 13, 14"),
    "Stand Back": LocationInfo(15, "Levels 10, 15"),
    "Blast Damage": LocationInfo(16, "Levels 16"),
    "Guerrilla Warfare": LocationInfo(17, "Levels 17"),
    "Rally The Troops": LocationInfo(18, "Levels 18, 19, 23"),
    "Traffic Jam": LocationInfo(19, "Levels 18, 19, 23"),
    "Acts of Heroism": LocationInfo(20, "Levels 20"),
    "Back To Basics": LocationInfo(21, "Levels 1, 21"),
    "Barreling Ahead": LocationInfo(22, "Levels 22"),
    "War Is Bad": LocationInfo(23, "Levels 18, 19, 23"),
    "The Final Battle": LocationInfo(24, "Levels 24"),

    # All Ranked Mode Ranks
    "Private Rank" : LocationInfo(30, "Ranked Early"),
    "First Class Rank" : LocationInfo(31, "Ranked Early"),
    "Corporal Rank" : LocationInfo(32, "Ranked Early"),
    "Sergeant Rank" : LocationInfo(33, "Ranked Early"),
    "Lieutenant Rank" : LocationInfo(34, "Ranked Early"),
    "Captain Rank" : LocationInfo(35, "Ranked Mid"),
    "Major Rank" : LocationInfo(36, "Ranked Mid"),
    "Colonel Rank" : LocationInfo(37, "Ranked Mid"),
    "General Rank" : LocationInfo(38, "Ranked Mid"),
    "Lord Rank" : LocationInfo(39, "Ranked Mid"),
    "Baron Rank" : LocationInfo(40, "Ranked Late"),
    "Viscount Rank" : LocationInfo(41, "Ranked Late"),
    "Earl Rank" : LocationInfo(42, "Ranked Late"),
    "Marques Rank" : LocationInfo(43, "Ranked Late"),
    "Duke Rank" : LocationInfo(44, "Ranked Late"),
    "Prince Rank" : LocationInfo(45, "Ranked Late"),
    "Monarch Rank" : LocationInfo(46, "Ranked Late"),
    "Emperor Rank" : LocationInfo(47, "Ranked Late"),
    "Demigod Rank" : LocationInfo(48, "Ranked Late"),
    "God Rank" : LocationInfo(49, "Ranked Late"),

    # All Survival Mode Ranks
    "Survival 25 Turns" : LocationInfo(50, "Survival Early"),
    "Survival 50 Turns" : LocationInfo(51, "Survival Early"),
    "Survival 75 Turns" : LocationInfo(52, "Survival Mid"),
    "Survival 100 Turns" : LocationInfo(53, "Survival Mid"),
    "Survival 125 Turns" : LocationInfo(54, "Survival Late"),
    "Survival 150 Turns" : LocationInfo(55, "Survival Late"),

    # For the sake of simplicity we are assuming beating a level without having all the required units is 'out of logic' since it is harder than the vanilla game.
    "Garden": LocationInfo(997, "Levels 10, 15"), # You can beat 12 levels with just Grunt, Archer, Shield, Spear, and Cavalry. This is the lowest amount of units you can beat 12 levels with assuming the rule above.
    "Gold": LocationInfo(998, "Levels 24"), # If Level 24 is in-logic, then the rest must also be since Level 24 includes every unit in the game.
    "Cherry": LocationInfo(999, "Levels 24")
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> dict[str, int]:
    return {f"Attactics - {name}": data.id_offset + get_game_base_id("Attactics") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> dict[str, set[str]]:
    location_groups: dict[str, set[str]] = {"Attactics": {f"Attactics - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Attactics" not in world.options.cherry_allowed_games:
            break

        if loc_name in ["Gold", "Cherry"] and "Attactics" in world.goal_games:
            if (loc_name == "Gold" and "Attactics" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Attactics - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Attactics", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Attactics", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break

        loc = Location(world.player, f"Attactics - {loc_name}", get_game_base_id("Attactics") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
