# Engima Machine
------
### Introduction
The engima machine is an encryption device used by Nazi Germany in world war II to encrypt/decrypt messages. This project replicates the functionality of an enigma machine (plugleads / plugboards / rotor system / reflectors). This engima machine is designed to be highly customisable, which means historically accurate enigma machines can be generated (of which there are multiple versions), or user defined setups (infinite rotors, customised rotor wirings and customised reflectors).

### Files
- engima.ipynb (Jupyter notebook) - Describes working of enigma machine, and demonstrates some of its functionality.  
- engima.py (Python file) - Contains engima machine classes.
- readme.md (Markdown file) - Documentation describing engima machine classes / functionality.

### Classes

#### 1. plugs(ABC)
Abstract Base Class, which serves as parent class for PlugLead and Plugboard. 

Methods  
- **encode(self, letter)**  
Returns encoded letter if letter is in plug_dict, otherwise returns letter.  
- **_input_check(self, user_input, length)**  
Checks whether user_input is a string of length equal to length, contains only uppercase letters, and those letters are not identical, otherwise ValueError raised.
- **\__contains__(self, letter)**  
Returns true if letter is in the keys or values in plug_dict.

#### 2. PlugLead(plugs)  
The PlugLead class contains the functionality of a PlugLead. It inherits from the ABC class. Plugleads are stored in plug_dict, with each pair of letters represented by a key/value and value/key pair.

Attributes  
- **plug_dict**  
Dictionary; equal to {"A":"B","B":"A"} if lead = "AB". Plug_dict created when class instantiated, as long as letters are of correct format.

Methods  
- **__init__(self, lead = None)**  
Will instantiate PlugLead object and create plug_dict from two letters in lead.
- **encode(self, letter)**  
Returns encoded letter if letter is in plug_dict, otherwise returns letter.  
- **_input_check(self, user_input, length)**  
Checks whether user_input is a string of length equal to length, contains only uppercase letters, and those letters are not identical, otherwise ValueError raised.
- **\__getitem__(self, letter)**  
Will return encode(letter) which allows PlugLead object to operate like a dictionary. So obj = PlugLead("AB"), obj["A"] will return B.
- **\__contains__(self, letter)**  
Will return True if letter is in plug_dict, otherwise will return False.

```python
obj = PlugLead("AB")
obj.encode("A") # B
obj["A"] # B
obj["B"] # A
"A" in obj # True
"C" in obj # False
```

#### 3. Plugboard(plugs)
The Plugboard class which contains the functionality of a PlugBoard. It inherits from the ABC class. Plugleads are stored in plug_dict, with each pair of letters represented by a key/value and value/key pair. Multiple PlugLeads can be added in a single method. PlugLeads will be automatically removed if attempt is made to add PlugLead to occupied letter.

Attributes  
- **plug_dict**  
Dictionary; equal to {"A":"B","B":"A", "C":"D","D":"C"} if PlugLead("AB") and PlugLead("CD") added. Empty Plug_dict created when class instantiated.

Methods  
- **__init__(self)**  
Will instantiate Plugboard object and create plug_dict as an empty dictionary.
- **add(self, plug)**  
Will add a PlugLead object to Plugboard as long as Plugboard not full (less than 20 letters occupied). If letter already occupied, the associate PlugLead will be removed from the Plugboard using _remove, before the new one is added.
- **multiple_adds(self, *args)**  
Will create multiple PlugLeads, and add those PlugLeads to the Plugboard object.
- **encode(self, letter)**  
Returns encoded letter if letter is in plug_dict, otherwise returns letter.
- **_remove(self, letter)**  
Will remove a letter from plug_dict.
- **_input_check(self, user_input, length)**  
Checks whether user_input is a string of length equal to length, contains only uppercase letters, and those letters are not identical, otherwise ValueError raised.
- **\__getitem__(self, letter)**  
Will return encode(letter) which allows PlugLead object to operate like a dictionary. Plugboard object 'obj' which contains PlugLead("AB"); obj["A"] will return B.
- **\__contains__(self, letter)**  
Will return True if letter is in plug_dict, otherwise will return False.

```python
pb = Plugboard()
pb.add(PlugLead("AB"))
pb.plug_dict # {"A":"B","B":"A"}
pb.add(PlugLead("BC"))
pb.plug_dict # {"B":"C", "C:B"}
pb.multiple_adds("XY", "MN")
pb.plug_dict # {'B': 'C', 'C': 'B', 'X': 'Y', 'Y': 'X', 'M': 'N', 'N': 'M'}
```

#### 3. Rotor()
The Rotor class contains the functionality of a Rotor. It requires the rotor name, start position, ring position, and whether the rotor has a pawl on its left. The pawl is critical to the rotation mechanism. A rotor will rotate if the previous rotor has a pawl and is on its notch (pawl drops down and engages ratchet), or if the current rotor has a pawl and its on its notch (pawl drops down an engages ratchet). The reason the 4th rotor does not rotate is because it has no pawl on either side, so it never turns.  

Class Attributes  
- **_alphabet**  
String;  Alphabet A-Z.  
"ABCDEFGHIJKLMNOPQRSTUVWXYZ". 
- **_notch_dict**  
Dictionary;  Keys = rotor names, values = notches.  
{"I" : "Q", "II" : "E", "III" : "V", "IV" : "J", "V" : "Z"} 
- **_rot_dict**  
Dictionary; Keys = rotor names, values = strings representing internal wirings.  
{"I" : "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
"II" : "AJDKSIRUXBLHWTMCQGZNPYFVOE",
"III" : "BDFHJLCPRTXVZNYEIWGAKMUSQO",
"IV" : "ESOVPZJAYQUIRHXLNFTGKDCMWB",
"V" : "VZBRGITYUPSDNHLXAWMJQOFECK",
"Beta" : "LEYJVCNIXWPBQMDRTAKZGFUHOS",
"Gamma" : "FSOKANUERHMBTIYCWLQPZXVGJD"}
- **_reflectors**   
Dictionary;  Keys = reflector names, values = strings representing internal wirings.  
{"A": "EJMZALYXVBWFCRQUONTSPIKHGD",
"B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
"C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}

Attributes  
- **_rotor_name**  
String; Name for rotor. Standard = ["I","II","III","IV","V","Beta","Gamma"]. Customised rotors will allow for customised rotor names, but they can't be the same name as a 'standard' rotor.
- **_start_pos**  
String; Letter between A-Z representing starting position for rotor.
- **_ring_pos**  
Integer; Number between 1-26 representing the ring position for rotor. 
- **_notch**  
String; Letter between A-Z  representing the location of notch in a rotor.
- **_pawl**  
Boolean; A reflector either has a pawl to its left, or it does not. This pawl is the heart of the stepping mechanism. 
- **_rotor**  
List; contains the letters of the alphabet, but adjusted for start / ring position. 
- **_mapping_rl**  
Dictionary; reflects the internal wirings, maps letters on 'right' of rotors with letters on 'left' of rotors.
- **_mapping_lr**  
Dictionary; reflects the internal wirings, maps letters on 'left' of rotors with letters on 'right' of rotors.
- **_adjusted_notch**  
String; Letter between A-Z representing the location of notch after taking account of any adjustments from ring position.

Methods  
- **\__init__(self, rot_name, start_pos = "A", ring_pos = 1, pawl = True)**  
Will instantiate Rotor object and create all the instance variables. It requires the name of the rotor ("I","II","III","IV","V","Beta","Gamma"), and has optional inputs of the start_position, ring_position and whether it has a pawl on its left.
- **rotate(self)**  
Will 'turn' the rotor by moving the first letter in _rotor to the end.
- **_encode_right_to_left(self, index_in)**  
Encodes an 'index' value (1-26) in a right-to-left manner. For example, if a signal enters at index '1', it will check tbe corresponding letter on the rotor it connects to, apply the appropriate mapping for the given rotor, and return the exit index value.
- **_encode_left_to_right(self, letter)**  
Encodes an 'index' value (1-26) in a left-to-right manner. For example, if a signal enters at index '1', it will check tbe corresponding letter on the rotor it connects to, apply the appropriate mapping for the given rotor, and return the exit index value.
- **_rotor_check_int(self, user_input)**  
Raises ValueError if user_input is not an integer between 1 and 26.
- **_rotor_check_str(self, user_input)**  
Raises ValueError if user_input is not a letter between A and Z
- **\__str__(self)**  
Will return a string containing information about the rotor, such as its name, start position, ring position, notch, adjusted notch and current position.

```python
r1 = Rotor("Beta","C",20)
print(r1) # Rotor: Beta, Start Position: C, Ring Position: 20, Notch: [None], (Adj. Notch: [None]), Current Position: J
r2 = Rotor("I","A",1)
print(r2) # Rotor: I, Start Position: A, Ring Position: 1, Notch: ['Q'], (Adj. Notch: ['Q']), Current Position: A
r2.rotate()
print(r2) # Rotor: I, Start Position: A, Ring Position: 1, Notch: ['Q'], (Adj. Notch: ['Q']), Current Position: B
```

@ClassMethod  
- **custom_rotor(cls, rot_name, mapping, notch = None, start_pos = ["A"], ring_pos = 1, pawl = True)**  
This class method allows the user to build a custom rotor, defining the name (can't conflict with inbuilt rotors), start position, ring position, and whether it has a pawl on its left or not. Many different types of rotors were used historically, so this feature allows the user to recreate other types of engima machines, simply by creating own rotors.   

In the example below the rotor 'VIII' is created, it was used in the M3 & M4 Navy variation of the enigma machine, and had two notches. Notice how the Rotor class's variables _rot_dict (which stores rotor mappings) has been updated for the new rotor. 

```python
r3 = Rotor.custom_rotor("VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", notch = ["H","U"], start_pos = "A", ring_pos = 1, pawl = True)
print(r3) # Rotor: VIII, Start Position: A, Ring Position: 1, Notch: ['H', 'U'], (Adj. Notch: ['H', 'U']), Current Position: A
Rotor._rot_dict
# {'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
# 'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
# 'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
# 'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
# 'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
# 'Beta': 'LEYJVCNIXWPBQMDRTAKZGFUHOS',
# 'Gamma': 'FSOKANUERHMBTIYCWLQPZXVGJD',
# 'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV'}
```

#### 4. Reflector(Rotor)
The Reflector class contains the functionality of a reflector in an engima machine. It inherits from the Rotor class, because a Reflector is simply a rotor that does not turn. Therefore the encryption related methods can still be used.

Attributes  
- **_reflector**  
String; represents internal wiring with a reflector, e.g. for reflector "A"; "EJMZALYXVBWFCRQUONTSPIKHGD" 
- **_rotor_name**  
String; Name for rotor. Standard = ["A","B","C"]. Customised rotors will allow for customised rotor names, but they can't be the same name as a 'standard' rotor.
- **_pawl**  
Boolean; set to False as a Reflector does not have a pawl. 
- **_rotor**  
List; contains the letters of the alphabet, but adjusted for start / ring position. 
- **_mapping_rl**  
Dictionary; reflects the internal wirings, maps letters coming into rotor, into letter coming out of rotor, in a right-to-left manner.
- **_mapping_lr**  
Dictionary; reflects the internal wirings, maps letters coming into rotor, into letter coming out of rotor, in a left-to-right manner.  

Methods  
- **\__init__(self, rot_name)**  
Will instantiate Rotor object and create all the instance variables. It requires the name of the reflector.

```python
r4 = Reflector("A")
print(r4) # Reflector: A
print("")

```

@ClassMethod  
- **custom_rotor(cls, rot_name, mapping)**  
This class method allows the user to build a custom reflector. It requires a rotor name and a mapping. The user needs to ensure that the mapping will connect pairs of letters together.  

Custom reflectors provide additional functionality / flexibility to recreate alternative engima versions, or be creative and invent their own. In the example below the reflector 'BTHIN' has been created (used in M3/M4 version of engima machines). Notice how the Rotor class's _reflectors variable has been updated to store the new reflector mapping.

```python
r5 = Reflector.custom_rotor("BTHIN", "ENKQAUYWJICOPBLMDXZVFTHRGS")
print(r5) # Reflector: BTHIN
print(Rotor._reflectors) # {'A': 'EJMZALYXVBWFCRQUONTSPIKHGD', 'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT', 'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL', 'BTHIN': 'ENKQAUYWJICOPBLMDXZVFTHRGS'}
```

#### 5. Rotor_spindle()
The Rotor_spindle class contains the functionality of the combined set of rotors in an engima machine. This class will takes an unlimited number of rotor objects as its argument. This means that a full range of historical engima machines can be created but also completely theoretical engima machines (ones with dozens of rotors for example). Rotors are inputted in a left-to-right manner. 

Attributes  
- **.args**  
List; list of rotors, but in reverse order (so right-to-left).

Methods  
- **rotate_spindle(self)**  
Checks which rotors are on notches, and which have pawls, and rotates the appropriate rotors.
- **_encode_right_to_left(self, index_in)**  
Will encode a letter through the spindle of rotors in a right-to-left manner.
- **_encode_left_to_right(self, index_in)**  
Will encode a letter through the spindle of rotors in a left-to-right manner.
- **\__str__(self)**  
Will return the current positions of all the rotors.

```python
r1 = Rotor("I","A",1)
r2 = Rotor("II","A",1)
r3 = Rotor("III","A",1)
Spindle = Rotor_spindle(r1,r2,r3)
print(Spindle) # ["A","A","A"]
Spindle.rotate_spindle()
print(Spindle) # ["A","A","B"]
```

#### 5. Engima_machine()
The Enigma_machine class combines Plugboard objects, Rotor objects and Reflector objects to create an engima machine. The machine is completely customisable; infinite rotors, custom rotors, custom reflectors, none/multiple notches, and pawl/no pawl are possible. The main limitations are that the first rotor must rotate, and there must be atleast 1 rotor and reflector. 

Class Attributes  
- **_alphabet**  
String; the letters of the alphabet A-Z in order.  

Attributes  
- **_plugboard**  
Plugboard object. 
- **_rotorspindle**  
Rotor_spindle object.
- **_reflector**  
Reflector object. 
- **_alphabet_to_num**  
Dictionary; keys = alphabet A-Z. values = integers 1-26.
- **_num_to_alphabet**  
Dictionary; keys = values = integers 1-26. values = alphabet A-Z. 
- **_etw**  
None if no custom entry-wheel or string representing mapping (only needed for non-military variants).
- **_etw_to_alphabet**  
Dictionary; Mapping from etw to alphabet.  
- **_alphabet_to_etw**  
Dictionary; Mapping from alphabet to etw.  

Methods  
- **\__init__(self, rotorspindle, reflector, plugboard = None)**  
Will instantiate engima machine object, and create all the instance attributes shown above. It requires a Rotor_spindle object, Reflector object and an optional Plugboard.

- **encode(self, word, output = False)**  
Will return an encoded string. If output True, then basic print out will be displayed which show the starting setup of the machine, the position of the rotors, and the encoded string. 

```python
pb1 = Plugboard()
pb1.multiple_adds("HL","MO","AJ","CX","BZ","SR","NI","YW","DG","PK")
r1 = Rotor("I","A",1, pawl = None)
r2 = Rotor("II","A",1)
r3 = Rotor("III","Z",1)
rotor = Rotor_spindle(r1,r2,r
reflector = Reflector("B")
E2 = Enigma_machine(rotor, reflector, pb1)
print(E2.encode("RFKTMBXVVW", output = True))

# Engima Machine - Rotor Names: ['I', 'II', 'III'], Start Positions: ['A', 'A', 'Z'], Ring Positions: [1, 1, 1], Reflector: B, Pawl on left: [None, True, True]
# Start Position: ['A', 'A', 'Z'], Letter In: R, End Position: ['A', 'A', 'A'], Letter Out: H
# Start Position: ['A', 'A', 'A'], Letter In: F, End Position: ['A', 'A', 'B'], Letter Out: E
# Start Position: ['A', 'A', 'B'], Letter In: K, End Position: ['A', 'A', 'C'], Letter Out: L
# Start Position: ['A', 'A', 'C'], Letter In: T, End Position: ['A', 'A', 'D'], Letter Out: L
# Start Position: ['A', 'A', 'D'], Letter In: M, End Position: ['A', 'A', 'E'], Letter Out: O
# Start Position: ['A', 'A', 'E'], Letter In: B, End Position: ['A', 'A', 'F'], Letter Out: W
# Start Position: ['A', 'A', 'F'], Letter In: X, End Position: ['A', 'A', 'G'], Letter Out: O
# Start Position: ['A', 'A', 'G'], Letter In: V, End Position: ['A', 'A', 'H'], Letter Out: R
# Start Position: ['A', 'A', 'H'], Letter In: V, End Position: ['A', 'A', 'I'], Letter Out: L
# Start Position: ['A', 'A', 'I'], Letter In: W, End Position: ['A', 'A', 'J'], Letter Out: D
# Encoding: HELLOWORLD

```

