from typing import TYPE_CHECKING

from BaseClasses import Region, CollectionState
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from ... import UFO50World

def create_rules(world: "UFO50World", regions: dict[str, Region]) -> None:

    # Note: x1 Grunt is given to you by default. 1 Progressive Grunt is in the world as an upgrade for enabling promotion
    archer = "Attactics - Progressive Archer"
    shield = "Attactics - Progressive Shieldman"
    cavalry = "Attactics - Progressive Cavalry"
    spear = "Attactics - Progressive Spearman"
    assassin = "Attactics - Progressive Assassin"
    sapper = "Attactics - Progressive Sapper"
    hero = "Attactics - Hero Spawning"

    ranked = "Attactics - Ranked Mode"
    survival = "Attactics - Survival Mode"

    player = world.player

    # Grunt is assumed by default because you start with it
    level_units = [
        [],
        [archer],
        [archer],
        [shield],
        [archer, cavalry], 
        [archer, cavalry], 
        [archer, cavalry, shield],
        [archer, cavalry, shield],
        [shield, spear],
        [archer, cavalry, shield, spear],
        [archer, assassin, cavalry, spear],
        [cavalry, spear],
        [archer, assassin, cavalry, shield, spear],
        [archer, assassin, cavalry, shield, spear],
        [archer, cavalry, shield, spear],
        [cavalry, sapper, shield, spear],
        [assassin, cavalry, sapper],
        [archer, assassin, cavalry, sapper, shield, spear],
        [archer, assassin, cavalry, sapper, shield, spear],
        [archer, assassin, hero, shield],
        [],
        [archer, sapper],
        [archer, assassin, cavalry, sapper, shield, spear],
        [archer, assassin, cavalry, hero, sapper, shield, spear],
        ]



    # Different screens
    regions["Menu"].connect(regions["Campaign Mode"])
    regions["Menu"].connect(regions["Ranked Mode"], rule=lambda state: state.has(ranked, player))
    regions["Menu"].connect(regions["Survival Mode"], rule=lambda state: state.has(survival, player))

    # Different levels of the Campaign Mode
    regions["Campaign Mode"].connect(regions["Levels 1, 21"])
    regions["Campaign Mode"].connect(regions["Levels 2, 3"], rule=lambda state: state.has_all(level_units[1], player))
    regions["Campaign Mode"].connect(regions["Levels 4"], rule=lambda state: state.has_all(level_units[3], player))
    regions["Campaign Mode"].connect(regions["Levels 5, 6"], rule=lambda state: state.has_all(level_units[4], player))
    regions["Campaign Mode"].connect(regions["Levels 7, 8"], rule=lambda state: state.has_all(level_units[6], player))
    regions["Campaign Mode"].connect(regions["Levels 9"], rule=lambda state: state.has_all(level_units[8], player))
    regions["Campaign Mode"].connect(regions["Levels 10, 15"], rule=lambda state: state.has_all(level_units[9], player))
    regions["Campaign Mode"].connect(regions["Levels 11"], rule=lambda state: state.has_all(level_units[10], player))
    regions["Campaign Mode"].connect(regions["Levels 12"], rule=lambda state: state.has_all(level_units[11], player))
    regions["Campaign Mode"].connect(regions["Levels 13, 14"], rule=lambda state: state.has_all(level_units[12], player))
    regions["Campaign Mode"].connect(regions["Levels 16"], rule=lambda state: state.has_all(level_units[15], player))
    regions["Campaign Mode"].connect(regions["Levels 17"], rule=lambda state: state.has_all(level_units[16], player))
    regions["Campaign Mode"].connect(regions["Levels 18, 19, 23"], rule=lambda state: state.has_all(level_units[17], player))
    regions["Campaign Mode"].connect(regions["Levels 20"], rule=lambda state: state.has_all(level_units[19], player))
    regions["Campaign Mode"].connect(regions["Levels 22"], rule=lambda state: state.has_all(level_units[2], player))
    regions["Campaign Mode"].connect(regions["Levels 24"], rule=lambda state: state.has_all(level_units[23], player))

    regions["Levels 24"].connect(regions["Campaign + Ranked"], rule=lambda state: state.can_reach_region("Attactics - Ranked Mid", player))


    regions["Ranked Mode"].connect(regions["Ranked Early"], rule=lambda state: state.has_group("Attactics - Units", player, 4))
    regions["Ranked Mode"].connect(regions["Ranked Mid"], rule=lambda state: state.has_group("Attactics - Units", player, 7))
    regions["Ranked Mode"].connect(regions["Ranked Late"], rule=lambda state: state.has_group("Attactics - Units", player, 12))

    regions["Survival Mode"].connect(regions["Survival Early"], rule=lambda state:  state.has_group("Attactics - Units", player, 4))
    regions["Survival Mode"].connect(regions["Survival Mid"], rule=lambda state: state.has_group("Attactics - Units", player, 7))
    regions["Survival Mode"].connect(regions["Survival Late"], rule=lambda state: state.has_group("Attactics - Units", player, 12))