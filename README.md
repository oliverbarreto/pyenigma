pyEnigma is a Python Enigma machine simulator

## Usage as a Python library

```
from pyenigma import enigma

machine = enigma.Enigma(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    rotors=[enigma.Rotor.ROTORS[0], enigma.Rotor.ROTORS[1], enigma.Rotor.ROTORS[2], enigma.Rotor.ROTORS[3], enigma.Rotor.ROTORS[4], enigma.Rotor.ROTORS[5]], 
                    initial_position="KVEZMA",
                    reflector=enigma.Reflector.REFLECTORS[1], 
                    plugboard=enigma.Plugboard.PLUGBOARDS[1],
                    verbose=True)

message = input("Type the message here: ")
encrypted_message = machine.encrypt_message(message.replace(" ", ""))
print(message)

```