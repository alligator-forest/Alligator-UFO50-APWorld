from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import ItemClassification as IC, Item

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class ItemInfo(NamedTuple):
    id_offset: int
    classification: IC
    quantity: int
    group : str

# 2 Progressive Units: 1st instance gives the ability to spawn that unit, the 2nd gives the ability to promote that unit
item_table: dict[str, ItemInfo] = {
    "Progressive Grunt": ItemInfo(0, IC.useful, 1, "Units"),
    "Progressive Archer": ItemInfo(1, IC.progression, 2, "Units"),
    "Progressive Shieldman": ItemInfo(2, IC.progression, 2, "Units"),
    "Progressive Cavalry": ItemInfo(3, IC.progression, 2, "Units"),
    "Progressive Spearman": ItemInfo(4, IC.progression, 2, "Units"),
    "Progressive Assassin": ItemInfo(5, IC.useful, 2, "Units"),
    "Progressive Sapper": ItemInfo(6, IC.useful, 2, "Units"),
    "Hero Spawning": ItemInfo(7, IC.useful, 1, "Units"),
    "Ranked Mode Access": ItemInfo(8, IC.progression, 1, "Modes"),
    "Survival Mode Access": ItemInfo(9, IC.useful, 1, "Modes"),
    "Extra Flag": ItemInfo(10, IC.useful, 5, "Bonus"),
    "+10% Extra Units": ItemInfo(11, IC.useful, 10, "Bonus"),
    "+5 Ranked Win Bonus": ItemInfo(12, IC.filler, 0, "Bonus"),
}


# this is for filling out item_name_to_id, it should be static regardless of yaml options
def get_items() -> dict[str, int]:
    return {f"Attactics - {name}": data.id_offset + get_game_base_id("Attactics") for name, data in item_table.items()}


# this should return the item groups for this game, independent of yaml options
# you should include a group that contains all items for this game that is called the same thing as the game
def get_item_groups() -> dict[str, set[str]]:
    item_groups: dict[str, set[str]] = {"Attactics": {
        f"Attactics - {item_name}" for item_name in item_table.keys()}}
    return item_groups


# for when the world needs to create an item at random (like with random filler items)
# the first argument must be the item name. It must be able to handle the world giving it an actual item name
# the second argument must be the world class
# the third argument is an item classification, `item_class: ItemClassification = None`
# you must put the third argument in, but you are not required to use it
def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Attactics")
    if item_name.startswith("Attactics - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Attactics - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


# for when the world is getting the items to place into the multiworld's item pool
# you must pass in the world class as the argument
def create_items(world: "UFO50World") -> list[Item]:
    items_to_create: dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    attactics_items: list[Item] = []
    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            attactics_items.append(create_item(item_name, world))
    return attactics_items


def get_filler_item_name(world: "UFO50World") -> str:
    return "Attactics - +10 Ranked Win Bonus"
