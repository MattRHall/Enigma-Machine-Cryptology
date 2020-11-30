from enigma import *
import itertools

# Challenge 1 - 3 possibilities (reflector A, B or C)
def encode1():
    answer = []
    for ref in ["A","B","C"]:
        pb = Plugboard()
        pb.multiple_adds("KI","XN","FL")
        r1 = Rotor("Beta","M",4, pawl = None) 
        r2 = Rotor("Gamma","J",2)
        r3 = Rotor("V","M",14)
        rotor = Rotor_spindle(r1, r2, r3)
        reflector = Reflector(ref)
        E = Enigma_machine(rotor, reflector, pb)
        encoded_str = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
        decoded_str = E.encode(encoded_str)
        
        if "SECRETS" in decoded_str:
            answer.append(str(ref) + ": " + str(decoded_str))
    return answer

# Challenge 2 - 17,576 possibilities (26x26x26)
def encode2():
    answer = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    start_pos = itertools.product(alphabet,alphabet,alphabet)
    for i,j,k in start_pos:
        pb = Plugboard()
        pb.multiple_adds("VH","PT", "ZG", "BJ", "EY", "FS")
        r1 = Rotor("Beta", i, 23, pawl = None)
        r2 = Rotor("I", j, 2)
        r3 = Rotor("III", k, 10)
        reflector = Reflector("B")
        rotor = Rotor_spindle(r1, r2, r3)
        E = Enigma_machine(rotor, reflector, pb)
        encoded_str = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
        decoded_str = E.encode(encoded_str)

        if "UNIVERSITY" in decoded_str:
            answer.append(str(i) + str(j) + str(k) + ":" + str(decoded_str))
    return answer

# Challenge 3 - 98,304 possibilities (4x4x4x3x8x8x8)
def encode3():
    answer = []
    a = [["II","IV","Gamma","Beta"],
        ["II","IV","Gamma","Beta"],
        ["II","IV","Gamma","Beta"],
        ["A","B","C"],
        [2,4,6,8,20,22,24,26],
        [2,4,6,8,20,22,24,26],
        [2,4,6,8,20,22,24,26]]
    input_domain = itertools.product(*a)

    pb = Plugboard()
    pb.multiple_adds("FH","TS","BE","UQ","KD","AL")
    for a1,a2,a3,r,s1,s2,s3 in input_domain:
        r1 = Rotor(a1, "E", s1, pawl = None)
        r2 = Rotor(a2, "M", s2)
        r3 = Rotor(a3, "Y", s3)
        rotor = Rotor_spindle(r1, r2, r3)
        reflector = Reflector(r)
        E = Enigma_machine(rotor, reflector, pb)
        encoded_str = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
        decoded_str = E.encode(encoded_str)
        
        if "THOUSANDS" in decoded_str:
            answer.append(str(a1) + " " + str(a2) + " " + str(a3) + ", " + str(r) +
            " " + str(s1) + " " + str(s2) + " " + str(s3) + ": " + str(decoded_str))
    return answer

# Challenge 4 - 132 possibilities (12!/(12-2)!)
def encode4():
    answer = []
    alphabet = "DEKLMOQTUXYZ"
    possibilities = itertools.product(alphabet,alphabet)
    plug_poss = [x for x in possibilities if x[0] != x[1]]
    for x in  plug_poss:
        pb = Plugboard()
        pb.multiple_adds("WP", "RJ", "VF", "HN", "CG", "BS", "A" + x[0], "I" + x[1])
        r1 = Rotor("V","S",24, pawl = None)
        r2 = Rotor("III","W",12)
        r3 = Rotor("IV","U",10)
        rotor = Rotor_spindle(r1,r2,r3)
        reflector = Reflector("A")
        E = Enigma_machine(rotor, reflector, pb)
        encoded_str = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
        decoded_str = E.encode(encoded_str)
        
        if "TUTORS" in decoded_str:
            answer.append("A"+str(x[0])+ " " + "I" + str(x[1]) + ": " + str(decoded_str))
    return answer

# Challenge 5 - 6435 possibilities. 13 pairs of letters. 13C4 = 715. Each 4 pairs have
# 3 ways of swapping. 715*3 = 2145. There are 3 reflectors to test, 2145*3 = 6435.
def encode5():
    answer = []
    for reflector in  ["YRUHQSLDPXNGOKMIEBFZCWVJAT", "FVPJIAOYEDRZXWGCTKUQSBNMHL", "EJMZALYXVBWFCRQUONTSPIKHGD"]:
        alphabet =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        all_letters = list(zip(alphabet,reflector))

        pairs = []
        for i in range(26):
            if ((all_letters[i][0],all_letters[i][1]) not in pairs and
                (all_letters[i][1],all_letters[i][0]) not in pairs):
                pairs.append((all_letters[i][0],all_letters[i][1]))
                
        all_pairs = itertools.combinations(pairs,4)
        all_reflectors = []

        for p in all_pairs:
            pair_poss = [[(p[0],p[1]),(p[2],p[3])],[(p[0],p[2]),(p[1],p[3])],[(p[0],p[3]),(p[1],p[2])]]
            for leads in pair_poss:
                ref_dict = {leads[0][0][0]:leads[0][1][0], leads[0][0][1]:leads[0][1][1],
                        leads[1][0][0]:leads[1][1][0], leads[1][0][1]:leads[1][1][1]}

                new_reflector = ""
                count = 0
                for i in reflector:
                    if i in ref_dict.keys() or i in ref_dict.values():
                        count += 1
                        for k,v in ref_dict.items():
                            if k == i:
                                new_reflector += v
                            if v == i:
                                new_reflector += k
                    else:
                        new_reflector += i
                            
                all_reflectors.append(new_reflector)

        for reflector_test in all_reflectors:

            pb = Plugboard()
            pb.multiple_adds("UG", "IE", "PO", "NX","WT")
            r1 = Rotor("V","A",6)
            r2 = Rotor("II","J",18)
            r3 = Rotor("IV","L",7)
            rotor = Rotor_spindle(r1, r2, r3)
            
            reflector_try = Reflector.custom_rotor("TEST", reflector_test)
            E = Enigma_machine(rotor, reflector_try, pb)
            encoded_str = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
            decoded_str = E.encode(encoded_str)

            for word in ["INSTAGRAM", "FACEBOOK", "WHATSAPP", "TIKTOK", "SNAPCHAT"]:
                if word in decoded_str:
                    answer.append(str(reflector) + " : " + str(reflector_test) + " : " + str(decoded_str))
    return answer

if __name__ == "__main__":
   # print("-----Challenge1-----")
   # print(encode1())
   # print("")
   # print("-----Challenge2-----")
   # print(encode2())
   # print("")
   # print("-----Challenge3-----")
   # print(encode3())
   # print("")
   # print("-----Challenge4-----")
   # print(encode4())
   # print("")
   # print("-----Challenge5-----")
    print(encode5())
    print("")    