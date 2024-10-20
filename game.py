import random
import time
import argparse

# Die class to represent a six-sided die
class Die:
    def __init__(self):
        random.seed(0)

    def roll(self):
        return random.randint(1, 6)

# Base Player class representing a human player
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0  # Initialize player's score to 0
    
    def add_score(self, points):
        self.score += points
    
    def __str__(self):
        return f"{self.name} - Score: {self.score}"

# Inherited class for the computer player, with a predefined strategy
class ComputerPlayer(Player):
    def __init__(self, name="Computer"):
        super().__init__(name)  # Call the base class constructor
    
    # computer's decision-making strategy: roll or hold based on score
    def decide(self):
        """Returns 'r' to roll or 'h' to hold based on strategy."""
        # The computer holds if its score reaches the threshold
        threshold = min(25, 100 - self.score)
        if self.score < threshold:
            return 'r'  # Roll if below threshold
        return 'h'  # Hold otherwise

# factory class to create either human or computer players
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == 'human':
            return Player(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

# main Game class to handle the core game logic
class Game:
    def __init__(self, player1_type='human', player2_type='human'):
        self.die = Die()  # Create a die for rolling
        # Create players using the PlayerFactory class
        self.players = [
            PlayerFactory.create_player(player1_type, "Player 1"),
            PlayerFactory.create_player(player2_type, "Player 2")
        ]
        self.current_player_index = 0  # Track which player's turn it is
    
    # Switch to the other player after each turn
    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % 2
    
    # Get the player whose turn it is
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def play_turn(self):
        player = self.get_current_player()
        turn_total = 0  # Points accumulated during the current turn
        print(f"\n{player.name}'s turn!")
        
        while True:
            # Computer decides automatically, human player inputs 'r' or 'h'
            if isinstance(player, ComputerPlayer):
                action = player.decide()
                print(f"{player.name} chooses to {'roll' if action == 'r' else 'hold'}.")
            else:
                action = input(f"ROLL: [ r ] or HOLD [ h ] ").strip().lower()

            if action == 'r':  # If the player rolls the die
                roll_result = self.die.roll()
                print(f"Rolled: {roll_result}")
                if roll_result == 1:  # Rolling a 1 means the turn ends with no points
                    print("Rolled a 1! No points this turn.")
                    turn_total = 0
                    break
                else:  # Add the rolled points to the turn total
                    turn_total += roll_result
                    print(f"Turn Total: {turn_total}")
            elif action == 'h':  # If the player holds, add turn points to the total score
                player.add_score(turn_total)
                break
            else:
                print("Invalid input. Please enter 'r' or 'h'.")
        
        # Display the player's total score after the turn ends
        print(f"{player.name}'s total score: {player.score}")
    
    # check if any player has won by reaching a score of 100
    def determine_winner(self):
        for player in self.players:
            if player.score >= 100:
                return player
        return None
    
    # Main game loop
    def play(self):
        print("Welcome to the Pig Game!")
        while True:
            self.play_turn()
            winner = self.determine_winner()  # check if there's a winner
            if winner:
                print(f"\n{winner.name} wins with a score of {winner.score}!")
                break
            self.switch_player()  # Switch turns

# add time-based functionality to the game
class TimedGameProxy(Game):
    def __init__(self, player1_type='human', player2_type='human'):
        super().__init__(player1_type, player2_type)
        self.start_time = time.time()  # Track when the game starts
        self.time_limit = 60  # 1 minute time limit
        self.time_up = False

    # Override play_turn to check if the time limit has been exceeded
    def play_turn(self):
        if time.time() - self.start_time > self.time_limit:
            if not self.time_up:
                print("Time is up!")
                self.declare_winner() 
                self.time_up = True
            return
        super().play_turn()  
    
    # declare the player with the highest score as the winner if time runs out
    def declare_winner(self):
        print("Game over! Time limit reached.")
        player1, player2 = self.players
        if player1.score > player2.score:
            winner = player1
        elif player2.score > player1.score:
            winner = player2
        else:
            print("It's a tie!")
            return
        
        print(f"\n{winner.name} wins with a score of {winner.score}!")

if __name__ == "__main__":
    # argument parsing for player types and timed mode
    parser = argparse.ArgumentParser(description="Play the Pig Game")
    parser.add_argument('--player1', choices=['human', 'computer'], default='human', help='Type of player 1')
    parser.add_argument('--player2', choices=['human', 'computer'], default='human', help='Type of player 2')
    parser.add_argument('--timed', action='store_true', help='Enable timed game mode')

    args = parser.parse_args()

    # If timed mode is enabled, use TimedGameProxy, otherwise use the normal Game class
    if args.timed:
        game = TimedGameProxy(args.player1, args.player2)
    else:
        game = Game(args.player1, args.player2)
    
    game.play()  # Start the game
