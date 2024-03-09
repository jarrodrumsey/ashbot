import random
import re
from unittest import result

class Dice():
    def __init__(self, die_count, face_count):
        self.die_count = die_count if die_count >= 1 else Exception()
        self.face_count = face_count if face_count >= 1 else None
    
    def roll(self):
        
        if(self.die_count == None or self.face_count == None):
            print("Die value entered incorrectly.")
       
        result = 0 # Related message that the bot will return for these rolls.
        total = 0
        output = ""
        
        for i in range(self.die_count):
            # generate the roll
            result = random.randint(1, self.face_count) ## Current dice roll
            total += result                             ## Total dice rolls summed.
            
            natural = (result == 1 or result == self.face_count)
            nat_append = f" - Natural {result}! " if natural else ""
            
            output += f"({i+1}/{self.die_count}): D{self.face_count}: Rolled - {result}{nat_append}\n"
            
        output += f" --- Total: {total} --- \n"
        output = f"Content too large to show each roll, just showing total: {total}" if(len(output)>=1000) else output 
        return total, output

class RollsModule():
    def __init__(self):
        print("Initialized")

    # "9D20'def stable:print('Hello')"
    
    def roll_str_dice(self, dice_str):

        dice = dice_str.lower() # 1D20 -> 1d20, 1d20 -> 1d20 (Standardize input)
        res = [int(i) for i in dice.split("d") if i.isdigit()]
        
        if len(res) != 2:
            res.insert(0, 1)
            
        count = res[0] 
        value_max = res[1] 

        dice = Dice(count, value_max)
        result, response = dice.roll()
 
        return result, response
     
    def roll_args(self, args):
        result = 0
        response = ""
        for dice_group in args[1:]: # [1:] Skips the first entry which *should* be "!roll"
            value, output = self.roll_str_dice(dice_group)
            result += value
            response += output
        return response + f"\nGrand Total: {result}"
   
    def execute(self, message):
        args = message.content.split()
        response = ""
        try:
            response = "```"+self.roll_args(args)+"```"
        except:
            response = "```Failure to comply with command syntax.```"
        return response


    def test_roll_group(self, max):
       
        count = 2
        val_str = f'{count}D{max}'
        print(f"Test: Rolling {val_str}")
        result = self.roll_str_dice(val_str)
        
        max_bound = max * count
        min_bound = count if (count >= 1) else 1
        
        test_result = "success" if (result[0] >= min_bound and result[0] <= max_bound) else "fail"
        print(f'Test - Result of {val_str}: {result[0]} (Should be between {min_bound} and {max_bound} (inclusive)): {test_result}\n ==============' )
    
    def test_str_roll(self, str):
        args = str.split()
        self.roll_args(args)
       

# Test

roller = RollsModule()

# Roll Individual Dice
print('Test - Rolling Individual Dice\n')

for i in range(1, 7): # D2, D4, D6, D8, D10, D12
    roller.test_roll_group(i * 2) 
roller.test_roll_group(20)  # D20
roller.test_roll_group(100) # D100
roller.test_str_roll("!roll 20D'+'20D20")

