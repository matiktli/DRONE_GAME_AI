# Reward Generator

## Space description

Map of size: `{game.map.size_x} x {game.map.size_y}`, by default: `50 x 50`.\
Game turns number max: `{game.max_turns}`, by default: `200`.\
Players no: `{game.players_no}`, by default: `4`.\
Players actions: `{players[i].allowed_actions}`, by default: `[MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, STAY, DUPLICATE]`.\
Player drones noL `{players[i].drone_no}`, by default: `20`.\

## Reward simple calculation function

Abstract of how this policy is calculating reward from current grame frame:

```
def reward(your_drones_no, enemy_drones_no, your_cells_no, enemy_cells_no, grid_size, turn_no):
    return your_drones_no + your_cells_no + turn_no
```
