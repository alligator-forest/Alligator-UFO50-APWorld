from typing import NamedTuple, TYPE_CHECKING

from BaseClasses import Region

from .locations import create_locations
from .rules import create_rules

if TYPE_CHECKING:
    from ... import UFO50World


# not sure if we really need this yet, but making it in case we need it later since it's easy to remove
class RegionInfo(NamedTuple):
    rooms: list[str] = []  # rooms this region contains, for the purpose of the garden prize access rule


regions: list[str] = [
    "Menu",  # the non-existent start menu, every game needs a region named "Game Name - Menu"
    "Campaign Mode", # includes all campaign levels
    "Ranked Mode", # the ranked mode
    "Survival Mode", # the survival mode

    "Campaign + Ranked", # used for the Cherry Condition

    # Campaign Mode Regions
    # Each of these regions features a unqiue set of units: 
    "Levels 1, 21", # Grunt only
    "Levels 2, 3", # Archer + Grunt
    "Levels 4", # Shield + Grunt
    "Levels 5, 6", # Cavalry + Archer + Grunt
    "Levels 7, 8", # Shield + Cavalry + Archer + Grunt
    "Levels 9", # Spear + Shield + Grunt
    "Levels 10, 15", # Cavalry + Archer + Shield + Spear + Grunt
    "Levels 11", # Assassin + Archer + Spear + Cavalry + Grunt
    "Levels 12", # Spear + Cavalry
    "Levels 13, 14", # All units except Sapper + Hero
    "Levels 16", # Sapper + Shield + Spear + Cavalry
    "Levels 17", # Assassin + Cavalry + Sapper + Grunt
    "Levels 18, 19, 23", # All units except Hero
    "Levels 20", # Shield + Assassin + Archer + Hero
    "Levels 22", # Sapper + Archer
    "Levels 24", # All units including Hero

    # Ranked Mode Regions
    "Ranked Early", # Ranks 0 - 50
    "Ranked Mid", # Ranks 60 - 100
    "Ranked Late", # Ranks 110 - 200

    # Survival Mode Regions
    "Survival Early",
    "Survival Mid",
    "Survival Late",

]


# this function is required, and its only argument can be the world class
# it must return the regions that it created
# it is recommended that you prepend each region name with the game it is from to avoid overlap
def create_regions_and_rules(world: "UFO50World") -> dict[str, Region]:
    attactics_regions: dict[str, Region] = {}
    for region_name in regions:
        attactics_regions[region_name] = Region(f"Attactics - {region_name}", world.player, world.multiworld)

    create_locations(world, attactics_regions)
    create_rules(world, attactics_regions)

    return attactics_regions
