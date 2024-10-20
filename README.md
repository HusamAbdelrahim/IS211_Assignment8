# Pig Game with Design Patterns (IS211_Assignment8)
# Author: Husam Abdelrahim 

This project is an implementation of the Pig dice game, expanded to include the use of **Proxy** and **Factory** design patterns. It allows for gameplay against a human or computer opponent, and includes an optional timed mode where the game lasts for a maximum of one minute.

## Design Patterns Used

### Proxy Pattern
The `TimedGameProxy` class acts as a proxy for the `Game` class and introduces the timed functionality. This proxy ensures that the game finishes either when a player reaches 100 points or when the time limit (60 seconds) is reached.

### Factory Pattern
The `PlayerFactory` class dynamically instantiates either a `HumanPlayer` or `ComputerPlayer`, based on the arguments provided by the user. This encapsulates the object creation logic, adhering to the Factory design pattern.

## How to Play

Players take turns rolling a die. On each turn, a player may either:
- **Roll**: Add the die result to their current turn total.
  - If the die shows **1**, the player's turn ends, and their turn total is reset.
- **Hold**: Add the turn total to their overall score, and pass the turn to the opponent.

The first player to reach **100 points** wins, unless the timed mode is enabled.

### Computer Strategy
The computer player will **hold** if their score reaches the lesser of 25 points or `100 - x` (where `x` is their current score). Otherwise, the computer will **roll**.

## Usage

To run the game, use the following command:

```bash
python pig_game.py --player1 [human|computer] --player2 [human|computer] --timed
```