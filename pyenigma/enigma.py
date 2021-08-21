# https://github.com/NationalSecurityAgency/enigma-simulator/blob/master/components.py

# https://github.com/cedricbonhomme/pyEnigma
# https://github.com/cedricbonhomme/pyEnigma/blob/master/pyenigma/enigma.py
# https://github.com/cedricbonhomme/pyEnigma/blob/master/pyenigma/rotor.py


# Enigma
# ********************************************************************************************************

# PLUGBOARD
# 1. set plugboard direct connection for letter substitution
# 2. encrypt: every time a letter is typed and it is in the plugboard (in the dictrioanry key or value), its is directly subtituted by its counterpart

# ROTORS
# 1. set rotors 
# 2. rotate rotors
# 3. encrypt with rotor FORWARD
# 4. encrypt with rotor BACKWARDS

# REFLECTOR
# 1. set rotor
# 2. reflect

# ENCRYPT MESSAGE
# 0. Initial Config:
#   - Set plugboard 
#   - Set rotors from available
#   - Set Key: Rotors initial position
#   - Get message (lowercased/uppercased everything)
#   - Encrypt every letter of the message
# 1. Rotate rotors first
# 2. Plugboard
# 3. WAY FORWARD: , encrypt rotor1, rotor2, rotor3, ..., rotorN
# 4. Reflect
# 5. WAY BACK: encrypt rotorN, ..., rotor3, rotor2, rotor1
# 6. Print final message



class Plugboard(object):
    PLUGBOARDS = [{" ":""},
                  {"E":"F", "O":"X", "L":"M", "W":"S","D":"P"},
                  {"": " ", "A":"B", "C":"D", "E":"F", "G":"H","I":"J", "K":"L", "M":"N", "O":"P", "Q":"R","S":"T","U":"V", "X":"Y", "Z":"W"},] # Example Wiring

    def __init__(self, wiring=None, verbose=False):
        if wiring != None:
            self.wiring = wiring
        else:
            self.wiring = self.PLUGBOARDS[0]

        if verbose != None:
            self.verbose = verbose

    def print_plugboard(self):
        print(f"PLUGBOARD:")
        for char in self.wiring.keys():
            print(f"            Letter: '{char}' -> '{self.wiring[char]}'")

    def encrypt(self, char):
        """Get the value if exists for a key, otherwise the letter it's not substituted
        """
        temp_char = ""
        
        if char.upper() in self.wiring.keys():
            temp_char = self.wiring[char.upper()]
            
        elif char.upper() in self.wiring.values():
            temp_char = [key for key, value in self.wiring.items() if value == char][0].upper()

        else:
            temp_char = char.upper()
            
        if self.verbose:
            print("***** PLUGBOARD Encryption *****")
            print(f"Encode Char: '{char}' -> Encoded Char: '{temp_char}'")

        return temp_char


class Rotor(object):

    ROTORS = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ',     #1
            'AJDKSIRUXBLHWTMCQGZNPYFVOE',        
            'BDFHJLCPRTXVZNYEIWGAKMUSQO',        
            'ESOVPZJAYQUIRHXLNFTGKDCMWB',        
            'VZBRGITYUPSDNHLXAWMJQOFECK',      
            'JPGVOUMFYQBENHZRDKASXLICTW',       
            'NZJHGRCXMYSWBOUFAIVLPEKQDT',        
            'FKQHTLXOCBJSPDZRAMEWNIUYGV',]        #8   

    def __init__(self, alphabet, wiring=None, position=0, verbose=False):

        self.verbose = verbose
        self.alphabet = alphabet                # The alphabet used
        
        if wiring != None:
            self.wiring = wiring                # The physical wiring of the rotor: the order of letters in the rotor.
        else:
            self.wiring = self.ROTORS[0]
        
        self.position = position                # Position in the chain of rotors

        self.needs_to_rotate = False            # Flags when this rotor needs to rotate. It is set by the previous rotor in the chain 
        self.current_rotor_state = self.wiring  # Current rotation in this rotor.
        self.tick_count = 0                     # It is always in range from (0...25) based on MOD 26. When 0, it means rotation
        self.initial_position = ""              # The initial starting point of this rotor when the mechanism starts
        
    
    def print_rotor(self):
        print(f"ROTOR: {self.position}")
        print(f"            Alphabet:         {self.alphabet}")
        print(f"            Wiring:           {self.wiring}")
        print(f"            Current State:    {self.current_rotor_state}")
        print(f"            Initial Position: {self.initial_position}")

    def encrypt_forward(self, char):
        """WAY FORWARD: Get the value of the char in the current position of the rotor
        """
        
        temp_char = ""
        if char in self.wiring:
            index = self.alphabet.find(char)
            temp_char = self.current_rotor_state[index]
            
            if self.verbose:
                print(f"***** ROTOR Encryption WAY FORWARD: Index {self.position} *****")
                print(f"            Encode Char: '{char}' -> Encoded Char: {temp_char}")
                self.print_rotor()

            return temp_char
    
    def encrypt_backwards(self, char):
        """WAY BACKWARDS: Get the value of the char in the current position of the rotor
        """
        
        temp_char = ""

        if char in self.current_rotor_state:
            index = self.current_rotor_state.find(char)
            temp_char = self.alphabet[index]

            if self.verbose:
                print(f"***** ROTOR Encryption - WAY BACKWARDS: Index {self.position} *****")
                print(f"            Encode Char: '{char}' -> Encoded Char: {temp_char}")
                self.print_rotor()
                
            return temp_char
    
    def letter_for_index(self, index=0):
        return rotor.wiring[index]
    
    def index_for_letter(self, char):
        if char in self.wiring:
            return self.wiring.find(char)
            
    def tick(self):
        self.tick_count = (self.tick_count + 1 ) % 26
        self.current_rotor_state = self.current_rotor_state[-1] + self.current_rotor_state[:-1]
    
    def set_initial_position(self, char):
        if char in self.wiring:
            index = self.index_for_letter(char)

            for i in range(0, index):
                self.current_rotor_state = self.current_rotor_state[1:] + self.current_rotor_state[0] 
            
            self.tick_count = 0


class Reflector(object):
    REFLECTORS = [ 'EJMZALYXVBWFCRQUONTSPIKHGD',    #A    
                'YRUHQSLDPXNGOKMIEBFZCWVJAT',        
                'FVPJIAOYEDRZXWGCTKUQSBNMHL',]      #C 
    
    def __init__(self, wiring=None,verbose=False):

        self.verbose = verbose

        if wiring != None:
            self.wiring = wiring
        else:
            self.wiring = self.REFLECTORS[0]
     
    def print_reflector(self):
        print(f"REFLECTOR:  {self.wiring}")

    def encrypt(self, char):
        if char in self.wiring:
            index = self.wiring.find(char)
            temp_char = ''.join(reversed(self.wiring))[index]
                        
            if self.verbose:
                print("***** REFLECTOR  Encryption *****")
                print(f"Encode Char: '{char}' -> Encoded Char: '{temp_char}'")
                
            return temp_char


class Enigma(object):

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Configuration
    # ********************************************************************************************************
    def __init__(self,alphabet=None, rotors=None, initial_position=None,reflector=None, plugboard=None, verbose=False):
        """Basic 'wired' Initialization of the Enigma machine.
        """
        # Basic Configuration Check
        Enigma.check_configuration_settings(alphabet=alphabet, rotors=rotors, initial_position=initial_position,reflector=reflector, plugboard=plugboard)
        
        self.verbose = verbose  # To print hjow it works  

        # Alphabet
        if alphabet != None:
            self.alphabet = alphabet
        else:
            self.alphabet = Enigma.ALPHABET
        
        # Plugboard: we remove spaces
        if plugboard != None:
            self.plugboard = Plugboard(wiring=plugboard, verbose=self.verbose)
        else:
            self.plugboard = Plugboard(wiring=None, verbose=self.verbose)

        # Rotors
        self.rotors = []
        if rotors != None:
            for index, rotor in enumerate(rotors):
                self.rotors.append(Rotor(alphabet=self.alphabet, wiring=rotor, position= index, verbose=self.verbose))
        else:
            self.rotors = [Rotor(alphabet=alpself.alphabethabet, wiring=None, verbose=self.verbose)]

        # Set Initial Position of Rotors if passed eg: [KVE...NAF]
        self.initial_position = initial_position
        if initial_position != None and len(initial_position) == len(rotors):
            for index, rotor in enumerate(self.rotors):
                rotor.initial_position = initial_position[index]
                rotor.set_initial_position(initial_position[index])
        
        # Rotors Tick Count 
        self.rotors_tick_count = [0] * len(self.rotors)
        
        # Reflector
        if reflector != None:
            self.reflector = Reflector(wiring=reflector,verbose=self.verbose)
        else:
            self.reflector = Reflector(wiring=None,verbose=self.verbose)
        
        if self.verbose:    
            self.print_configuration()
    
    # Utility Methods
    def print_configuration(self):
        print("---------------------------- Enigma Machine - Initial Configuration ----------------------------")
        print("-------------------------------------------------------------------------------------------------")
        print(f"ALPHABET:   {self.alphabet}")
        self.plugboard.print_plugboard()
        self.reflector.print_reflector()
        print(f"ROTORS INITIAL POSITION:")   
        print(f"            {self.initial_position} - ({len(self.initial_position)} rotors)")
        for rotor in self.rotors:
            rotor.print_rotor()
        print("-------------------------------------------------------------------------------------------------")
        

    @staticmethod
    def check_configuration_settings(alphabet, rotors, initial_position,reflector, plugboard):
        def check_same_alphabet(alphabet, wiring):
            for char in alphabet:
                if char not in wiring:
                    print(f"Char {char} not found in wiring {wiring}")
                    return False
            return True

        # Check that the plugboard has less connections than possible pairs with the alphabet 
        if plugboard != None and alphabet != None:
            if len(plugboard.keys()) > len(alphabet) / 2:
                raise Exception(f"Enigma Machine Configuration Problem - The plugboard has more conexionts than allowed")

        # Check that the plugboard has the same letters than the alphabet
        str = "".join( ( list(plugboard.keys()) + list(plugboard.values()) ))
        if not check_same_alphabet(alphabet=str, wiring=alphabet):
            raise Exception(f"Enigma Machine Configuration Problem - Check that the alphabet and the plugboard have the same letters")
        

        # All rotors must have the same number of characters than the alphabet, 
        # and that all rotors have the same letters than the alphabet
        if rotors != None:
            for index, rotor in enumerate(rotors):
                if len(alphabet) != len(rotor):
                    raise Exception(f"Enigma Machine Configuration Problem - Alphabet and Rotor #{index} wiring both have different number of character")
                if not check_same_alphabet(alphabet=alphabet,wiring=rotor):
                    raise Exception(f"""Enigma Machine Configuration Problem - Check that Rotor #{index} has the same letters than the alphabet. \nRotor:    {rotor}\nAlphabet: {alphabet}""")


        # Initial Position for all rotors
        if len(initial_position) != len(rotors):
            raise Exception(f"Enigma Machine Configuration Problem - Check that the initial position configuration equals the number of rotors defined")

        # Reflector must be equal in legnth to the alphabet
        if len(reflector) != len(alphabet):
            raise Exception(f"Enigma Machine Configuration Problem - Check that the reflector has the same number of chars than the alphabet")

        # Check that the reflector has the same letters than the alphabet
        if not check_same_alphabet(alphabet=alphabet,wiring=reflector):
            raise Exception(f"Enigma Machine Configuration Problem - Check that the reflector and the plugboard have the same letters")


    # Engine
    # ********************************************************************************************************

    def update_current_rotors_tick_count(self):
        for index, rotor in enumerate(self.rotors):
            self.rotors_tick_count[index] = rotor.tick_count

        if self.verbose:
            print(f"---------------- Rotors Tick Count Current State: {self.rotors_tick_count} --------------------")


    def rotation_mechanism(self):
        """ THIS MECHANISM - The first rotor always moves. 
        After every 26-th rotation, the next rotor in the chain takes a rotation.

        ORIGINAL ENIGMA - After every 26-th rotation of the first rotor, the second also does a rotation.
        In the same way does and the third rotor, after every 26-th rotation of second rotor, it does a rotation, 
        but unlikely to the first pair of rotors, the second also takes a turn when the third takes one.
        """
        # Always move first rotor
        self.rotors[0].tick()
        self.update_current_rotors_tick_count()  

        if self.rotors[0].tick_count == 0 and len(self.rotors) > 1: # If there are more than one rotor, take into account that the next rotor has to be marked to rotate later 
            self.rotors[1].needs_to_rotate = True
            self.update_current_rotors_tick_count()  

        # Apply logic to move the rest of the rotors when the previous has fully moved, if there are more than one rotor
        # From the second rotor, to all available rotors (can be an array of any number of elements), if the previous has reached the tick point (tic_count mod 26 == 0) 
        # and it is marked me to rotate (to avoid rotating rotors that move slower and are in state 0 eg: not rotating the most right rotors in this case (0,1,0,0,0) ).
        # Rotate that rotor and check if that rotation has to mark the next one to rotate before continuing the loop
        if len(self.rotors) > 1:
            for index, rotor in enumerate(self.rotors):
                if  (index != 0) and (self.rotors[index - 1].tick_count == 0) and (self.rotors[index].needs_to_rotate):
                    self.rotors[index].tick()
                    if self.rotors[index].tick_count == 0:
                        self.rotors[index+1].needs_to_rotate = False
                    self.update_current_rotors_tick_count()
                
    def encryption_mechanism(self, char):
        """ Encrypt a character with current rotors configuration: forward, reflector and way backwards, back to the plugboard
        """
        temp_char = char

        # 2. Plugboard: bypass letters with its corresponding letter                       
        temp_char = self.plugboard.encrypt(temp_char)

        # 3. Rotors: WAY FORWARD
        for rotor in self.rotors:
            temp_char = rotor.encrypt_forward(temp_char)

        # 4. Reflector
        temp_char = self.reflector.encrypt(temp_char)

        # 5. Rotors: WAY BACKWARDS
        for rotor in reversed(self.rotors):
            temp_char = rotor.encrypt_backwards(temp_char)

        # 6. Plugboard on the way out as well
        temp_char = self.plugboard.encrypt(temp_char)

        return temp_char

    def encrypt_char(self, char):
        
        # 1. Move Rotors to next step any way. Rotors are moved before the encoding.
        self.rotation_mechanism()

        # 2. The rest of the machinery takes place afterthe plugboard, 
        temp_char = self.encryption_mechanism(char)

        return temp_char
    

    def encrypt_message(self, message):
        encrypted_message = ""

        for char in message.upper():
            if self.verbose:
                print(f"--------------------------------- Encrypting Character: {char} --------------------------------")
            
            encrypted_char = self.encrypt_char(char)
            
            if self.verbose:
                print(f"Encrypted char: {encrypted_char}")
                print(f"-----------------------------------------------------------------------------------------------")
            
            encrypted_message = encrypted_message + encrypted_char
        
        return encrypted_message
