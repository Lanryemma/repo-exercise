#this pro gram is for creating encrypted messages 
import random
import string

"""chars = " " + string.punctuation + string.digits + string.ascii_letters
print(chars)
#now we turn chars to a list so that we can use its elements individual
chars = list(chars)
key = chars.copy()#to create a copy of the list

random.shuffle(key)
#print(f"Normal list of characters: {chars}")
#print(f"encrypted list of characters: {key}")

#ENCRYPT
plain_text = input("Enter a message to encrypt: ")
encrypted_message = ""

for char in plain_text:
   index = chars.index(char)
   encrypted_message += key[index]

print(f"Original message: {plain_text}")
print(f"Encrypted message: {encrypted_message}")

print()
#Now to decrypt the message
plain_text = ""
encrypted_message = input("Enter a message to encrypt: ")

for char in encrypted_message:
   index = key.index(char)
   plain_text += chars[index]

print(f"Encrypted message: {encrypted_message}")
print(f"Original message: {plain_text}")"""





#--------------------------------------------------------------------------------------------------------------------------

#WE ARE CREATING A GAME  OF HANGMAN IN PYTHON
# first we create a list of words to guess from
words = ('apple',"orange","banana","coconut", "pineapple")

#a dictionary of keys to represent the number of guesses
hangman_art = {0:("  ",
                  "  ",
                  "  "),
               1:(" o ",
                  "  ",
                  "  "),
               2:(" o ",
                  " | ",
                  "  "),
               3:(" o ",
                  "/| ",
                  "  "),
               4:(" o ",
                  "/|\\",
                  "  "),
               5:(" o ",
                  "/|\\",
                  "/ "),
               6:(" o ",
                  "/|\\",
                  "/ \\"),}

def display_man(wrong):#to indicate when users guess the wrong letter
   print("**********")
   for line  in hangman_art[wrong]:
      print(f"{line}")
   print("**********")

def display_hint(hint):#to display the hint if he user is getting it right
   #print(hint,end=" ")
   print(" ".join(hint))

def display_answer(answer):#to display answer 
   print(" ".join(answer))

def main():
   answer = random.choice(words)
   hint = ["_"]*len(answer)
   wrong_guesses = 0
   guessed_letters = set()
   is_running = True
   
   while is_running:
      display_man(wrong_guesses)
      display_hint(hint)
      guess = input("Enter your guessed letter: ").lower()
      
      #to make sure the person only type a letter 
      if len(guess) > 1 or not guess.isalpha():
         print("invalid input")
         continue
      
      if guess in  guessed_letters:
         print(f"{guess} is already guess")
      
      guessed_letters.add(guess)
      
      #to display the hint as the user types the correct answers
      if guess in answer:
         for i in range(len(answer)):
            if answer[i] == guess:
               hint[i] = guess
      else:
         wrong_guesses +=1
      
      if "_" not in hint:
         display_man(wrong_guesses)
         display_answer(answer)
         print("YOU WIN!!!")
         is_running = False
      elif wrong_guesses >= len(hangman_art)-1:
         display_man(wrong_guesses)
         display_answer(answer)
         print("YOU LOSE!!!")
         is_running = False
               
               

if __name__ == "__main__":
   main()