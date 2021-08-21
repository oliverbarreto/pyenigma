from pyenigma import enigma

def run():
    # 6 Rotors
    machine = enigma.Enigma(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    rotors=[enigma.Rotor.ROTORS[0], enigma.Rotor.ROTORS[1], enigma.Rotor.ROTORS[2], enigma.Rotor.ROTORS[3], enigma.Rotor.ROTORS[4], enigma.Rotor.ROTORS[5]], 
                    initial_position="KVEZMA",
                    reflector=enigma.Reflector.REFLECTORS[1], 
                    plugboard=enigma.Plugboard.PLUGBOARDS[1],
                    verbose=True)
    
    # 3 Rotors
    # machine = enigma.Enigma(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    #                 rotors=[enigma.Rotor.ROTORS[0], enigma.Rotor.ROTORS[1], enigma.Rotor.ROTORS[2]], 
    #                 initial_position="KVE",
    #                 reflector=enigma.Reflector.REFLECTORS[1], 
    #                 plugboard=enigma.Plugboard.PLUGBOARDS[1],
    #                 verbose=True)

    # 1 Rotors
    # machine = enigma.Enigma(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    #                 rotors=[enigma.Rotor.ROTORS[0]], 
    #                 initial_position="K",
    #                 reflector=enigma.Reflector.REFLECTORS[1], 
    #                 plugboard=enigma.Plugboard.PLUGBOARDS[0],
    #                 verbose=True)

    print("""********************************************************************************************************""")
    print("WELCOME TO ENIGMA CHALLENGE")
    print("""********************************************************************************************************""")
    
    message = input("Type the message here: ")

    encrypted_message = machine.encrypt_message(message.replace(" ", ""))
    
    for i in range(0,10):
        print(f"{''.join(i*['.'])}")
    
    print("")
    print(f"Original Message:  {message} (length: {len(message.replace(' ',''))})")
    print(f"Encrypted Message: {encrypted_message}")
    print("""********************************************************************************************************""")


if __name__ == "__main__":
    run()