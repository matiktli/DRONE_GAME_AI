# Game AI
Drone Wars simulation engine build in python, inspired by: [Halite.io - 1st edition](https://2016.halite.io/index.html)

## Game Rules
Each drone has: energy in defined range, if drone loses all energy it dies.

Game is played by managing player's drones. When turn starts each drone can decide if to:

* **stay still** ( that will recharge it's energy by static size)
* **move by direction given** ( that will consumes it's energy base on distance of move taken )
* **duplicate** ( that will consume half of energy and spawn 2nd drone that would have the same energy)

If two drones of different players decided to move to the same location on the grid then each drone lose energy equals to oponents drone energy.

### Initialization
* Each player starts with `{initial_drone_count}` drones.
    * Each drone starts with `{initial_drones_energy}` energy.
* Map is a 2D grid of size `{initial_map_size}`.
* Player's drones are placed around defined point `{initial_start_point}`, within square of size `{initial_start_potint_size}`.

### Each Turn 
Each drone can decide to make a move from: UP, DOWN, LEFT, RIGHT or to use special action: STAY, DUPLICATE.

#### MOVE 
Moving consumes energy proportional to distance and current energy of drone. `enegry_loss = drone.energy * loss_factor`, where `loss_factor` is in range of `[0.1, 0.5]`. 

If drone decided to move by more than one step then energy consumption is...

#### STAY
Staying in place can benefit in recharging drones energy. `energy_gain = 10`

#### DUPLICATE
By duplicating drone firstly loses half of it's energy and then spawn 2nd drone with the same energy on top of him at the same location

    TW