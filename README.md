##Summary

This is a simple Python script that creates a bot that listens to activity on an IRC channel and logs it to a file.

##Arguments

###-server

DNS address of the IRC Server. It defaults to irc.freenode.net.

###-port

Port number of the IRC Server. It defaults to 6667.

###-channel

Channel to join. It defaults to #linux.

###-name

The name to use for the bot. It defaults to 'Mandalorian.'

###-output

File to write the log to. It defaults to stdout.

##Usage
Connect to 'irc.frenode.net' using the nickname 'l33tbot,' join the #ubuntu channel, and log to 'ubuntu.txt':

```python IRCBot.py -c '#ubuntu' -n 'l33tbot' -o 'ubuntu.txt'```
