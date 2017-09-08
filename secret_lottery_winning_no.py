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
from Crypto.Cipher import AES

gen_encrypted_winning_no    = lambda    : ''.join([chr(randint(48,90)) for _ in range(32)])
gen_decrypt_key             = lambda e,n: AES.new(e).encrypt(n.ljust(((len(n)-1)/16+1)*16))
decrypt_winning_no          = lambda e,k: AES.new(e).decrypt(k).strip()

locked_winning_no_to_MrX = gen_encrypted_winning_no() # give fake encrypted no. to mr. X
print 'locked_winning_no_to_MrX :\n\t', locked_winning_no_to_MrX

key_to_unlock = gen_decrypt_key(locked_winning_no_to_MrX, '12,3,4,9,20') # wait for actual winning no. is out and generate fake key
print 'key_to_unlock :\n\t', ''.join([hex(ord(o))[2:] for o in key_to_unlock])

unlocked_winning_no_to_MrX = decrypt_winning_no(locked_winning_no_to_MrX, key_to_unlock) # mr. X uses the fake key to decrypt the fake encrpted no.
print 'unlocked_winning_no_to_MrX :\n\t', unlocked_winning_no_to_MrX

# print (lambda **_:_.keys()[0])(locked_winning_no_to_MrX=0), ':\n\t', locked_winning_no_to_MrX
# print (lambda **_:_.keys()[0])(key_to_unlock=0),               ':\n\t', ''.join([hex(ord(o))[2:] for o in key_to_unlock])
# print (lambda **_:_.keys()[0])(unlocked_winning_no_to_MrX=0),  ':\n\t', unlocked_winning_no_to_MrX
