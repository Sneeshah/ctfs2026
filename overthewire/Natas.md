Found here: https://overthewire.org/wargames/natas/natas0.html

# Natas


## Description:
Natas is aimed at beginners in Web Exploitation. The first couple of levels should be enough to then swap to Port Swigger Academy.


### Level 0 -> 0
#### Username: natas0 Password: natas0 URL: http://natas0.natas.labs.overthewire.org

    -go to the URL
    -log in
    -use the inspector
    -password is in the <body>

The password is: scfWG6qNEIdzqVyfRwEGXyNUfFZkZeQ7
    
### Level 0 -> 1
#### Username: natas1 URL: http://natas1.natas.labs.overthewire.org

    -same way to login
    -can't just rightclick and go into inspector but f12 works, also rightclicking is not blocked on the whole page
    -password hidden in the 'content'-div

 The password is: vsDOxoXyq3wckCP1ZmTZ71ngIA606odB

### Level 1 -> 2
#### Username: natas2 URL: http://natas2.natas.labs.overthewire.org

    -page source shows nothing new
    -there is a png of a pixel though
    -the source of the png is a directory called files
    -the files directory has a users.txt with the password
    -Note: check for leaking of folders through images and other things. -> list every url a page references and poke at them

The password is: K30JrSRHzjxq3paUQuwozY4MNvmNFyhI

### Level 2 -> 3
#### natas3 URL: http://natas3.natas.labs.overthewire.org

    -Seemingly empty page again
    -inside the html it says there will be no more information leaks, not even google will find it this time
    -this sounds like we should look at the robots.txt
    -the robots.txt in turn leaks another directory /s3cr3t/ which holds another user.txt with our password

The password is: JDrPnuZAKyl6MkiqQGFIddrqpvgOASth

### Level 3 -> 4 request forgery
#### natas4 URL: http://natas4.natas.labs.overthewire.org

    -Access disallowed, we need to come from "http://natas5.natas.labs.overthewire.org/" which makes no sense to me
    -Apparently curl can change the referer (firefox could not) with the flag -e
    -curl -u natas4:JDrPnuZAKyl6MkiqQGFIddrqpvgOASth -e http://natas5.natas.labs.overthewire.org/ http://natas4.natas.labs.overthewire.org/index.php/index.php
    -Note: Page says X is not allowed -> can I forge X? In this cas: requests headers are not trustworthy because they are send by the client.

The password is: e4z2Noy3oqwPJUWzJH0dseN67Cn1sy2M


### Level 4 -> 5 request forgery
#### natas5 URL: http://natas5.natas.labs.overthewire.org

    -Not logged in, so no access.
    -looking at the network tab again. Cookie loggedin=0 looks like if we can use curl to set it to 1 this might work
    -curl -u natas5:e4z2Noy3oqwPJUWzJH0dseN67Cn1sy2M -b "loggedin=1" http://natas5.natas.labs.overthewire.org worked
    -Note: Curl is super powerful
    -Note2: server trusting client-controlled data without verification is dangerous

The password is 7mhjtShJAcld2NYbKHEadnhEwRn2P8VT

### Level 5 -> 6
#### natas6 URL: http://natas6.natas.labs.overthewire.org

    -looks like we have to input some kind of password to get our password
    -strongly smells of input injection
    -source code shows the block of code inside <?...?> which means php code and it includes includes/secret.inc
    -Inputting this path into the url gives back the password (FOEIUWGHFEEUHOFUOIU) that we can input
    -Note: php included files extensions other than .php (like .inc .bak .old) can be used for source disclosure by serving them as a raw source instead of exectuing them

The password is: B1szg95UcTnrzwnF3i3TzYHlyYh8iBV0

### Level 6 -> 7 Local File Inclusion
#### natas7 URL: http://natas7.natas.labs.overthewire.org

    -two buttons, one for home page one for about page
    -source code revelas that the password for webuser natas8 is in /etc/natas_webpass/natas8
    -if we change the url to http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8 it returns the password

The password is: ugXL95KQmUAJJj6bMezOlBNDyI9Imwkc

### Level 7 -> 8
#### natas8 URL: http://natas8.natas.labs.overthewire.org

    -same as in Level 5 -> 6 but this time it is encoded
    -encoded string looks like it could be hex encoded and looks like this decoded: ==QcCtmMml1ViV3b
    -seems like a flipped base64 (== is a strong hint)
    -flipped it becomes b3ViV1lmMmtCcQ== and decoded that is oubWYf2kBq which we can input as our passphrase and indeed that gives us the password for the next level. Encoding is not encryption.

The password is: UdxmI27dTaXmnd1rxKQTfws6jihTdcQ9

### Level 8 -> 9 OS command injection
#### natas9 URL: http://natas9.natas.labs.overthewire.org

    -okay nowe we have a dictonary search in front of us
    -we can search for words or letters and letter combinations
    -this is 100% injection
    -since grep is used we can just pipe to a cat command
    - | cat /etc/natas_webpass/natas10 (not cat 9....)reveals the password (the path is the same as in challenge 6 -> 7)
    

The password is: EgjlkzB6E8LJyf2Obt4q7q4ewt5ZWSNv


### Level 9 -> 10 OS command injection + blocklist bypass
#### natas10 URL: http://natas10.natas.labs.overthewire.org

    -same thing but this time we can not use the characters from large challenge (; | &)
    -inputting a combination of other well known "regex signs" works though. Here .* worked
    -.* /etc/natas_webpass/natas11
    -since our input is fed driectly into a grep command this works since the 'dictionary.txt' from the code is just appeneded after the file we inout to grep

The password is: VUMQDmuITOEHzhviLE5V0VG9cPMQkyxd