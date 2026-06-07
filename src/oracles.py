"""Oracle tables from Solo Wanderer for Perilous Void integration."""

COMPLICATIONS = [
    (2, "Roll again and make it a worse effect. (max once)"),
    (9, "Someone you know loses trust in you or acts against you."),
    (19, "Someone you know is exposed to danger, close or far."),
    (27, "A threat escalates or becomes an immediate danger."),
    (42, "Something of value is lost, broken, or no longer functions."),
    (55, "A new danger or foe is revealed."),
    (68, "A delay or disadvantage."),
    (76, "A temporary solution becomes a permanent problem."),
    (87, "You run out of something essential."),
    (94, "Something hidden becomes exposed."),
    (100, "Roll twice. (max once)"),
]

PERILS = [
    (4, "You encounter a dangerous animal or pack of animals"),
    (6, "You fall into a hidden sinkhole"),
    (10, "A sudden radstorm sweeps through the area"),
    (13, "An explosive detonates near your path"),
    (18, "A hostile patrol is in the area"),
    (23, "One of your essential piece of gear breaks unexpectedly"),
    (25, "You encounter a dangerous mutant"),
    (29, "A hostile robot awakens nearby"),
    (35, "Some of your food/water spoils"),
    (38, "You trigger a forgotten alarm system"),
    (44, "You are stalked by a silent figure"),
    (50, "A horde of small mutants blocks your path forward"),
    (53, "You are caught in the crossfire between two factions"),
    (60, "A burst of toxic fumes surrounds you"),
    (62, "Disease or sickness takes hold of you"),
    (66, "You are caught in a trap or ambush"),
    (67, "You find your name scratched onto a surface"),
    (69, "You are caught in quicksand, a pitfall, or mire"),
    (74, "An old injury flares up violently"),
    (76, "A sandstorm whips up, making navigation near impossible"),
    (85, "You cross into a highly radioactive zone"),
    (88, "You are overcome with a sudden flash of heat and tiredness"),
    (91, "The ground beneath you quakes and collapses"),
    (95, "You are forced to travel another way due to a collapse or flood"),
    (100, "You encounter a fellow wanderer in need of help"),
]

OPPORTUNITIES = [
    (3, "A helpful traveler crosses your path"),
    (7, "You discover a hidden stash of supplies"),
    (11, "A rare pre-war book improves one of your skills"),
    (13, "A traveling merchant offers you a deal"),
    (18, "You find a stash of Nuka-Cola under light rubble"),
    (20, "You find an old bunker that is still powered"),
    (26, "A clue offers you guidance towards your current mission"),
    (29, "You meet someone who owes you a favor"),
    (35, "A damaged robot becomes loyal to you"),
    (39, "You find an intact frame of power armor"),
    (41, "A stranger gives you clean water and food"),
    (47, "You encounter a friendly group of locals or faction members"),
    (53, "You find a useful item that you were looking for"),
    (56, "Your recover faster than expected"),
    (60, "You find a large stash of Caps"),
    (64, "The weather is perfect for traveling"),
    (68, "A vantage point reveals a key landmark for you mission"),
    (73, "An old radio plays a hopeful message inspiring you"),
    (77, "You learn of stash location filled with useful items"),
    (79, "Someone offers you permanent shelter for when you need it"),
    (82, "A mysterious stranger helps you from afar"),
    (90, "You encounter a potential ally in need of help"),
    (94, "A lurking foe reveals themselves"),
    (98, "You feel extra lucky and automatically critically hit on your next attack"),
    (100, "You learn the location of a secret Vault"),
]

def roll_oracle(table, roll=None):
    """Roll or take provided roll (1-100) and return the matching entry string."""
    if roll is None:
        import random
        roll = random.randint(1, 100)
    for threshold, text in table:
        if roll <= threshold:
            return text
    return table[-1][1]

def get_complication(roll=None):
    return roll_oracle(COMPLICATIONS, roll)

def get_peril(roll=None):
    return roll_oracle(PERILS, roll)

def get_opportunity(roll=None):
    return roll_oracle(OPPORTUNITIES, roll)
