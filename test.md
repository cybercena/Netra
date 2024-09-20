---
title: "NCA CTF: The Astley’s Secret"
date: 2024-09-20
draft: false
Tags:
- CTF
- CSAW
- Forensics
- Crypto
---


Here’s the markdown version of your text with a dummy image link:

```markdown
# Hello, Everyone!

Recently, I joined a cybersecurity community called **NCA@Nepal**, which aims to train people and build a cyber army with strong hacking knowledge. The classes are highly interactive and informative. We learn various topics from mentors and explore new techniques daily by solving picoCTFs and custom-made CTFs created by members of NCA@Nepal.

## The Astley’s Secret

In the challenge mentioned above, the creator provided a music file named `nca_ctf.mp3`. I opened the file, thinking it might contain Morse code, but to my surprise, it turned out to be the popular Rick Roll meme.

I then tried using `binwalk` with the command:

```bash
binwalk nca_ctf.mp3
```

and discovered that something was hidden inside the file. Next, I attempted to unzip `nca_ctf.mp3`, but it asked for a password. I guessed `rickroll`, and it worked.

There was nothing special in the images, so I tried unzipping the file again, but it asked for another password. I examined the strings in the image using the command:

```bash
strings sir_rick.jpg
```

and found something interesting. After entering the password, I extracted two files: `flag_or_key.txt` and `flag.txt`. I read the `flag.txt` file using the `cat` command and identified the flag format. Then, I read `flag_or_key.txt` and found Morse code inside.

I copied the Morse code and used **CyberChef** to decode it, but initially made no progress, only getting hex format data. I then decrypted the hex data, which gave me base-64 data.

I decrypted the base-64 data and obtained binary data. After decrypting the binary data, I got normal text, which seemed to be the key for the flag.

Remember, we have encrypted text in the `flag.txt` file. Now, with both the encrypted text and the key, and knowing the key is encrypted using the Vigenère cipher, I used **CyberChef**. I entered the encrypted text and the key, and finally, the flag was revealed:

```
NCA{bruhh_you_got_rick_rolled}
```

To play CTF and learn cybersecurity, join the Discord server of **NCA@Nepal**.

[Discord Server](https://discord.gg/KDuvkJHh3D)

![Image](https://via.placeholder.com/150)
```

Let me know if you need any more changes!
