# Perilous Wanderer

Solo sci-fi RPG prototype combining Solo Wanderer mechanics with Perilous Void procedural generation.

## Current Status

Working Python engine that implements:

- 2d20 test resolution with Advantage, Disadvantage, and critical failures (20s)
- Action Point economy (gain on double under TN, spend on rerolls/advantage/cancel peril/introduce opportunity)
- Progress tracks (10 boxes, variable marking by difficulty)
- Core moves: Progress, Travel, Scavenge, Explore, Arrive
- Full oracle tables for Complications, Perils, and Opportunities
- Simple game state for testing sessions via CLI

Run the prototype:

```bash
cd src
python game_state.py
