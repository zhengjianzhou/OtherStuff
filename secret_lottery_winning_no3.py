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
    Assuming the lottery is a set of 5 numbers in range [1..32]
'''

### SOLUTION:
import string, random
UNIT, MAX_NO, NDIGIT, NCODE = 6, 32, 3, 18
asciid = dict(enumerate(string.ascii_letters + string.digits + '-_'))
asciidr = dict(map(reversed, asciid.items()))
keydr = dict(enumerate([(i+1,j+1,k+1,l+1,m+1) for i in range(MAX_NO-4) for j in range(i+1, MAX_NO-3) for k in range(j+1, MAX_NO-2) for l in range(k+1, MAX_NO-1) for m in range(l+1, MAX_NO)]))
keyd = dict(map(reversed, keydr.items()))

# encoder, decoder
encode = lambda d: ('0'*NCODE+bin(keyd[d])[2:])[-NCODE:]
decode = lambda p: eval('0b'+''.join([('0'*UNIT+bin(asciidr[i])[2:])[-UNIT:] for i in p]))

# main logic
gen_encrypted_winning_no = lambda : ''.join(random.sample(string.ascii_letters*64,64))
gen_decrypt_key = lambda _, data : ''.join([asciid[eval('0b'+encode(data)[i*UNIT:(i+1)*UNIT])] for i in range(NDIGIT)])
decrypt_winning_no = lambda _, passwd: keydr[decode(passwd)]

### USE CASE:
# give fake encrypted no. to mr. X
locked_winning_no_to_MrX = gen_encrypted_winning_no()
print 'locked_winning_no_to_MrX :\n\t', locked_winning_no_to_MrX

# wait for actual winning no. is out and generate fake key
WINNING_NO = (3,11,12,27,31)
key_to_unlock = gen_decrypt_key(locked_winning_no_to_MrX, WINNING_NO)
print 'key_to_unlock :\n\t', key_to_unlock

# mr. X uses the fake key to decrypt the fake encrpted no.
unlocked_winning_no_to_MrX = decrypt_winning_no(locked_winning_no_to_MrX, key_to_unlock)
print 'unlocked_winning_no_to_MrX :\n\t', unlocked_winning_no_to_MrX

### OUTPUT:
'''
locked_winning_no_to_MrX :
	KCpmAZDzCtXExsVIcAkvMsItwbUMkcUxeQQkjYZtVHPGjzeDlEsveioNVtLeSfHJ
key_to_unlock :
	sBC
unlocked_winning_no_to_MrX :
	(3, 11, 12, 27, 31)
'''
