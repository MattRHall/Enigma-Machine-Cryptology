
from abc import ABC
from abc import abstractmethod

### Detailed information on the functionality of the engima machine, and the 
### classes below are contained in the readme.md file.  
###

class plugs(ABC):
    """Abstract base class used for creation of PlugLead and Plugboard classes"""
    
    @abstractmethod
    def _input_check(self, user_input, length):
        """Raises value errors if input has incorrect type/length/format"""

        if user_input == None:
            raise ValueError("Please enter a string")
        if isinstance(user_input, str) == False:
            raise TypeError("Input a string")
        if len(user_input) != length:
            raise ValueError("String of incorrect length")
        if user_input.isupper() == False or user_input.isalpha() == False:
            raise ValueError("Uppercase letters only")
        if length == 2 and user_input[0] == user_input[1]:
            raise ValueError("Letters must not be identical")
    
    @abstractmethod
    def encode(self, letter):
        """Returns encoded letter if letter in plug_dict"""

        self._input_check(letter, 1)
        return self.plug_dict[letter] if letter in self.plug_dict else letter
    
    @abstractmethod
    def __contains__(self, letter):
        """Returns true if letter is in plug_dict keys/values"""

        self._input_check(letter, 1)
        if letter in self.plug_dict.keys() or letter in self.plug_dict.values():
            return True
        return False
      
        
class PlugLead(plugs):
    """Creates PlugLead objects which have functionality of Plugleads"""
    
    def __init__(self, lead):
        self._input_check(lead, 2)
        self.plug_dict = {lead[0]:lead[1], lead[1]:lead[0]}
    
    def _input_check(self, user_input, length):
        super()._input_check(user_input, length)
        
    def encode(self, letter):
        return super().encode(letter)
        
    def __getitem__(self, letter):
        return super().encode(letter)
    
    def __contains__(self, letter):
        return super().__contains__(letter) 
                                    
                 
class Plugboard(plugs):
    """Creates Plugboard objects which have functionality of Plugboards"""
    
    def __init__(self):
        self.plug_dict = {}
        
    def __getitem__(self, letter):
        return super().encode(letter)
    
    def __contains__(self, letter):
        return super().__contains__(letter)
 
    def _input_check(self, user_input, length):
        super()._input_check(user_input, length)
        
    def encode(self, letter):
        return super().encode(letter)
    
    def add(self, plug):
        """Checks and removes if Plug occupied before adding new PlugLead"""

        if isinstance(plug, PlugLead) and len(self.plug_dict.keys()) <= 20:
            for key in plug.plug_dict.keys():
                if key in self:
                    self._remove(self[key]) 
                    self._remove(key)
            self.plug_dict.update(plug.plug_dict)
        
    def _remove(self, letter):
        self.plug_dict.pop(letter)
        
    def multiple_adds(self, *args):
        """Creates and adds multiple PlugLeads from a number of letter pairs"""

        if len(args)*2 + len(self.plug_dict.keys()) <= 20:
            for arg in args:
                if isinstance(arg, PlugLead):
                    self.add(arg)
                else:
                    self.add(PlugLead(arg))
        else:
            raise ValueError("Plugboard Full")

class Rotor():
    """Creates Rotor object with all the functionality of a Rotor"""
    
    _alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _notch_dict = {"I" : ["Q"], "II" : ["E"], "III" : ["V"], "IV" : ["J"], "V" : ["Z"]} #HERE  
    _rot_dict = {"I" : "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                "II" : "AJDKSIRUXBLHWTMCQGZNPYFVOE",
                "III" : "BDFHJLCPRTXVZNYEIWGAKMUSQO",
                "IV" : "ESOVPZJAYQUIRHXLNFTGKDCMWB",
                "V" : "VZBRGITYUPSDNHLXAWMJQOFECK",
                "Beta" : "LEYJVCNIXWPBQMDRTAKZGFUHOS",
                "Gamma" : "FSOKANUERHMBTIYCWLQPZXVGJD"}
    _reflectors = {"A": "EJMZALYXVBWFCRQUONTSPIKHGD",
                 "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                 "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}
    
    def __init__(self, rot_name, start_pos = "A", ring_pos = 1, pawl = True):
        self._rotor_check_str(start_pos)
        self._rotor_check_int(ring_pos)
        
        self._rotor_name = rot_name
        self._start_pos = start_pos
        self._ring_pos = ring_pos
        self._notch = Rotor._notch_dict.get(rot_name, [None])
        self._pawl = pawl
        
        # Create rotor variable, which is a list letters A-Z, adjusted for positioning
        self._rotor = [Rotor._alphabet[(i + ord(self._start_pos) - 64 - self._ring_pos) % 26]
         for i in range(26)]
        
        # Create dictionaries which represent the internal wiring within a rotor
        self._mapping_rl = dict(zip(Rotor._alphabet, Rotor._rot_dict[rot_name]))
        self._mapping_lr = dict(zip(Rotor._rot_dict[rot_name], Rotor._alphabet))
        
        # Adjust the list containing notch / notches for ring position.
        self._adjusted_notch = []
        if self._notch != [None]: ##HERE
            for i in Rotor._notch_dict[self._rotor_name]:
                self._adjusted_notch.append(Rotor._alphabet[25-(-self._alphabet.find(i)
                                                 + self._ring_pos - 2)%26])
        else:
            self._adjusted_notch = [None]
           
    def _rotor_check_int(self, user_input):
        if isinstance(user_input, int) and (user_input > 26 or user_input < 1):
            raise ValueError("Integer 1-26")
            
    def _rotor_check_str(self, user_input):    
        if isinstance(user_input, str) and user_input.isalpha() == False:
            raise ValueError("Letter A-Z")

    def rotate(self):
        """'Rotates a rotor by taking letter and index 0 and moving it to end"""

        self._rotor.append(self._rotor.pop(0))    
    
    def _encode_right_to_left(self, index_in):
        """Encodes a letter in right to left manner by checking entrance index and mapping"""

        self._rotor_check_int(index_in)
        connector = self._rotor[index_in - 1]
        pin = self._mapping_rl[connector]
        difference = ord(pin) - ord(connector)
        return 26 - (- index_in - difference ) % 26
 
    def _encode_left_to_right(self, index_in):
        """Encodes a letter in left to right manner by checking entrance index and mapping"""

        self._rotor_check_int(index_in)
        connector = self._rotor[index_in - 1]
        pin = self._mapping_lr[connector]
        difference = ord(pin) - ord(connector)
        return 26 - (- index_in - difference ) % 26
    
    def __str__(self):
        return (f"Rotor: {self._rotor_name}, Start Position: {self._start_pos}," +
                f" Ring Position: {self._ring_pos}, Notch: {self._notch}," +
                f" (Adj. Notch: {self._adjusted_notch}), Current Position: {self._rotor[0]}")
    
    @classmethod
    def custom_rotor(cls, rot_name, mapping, notch = [None], start_pos = "A", ring_pos = 1, pawl = True):
        """Create a Rotor object will customisable name / mapping / notches / pawl"""
        
        if set(mapping) != set(Rotor._alphabet):
            raise ValueError("mapping must be all A-Z")
        if notch != [None]:
            for _notch in notch:
                if _notch.isalpha() != True or len(_notch) != 1:
                    raise ValueError("Notch must be letter A-Z or None")
        if rot_name not in ["I", "II", "III", "IV", "V", "Beta","Gamma"]:
            Rotor._rot_dict[rot_name] = mapping
            Rotor._notch_dict[rot_name] = notch
        return cls(rot_name, start_pos, ring_pos, pawl)
        

class Reflector(Rotor):
    """Creates Reflector object with functionality of reflector"""

    def __init__(self, rot_name):
        self._rotor_check_str(rot_name)
        
        self._rotor_name = rot_name 
        self._pawl = False
        self._rotor = Rotor._alphabet
        self._reflector = Reflector._reflectors[rot_name]
        
        self._mapping_rl = dict(zip(Rotor._alphabet, self._reflector))
        self._mapping_lr = dict(zip(Rotor._alphabet, self._reflector))
        
    @classmethod
    def custom_rotor(cls, rot_name, mapping):
        if set(mapping) != set(Rotor._alphabet):
            raise ValueError("mapping must be all A-Z")
        if rot_name not in ["A","B","C"]:
            Reflector._reflectors[rot_name] = mapping
        return cls(rot_name)

    def __str__(self):
        return (f"Reflector: {self._rotor_name}")

class Rotor_spindle():
    """Creates Rotor_spindle object by combining mulitple rotors together"""
    
    def __init__(self, *args):
        
        if all([isinstance(arg, Rotor) for arg in args]) != True:
            raise TypeError("Rotor instances only")
        
        # Reverse rotors. Rotors inputted in right to left manner. This makes left to right.
        self.args = args[::-1]
        
    def rotate_spindle(self):
        """Internal rotation mechanism that is called when key is pressed"""
        
        rotor_notch_pawl = []
        
        # Create a list of tuples. One tuple for each rotor.
        # (True, False) would indicate Rotor is on its notch but does not have a pawl on its left
        for idx in range(len(self.args)):
            if self.args[idx]._adjusted_notch == [None]:
                rotor_notch_pawl.append((None, self.args[idx]._pawl))
            else:
                rotor_notch_pawl.append((self.args[idx]._rotor[0] in self.args[idx]._adjusted_notch,
                                        self.args[idx]._pawl))
        
        # Rotation mechanism. Rotator rotated if current rotor on notch and has pawl on left
        # or previous rotor on notch and has pawl on left. Rotor on right always rotates.
        for idx in range(len(self.args)):
            if idx == 0:
                self.args[idx].rotate()
            else:
                if rotor_notch_pawl[idx-1] == (True, True) or rotor_notch_pawl[idx] == (True, True):
                    self.args[idx].rotate()
                        
    def _encode_right_to_left(self, index_in):
        """Encode a letter in a right to left manner"""

        for _rotor in self.args:
            index_in = _rotor._encode_right_to_left(index_in)
        return index_in

    def _encode_left_to_right(self, index_in):
        """Encode a letter in a left to right manner"""

        for _rotor in self.args[::-1]:
            index_in = _rotor._encode_left_to_right(index_in)
        return index_in

    def __str__(self):
        positions = [i._rotor[0] for i in self.args[::-1]]
        return (f"Rotor positions: {positions}")

class Enigma_machine():
    
        _alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
        def __init__(self, rotorspindle, reflector, plugboard = None, etw = None):
            
            self._plugboard = Plugboard() if plugboard == None else plugboard
            self._rotorspindle = rotorspindle
            self._reflector = reflector
            
            # Create dictionaries to allow numbers / integers to be converted
            self._alphabet_to_num = dict(zip(Enigma_machine._alphabet,range(1,27)))
            self._num_to_alphabet = dict(zip(range(1,27),Enigma_machine._alphabet))  

            # Setup functionality of entry-wheel (not always present)
            if etw == None:
                self._etw = None
            else:
                if set(etw) != set(Enigma_machine._alphabet):
                    raise ValueError("etw must be a set of the alphabet")
                else:
                    self._etw = etw
                    self._etw_alphabet = dict(zip(etw, Enigma_machine._alphabet))
                    self._alphabet_etw = dict(zip(Enigma_machine._alphabet, etw))
            
        def encode(self, word, output = False):
            """Will encode a string, output will return information on encoding process"""

            if word == "":
                raise ValueError("Insert atleast one letter")
                
            for letter in word:
                if letter.upper().isalpha() == False:
                    raise ValueError("Inappropriate argument")

            # Variables created to store information about encoding process (used in output)
            rotor_names = [i._rotor_name for i in self._rotorspindle.args[::-1]]
            start_pos = [i._start_pos for i in self._rotorspindle.args[::-1]]
            ring_pos = [i._ring_pos for i in self._rotorspindle.args[::-1]]
            pawls = [i._pawl for i in self._rotorspindle.args[::-1]]

            if output:
                print(f"Engima Machine - Rotor Names: {rotor_names}, Start Positions: {start_pos}, " + 
                    f"Ring Positions: {ring_pos}, Reflector: {self._reflector._rotor_name}, " +
                    f"Pawl on left: {pawls}")

            encoding = ""

            for letter in word:
                
                # Encode letter through plugboard
                letter_in = self._plugboard.encode(letter.upper())
                
                # Encode letter through entry wheel
                if self._etw == None:
                    etw_letter = letter_in
                else:
                    etw_letter = self._etw_alphabet[letter_in]

                # Establish entry index for spindle
                spindle_idx_in = self._alphabet_to_num[etw_letter]

                # Save rotors settings / rotate / save rotor settings
                rotor_setting_in = [i._rotor[0] for i in self._rotorspindle.args[::-1]]
                self._rotorspindle.rotate_spindle()
                rotor_setting_out = [i._rotor[0] for i in self._rotorspindle.args[::-1]]
               
                # Establish exit index from spindle
                spindle_idx_out = self._rotorspindle._encode_right_to_left(spindle_idx_in)
                
                # Establish exit index from reflector
                reflect_idx = self._reflector._encode_right_to_left(spindle_idx_out)
                
                # Establish exit index from spindle
                spindle_idx_out_2 = self._rotorspindle._encode_left_to_right(reflect_idx)
                
                # Establish exit letter from spindle
                letter_out = self._num_to_alphabet[spindle_idx_out_2]
                
                # Establish exit letter from entry wheel
                if self._etw == None:
                    etw_letter_out = letter_out
                else:
                    etw_letter_out = self._alphabet_etw[letter_out]
                
                # Establish encoded letter
                encoded_letter = self._plugboard.encode(etw_letter_out)

                if output:
                    print(f"Start Position: {rotor_setting_in}, " + 
                    f"Letter In: {letter}, End Position: {rotor_setting_out}, Letter Out: {encoded_letter}")

                encoding += encoded_letter

            if output:
                return (f"Encoding: {encoding} ")
            else:
                return encoding 

if __name__ == "__main__":
    print("-----PlugLead checks-----")
    obj = PlugLead("AB")
    obj.encode("A")
    print(obj["A"])
    print(obj["B"])
    print("A" in obj)
    print("C" in obj)
    print("")

    print("-----Plugboard checks-----")
    pb = Plugboard()
    pb.add(PlugLead("AB"))
    print(pb.plug_dict)
    pb.add(PlugLead("BC"))
    print(pb.plug_dict)
    pb.multiple_adds("XY", "MN")
    print(pb.plug_dict)
    print("")

    print("-----Rotor checks-----")
    r1 = Rotor("Beta","C",20)
    print(r1)
    r2 = Rotor("I","A",1)
    print(r2)
    r2.rotate()
    print(r2)
    print("")

    print("-----Customised rotor check (double notchs)-----")
    r3 = Rotor.custom_rotor("VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", notch = ["H","U"],
     start_pos = "A", ring_pos = 1, pawl = True)
    print(r3)
    print(Rotor._rot_dict)
    print("")

    print("-----Reflector check-----")
    r4 = Reflector("A")
    print(r4)
    print("")

    print("-----Custom _reflector check-----")
    r5 = Reflector.custom_rotor("BTHIN", "ENKQAUYWJICOPBLMDXZVFTHRGS")
    print(r5)
    print(Rotor._reflectors)
    print("")

    print("-----Rotor_spindle check-----")
    r1 = Rotor("I","A",1)
    r2 = Rotor("II","A",1)
    r3 = Rotor("III","A",1)
    Spindle = Rotor_spindle(r1,r2,r3)
    print(Spindle)
    Spindle.rotate_spindle()
    print(Spindle)
    print("")

    print("-----Single letter encode - No Output -----")
    pb1 = Plugboard()
    r1 = Rotor("I","A",1, pawl = None)
    r2 = Rotor("II","A",1)
    r3 = Rotor("III","Z",1)
    rotor = Rotor_spindle(r1,r2,r3)
    rotor._encode_right_to_left(5)
    reflector = Reflector("B")
    E2 = Enigma_machine(rotor, reflector, pb1)
    print(E2.encode("A"))
    print("")

    print("-----Single letter encode - Output -----")
    pb1 = Plugboard()
    r1 = Rotor("I","A",1, pawl = None)
    r2 = Rotor("II","A",1)
    r3 = Rotor("III","Z",1)
    rotor = Rotor_spindle(r1,r2,r3)
    rotor._encode_right_to_left(5)
    reflector = Reflector("B")
    E2 = Enigma_machine(rotor, reflector, pb1)
    print(E2.encode("A", output = True))
    print("")

    print("-----Multiple letter encode - Output -----")
    pb1 = Plugboard()
    r1 = Rotor("I","A",1, pawl = None)
    r2 = Rotor("II","A",1)
    r3 = Rotor("III","Z",1)
    rotor = Rotor_spindle(r1,r2,r3)
    rotor._encode_right_to_left(5)
    reflector = Reflector("B")
    E2 = Enigma_machine(rotor, reflector, pb1)
    print(E2.encode("ABC", output = True))
    print("")

    print("-----Multiple letter encode - Output -----")
    pb1 = Plugboard()
    pb1.multiple_adds("HL","MO","AJ","CX","BZ","SR","NI","YW","DG","PK")
    r1 = Rotor("I","A",1, pawl = None)
    r2 = Rotor("II","A",1)
    r3 = Rotor("III","Z",1)
    rotor = Rotor_spindle(r1,r2,r3)
    reflector = Reflector("B")
    E2 = Enigma_machine(rotor, reflector, pb1)
    print(E2.encode("RFKTMBXVVW", output = True))
    print("")







