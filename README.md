# Game AI

Drone Wars simulation engine build in python, inspired by: [Halite.io - 1st edition](https://2016.halite.io/index.html).
Purpose of it is to simulate easy to control environment for training deep learning models on making decisions based on mutliple parameter input.
Possible transfer learning environment.

## Game Rules

Each drone has: energy in defined range, if drone loses all energy it dies.

Game is played by managing player's drones. When turn starts each drone can decide if to:

- **stay still** ( that will recharge it's energy by static size)
- **move by direction given** ( that will consumes it's energy base on distance of move taken )
- **duplicate** ( that will consume half of energy and spawn 2nd drone that would have the same energy)

If two drones of different players decided to move to the same location on the grid then each drone lose energy equals to oponents drone energy.

### Initialization

- Each player starts with `{player_initial_drones_count}` drones.
  - Each drone starts with `{player_initial_drone_energy}` energy.
- Map is a 2D grid of size `{map_size}`.
- Player's drones are placed around defined point `{player_start_point}`, within square of size `{player_start_potint_size}`.

### Each Turn

Each drone can decide to make a move from: UP, DOWN, LEFT, RIGHT or to use special action: STAY, DUPLICATE.

#### Action: MOVE

Moving consumes energy proportional to distance and current energy of drone. `enegry_loss = drone.energy * loss_factor`, where `loss_factor` is in range of `[0.1, 0.5]`.

If drone decided to move by more than one step then energy consumption is...

#### Action: STAY

Staying in place can benefit in recharging drones energy. `energy_gain = 30`

#### Action: DUPLICATE

By duplicating drone firstly loses half of it's energy and then spawn 2nd drone with the same energy on top of him at the same location.
`energy_loss = drone.energy/2`
& `new Drone(energy_loss, drone.pos + (0,1), player)`

### Turn End

At the end of turn there are performed impact calcuations. There are possible state:

- two or more drones of **different** players at the same field (they will **fight**)
- two or more drones of the **same** player at tha same field (they will **assable**)

#### Action: FIGHT

Drones of the same players will sum their energy and then attack opponent's ones, so both sums would be distracted from eachother giving: `energy_loss = drones_energy_sum / number_of_player_drones_in_fight`.

#### Action: ASSAMBLE

Drones of the same player at the same field are assambling together into one drone. Their energy is summed, but no more than **100**.

### Game End

Game and can be done by:

- If only one player have drones left.
- If the max turn counter was reached `{game_max_turns}`.
- If there are no drones ofc.

---

## How to start

### Creating game environemnt and simulating:

```python
# Initialise data storage impl
data_store = DataStore()

# --- Single Game Container Start ---
container = SingleGameContainer()\
    .with_config(CONFIG_PATH, IS_DISPLAY, GAME_NAME)\
    .with_data_store(data_store)\
    .simulate()\
    .save_game_outcome(FOLDER_PREFIX)
# --- Single Game Container End ---
```

### Visualizing game data:

```python
# Read data from saved storage
data_store = DataStore().with_data_from_file(FRAME_DB_PATH, DECISION_DB_PATH)

# Initialise game visualization module
data_visualizer = DataVisualizer(GAME_NAME, IS_DISPLAY)

# Replay game and save gif
img_frames = data_visualizer.replay_game(data_store.db_frame, data_store.db_decission)
data_visualizer.save_gif(img_frames, GIF_PATH)

# Display plot created from data and save it
plt = data_visualizer.plot_from_data(data_store.db_frame)
data_visualizer.save_plot(plt, PLOT_PATH)
```

## Config file

    {

    }

## Progress fotage:

- First visualization tool. (random bots)
  ![](.git_examples/early_work_visualization_tool_3.gif)
  ![](.git_examples/early_work_visualization_tool_1.gif)
  ![](.git_examples/early_work_visualization_tool_2.gif)

- Early try with 3 Random bots. (Movement)
  ![](.git_examples/early_work_random_bots.png)

- Early try with 3 Random bots. (Duplication & Movement)
  ![](.git_examples/early_work_random_bots_with_duplication_impl.png)

- Early try with 3 Random bots. (Duplication & Movement) (Modified actions per player)
  ![](.git_examples/early_work_random_bots_individual_pool_of_actions.png)

- Early try with 3 Random bots. (Duplication & Movement & Attacking) (Modified actions/stats per photo)
  ![](.git_examples/early_work_random_bots_attacking_impl.png)
