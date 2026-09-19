list_string = """123456
password
12345678
qwerty
123456789
12345
1234
111111
1234567
dragon
123123
baseball
abc123
football
monkey
letmein
shadow
master
666666
qwertyuiop
123321
mustang
1234567890
michael
654321
superman
1qaz2wsx
7777777
121212
000000
qazwsx
123qwe
killer
trustno1
jordan
jennifer
zxcvbnm
asdfgh
hunter
buster
soccer
harley
batman
andrew
tigger
sunshine
iloveyou
2000
charlie
robert
thomas
hockey
ranger
daniel
starwars
klaster
112233
george
computer
michelle
jessica
pepper
1111
zxcvbn
555555
11111111
131313
freedom
777777
pass
maggie
159753
aaaaaa
ginger
princess
joshua
cheese
amanda
summer
love
ashley
nicole
chelsea
biteme
matthew
access
yankees
987654321
dallas
austin
thunder
taylor
matrix
mobilemail
mom
monitor
monitoring
montana
moon
moscow"""


usernames = """carlos\n"""*100   ## creates the carlos username string

## split both strings into dictonaries
splitted = list_string.split()                  
splitted_users = usernames.split()

# ## go through the dictionaries and insert peter / wiener after every 2 entries
# for i in range(len(splitted)+50):
#     if (i+1)%3 == 0:
#         splitted.insert(i, 'peter')
#         splitted_users.insert(i,'wiener')


# ## transform back to original format for easy copy and baste into intruder
# final_users = "\n".join(splitted_users)
# final_password = "\n".join(splitted)

# ## simple print
# print(final_users)
# print('\n\n\n\n------------------------\n\n\n\n\n')
# print(final_password)




password_chunks = [splitted[i:i+2:1] + ['peter'] for i in range(0,len(splitted), 2)]

password_list = [   ## think of this: for sentence in text for word in sentence and place element in the last for (like an append)
    element
    for sublist in password_chunks
        for element in sublist
]


user_chunks = [splitted_users[i:i+2:1] + ['wiener'] for i in range(0,len(splitted_users), 2)]

username_list = [   ## think of this: for sentence in text for word in sentence and place element in the last for (like an append)
    element
    for sublist in user_chunks
        for element in sublist
]

final_users = "\n".join(username_list)
final_password = "\n".join(password_list)

## simple print
print(final_users)
print('\n\n\n\n------------------------\n\n\n\n\n')
print(final_password)