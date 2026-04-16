import random
from itertools import combinations
from .scoring import calculate_score, has_scoring_dice

class FarkleGame:
    def __init__(self, target_score=2000):
        self.target_score = target_score
        self.players = ["Player", "AI"]
        self.scores = {p: 0 for p in self.players}
        self.history = {p: [] for p in self.players}
        self.current_player_idx = 0
        
        self.turn_score = 0
        self.dice_count = 6
        self.current_roll = []
        self.current_turn_holds = []
        self.is_game_over = False
        self.winner = None

    def record_hold(self, roll_snapshot, kept_faces, points):
        self.current_turn_holds.append({
            "roll": list(roll_snapshot),
            "kept": list(kept_faces),
            "points": points,
        })
        
    def current_player(self):
        return self.players[self.current_player_idx]
        
    def roll_dice(self):
        self.current_roll = [random.randint(1, 6) for _ in range(self.dice_count)]
        return self.current_roll
        
    def check_bust(self):
        if not has_scoring_dice(self.current_roll):
            lost = self.turn_score
            self.current_turn_holds.append({
                "roll": list(self.current_roll),
                "kept": [],
                "points": 0,
                "bust": True,
            })
            self.history[self.current_player()].append({
                "type": "bust",
                "amount": lost,
                "holds": list(self.current_turn_holds),
            })
            self.current_turn_holds = []
            self.turn_score = 0
            self.next_turn()
            return True
        return False
        
    def keep_dice(self, kept_dice):
        """
        kept_dice is a list of integers representing the dice faces kept.
        Returns True if valid, False otherwise.
        """
        score, count = calculate_score(kept_dice)
        if score == 0 or count != len(kept_dice):
            return False
            
        # Verify the kept dice are a subset of the current roll
        roll_copy = self.current_roll.copy()
        for d in kept_dice:
            if d in roll_copy:
                roll_copy.remove(d)
            else:
                return False
                
        self.turn_score += score
        self.dice_count -= len(kept_dice)
        
        if self.dice_count == 0:
            self.dice_count = 6 # Hot dice!
            
        return True
        
    def bank(self):
        player = self.current_player()
        banked = self.turn_score
        self.scores[player] += banked
        self.history[player].append({
            "type": "bank",
            "amount": banked,
            "holds": list(self.current_turn_holds),
        })
        self.current_turn_holds = []
        if self.scores[player] >= self.target_score:
            self.is_game_over = True
            self.winner = player
        else:
            self.next_turn()
            
    def next_turn(self):
        self.turn_score = 0
        self.dice_count = 6
        self.current_roll = []
        self.current_turn_holds = []
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        
    def ai_turn(self):
        """
        Executes a single step of the AI's turn.
        Returns (action, roll, kept_dice, turn_score)
        action can be "bust", "bank", or "roll"
        """
        roll = self.roll_dice()
        if self.check_bust():
            return "bust", roll, [], 0
            
        # Find best scoring combination
        best_score = 0
        best_combo = []
        
        for i in range(1, len(roll) + 1):
            for combo in set(combinations(roll, i)):
                score, count = calculate_score(list(combo))
                if score > best_score and count == len(combo):
                    best_score = score
                    best_combo = list(combo)
                    
        if not best_combo:
            self.turn_score = 0
            self.next_turn()
            return "bust", roll, [], 0

        roll_snapshot = list(self.current_roll)
        self.record_hold(roll_snapshot, best_combo, best_score)
        self.keep_dice(best_combo)
        current_turn_score = self.turn_score
        
        # Simple AI logic: bank if we have >= 300 points and <= 2 dice left, or >= 500 points
        if self.turn_score >= 500 or (self.turn_score >= 300 and self.dice_count <= 2):
            self.bank()
            return "bank", roll, best_combo, current_turn_score
        else:
            return "roll", roll, best_combo, current_turn_score
