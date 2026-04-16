import sys
from game import FarkleGame

DICE_ART = {
    1: [" ----- ", "|     |", "|  o  |", "|     |", " ----- "],
    2: [" ----- ", "| o   |", "|     |", "|   o |", " ----- "],
    3: [" ----- ", "| o   |", "|  o  |", "|   o |", " ----- "],
    4: [" ----- ", "| o o |", "|     |", "| o o |", " ----- "],
    5: [" ----- ", "| o o |", "|  o  |", "| o o |", " ----- "],
    6: [" ----- ", "| o o |", "| o o |", "| o o |", " ----- "]
}

def print_dice(dice_list):
    if not dice_list:
        return
    lines = [""] * 5
    for d in dice_list:
        art = DICE_ART[d]
        for i in range(5):
            lines[i] += art[i] + "  "
    for line in lines:
        print(line)

def main():
    print("Welcome to Farkle!")
    print("First to 2000 points wins.")
    print("--------------------------")
    
    game = FarkleGame(target_score=2000)
    
    while not game.is_game_over:
        player = game.current_player()
        print(f"\n=== {player}'s Turn ===")
        print(f"Scores -> Player: {game.scores['Player']} | AI: {game.scores['AI']}")
        print(f"Turn Score: {game.turn_score} | Dice remaining: {game.dice_count}")
        
        if player == "AI":
            print("AI is rolling...")
            action, roll, kept, turn_score = game.ai_turn()
            print("AI rolled:")
            print_dice(roll)
            if action == "bust":
                print("AI BUSTED!")
            else:
                print(f"AI kept: {kept}")
                if action == "bank":
                    print(f"AI banked {turn_score} points.")
                else:
                    print(f"AI decides to roll again with {game.dice_count} dice.")
            continue
            
        # Human turn
        input("Press Enter to roll...")
        roll = game.roll_dice()
        print("You rolled:")
        print_dice(roll)
        
        if game.check_bust():
            print("BUST! You lose your turn points.")
            continue
            
        valid_keep = False
        while not valid_keep:
            print("Enter the dice you want to keep (e.g. '1 5 5' or '2 2 2'): ")
            keep_str = input("> ").strip()
            try:
                kept_dice = [int(x) for x in keep_str.split()]
                if not kept_dice:
                    print("You must keep at least one scoring die.")
                    continue
                if game.keep_dice(kept_dice):
                    valid_keep = True
                else:
                    print("Invalid selection. Make sure they are scoring dice from your roll.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
                
        print(f"Turn Score is now: {game.turn_score}")
        
        if game.dice_count == 6:
            print("HOT DICE! You get to roll all 6 dice again!")
            
        while True:
            print("Do you want to (B)ank or (R)oll again?")
            choice = input("> ").strip().lower()
            if choice == 'b':
                print(f"You banked {game.turn_score} points.")
                game.bank()
                break
            elif choice == 'r':
                break
            else:
                print("Invalid choice.")
                
    print("\n==========================")
    print(f"GAME OVER! {game.winner} wins!")
    print(f"Final Scores -> Player: {game.scores['Player']} | AI: {game.scores['AI']}")

if __name__ == "__main__":
    main()
