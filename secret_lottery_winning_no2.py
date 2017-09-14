### QUESTION:
'''
    Mr. X is approached in the subway by a guy who claims to be an alien stranded on Earth and to possess time machine
that allows him to know the future. He needs funds to fix his flying saucer but filling in winning numbers for next week's lottery
would create a time paradox. Therefore, he's willing to sell next week's winning numbers to Mr. X at a favorable price. Mr. X,
as gullible as he is, feels that this may be a scam and asks for a proof. Alien gives him the next week's winning numbers in
encrypted form so that Mr. X can't use them and then decide not to pay for them. After the lottery draw he'll give Mr. X the key
to unlock the file and Mr. X can verify that the prediction was correct.
After the draw, Mr. X gets the key and lo and behold, the numbers are correct! To rule out the possibility that it happened by chance,
they do the experiment twice. Then thrice. Finally, Mr. X is persuaded. He pays the alien and gets the set of numbers for the next
week's draw. But the numbers drawn are completely different.
    And now the question: How did the scam work? 
'''

### SOLUTION:
from random import randint

gen_encrypted_winning_no    = lambda    : ''.join([chr(randint(48,90)) for _ in range(256)])
def gen_decrypt_key(locked_winning_no_to_MrX, data):
    key = ''.join(['1' if i+1 in data else '0' for i in range(36)])
    d = dict([(i,chr(v)) for i,v in enumerate(range(ord('0'), ord('9')) + range(ord('A'), ord('Z')) + range(ord('a'), ord('z')) + [ord('-'), ord('_')])])
    dr = dict([(d[k], k) for k in d])
    return ''.join([d[eval('0b' + key[i*6:i*6+6])] for i in range(6)])
    
def decrypt_winning_no(locked_winning_no_to_MrX, passwd):
    d = dict([(i,chr(v)) for i,v in enumerate(range(ord('0'), ord('9')) + range(ord('A'), ord('Z')) + range(ord('a'), ord('z')) + [ord('-'), ord('_')])])
    dr = dict([(d[k], k) for k in d])
    dd = ''.join([('000000' + bin(dr[i])[2:])[-6:] for i in passwd])
    return [i+1 for i,v in enumerate(dd) if v == '1']

locked_winning_no_to_MrX = gen_encrypted_winning_no() # give fake encrypted no. to mr. X
print 'locked_winning_no_to_MrX :\n\t', locked_winning_no_to_MrX
key_to_unlock = gen_decrypt_key(locked_winning_no_to_MrX, [1,2,5,6,7,9,12,13,15,16,17,20,21,23,25,26,27,28,29,30,33,36]) # wait for actual winning no. is out and generate fake key
print 'key_to_unlock :\n\t', key_to_unlock
unlocked_winning_no_to_MrX = decrypt_winning_no(locked_winning_no_to_MrX, key_to_unlock) # mr. X uses the fake key to decrypt the fake encrpted no.
print 'unlocked_winning_no_to_MrX :\n\t', unlocked_winning_no_to_MrX

