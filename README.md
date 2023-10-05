# Discord Bot - JugoBot
_As part of the university course unit "Professional Development" to create and manage a group project, in which we selected the "Discord Bot" project brief._

Our aim was to create a multi-purpose Discord bot, **JugoBot**, with various functions that we split amongst our team of 4.

![image](https://github.com/M1nhnho/JugoBot-Discord-Bot/assets/81564712/d0add6c7-6816-4e9b-b2ca-545b9fd9310f)

※ As of October 2023, **JugoBot** is partially outdated so total functionality may not work 100% or may appear slightly incorrect. However, a few fixes have been applied specifically to `trivia` and `charades`.

_Made with Python using discord.py._

## My Contributions
### Trivia
![image](https://github.com/M1nhnho/JugoBot-Discord-Bot/assets/81564712/d29b3900-7f8b-40e2-9c52-3ce080d2cac9)
![image](https://github.com/M1nhnho/JugoBot-Discord-Bot/assets/81564712/ff63e10b-d3a9-4b22-94c6-2b44e9243da1)

An extensive trivia function with customisability. At its core, a user can invite others to a trivia game to which they can join by reacting to the invite message. By default, players are given 15 seconds to answer with first to type the answer - first to 3 wins the trivia game. The time given to answer and correct answers to win can be edited through the `settings` subcommand.

When **JugoBot** first joins the server, there will be no trivia lists to play from as the collection of trivia lists are per server. Recommended to use the `copy` subcommand to copy a trivia list from **JugoBot**'s collection to the server's collection.

Alternatively, one can `add` their own custom trivia list as they are simply text files.
![image](https://github.com/M1nhnho/JugoBot-Discord-Bot/assets/81564712/5e78a529-d547-461f-8e6e-7a85fabe28b1)

As collections are per server, this allows for more private trivia lists as they will only belong to the server's collection they were added to. One can `delete` them any time from the server's collection. Moreover, to edit a trivia list, one would need to `download` it to edit the text file and then re-add with the same name to overwrite the old trivia list.

### Leaderboard
![image](https://github.com/M1nhnho/JugoBot-Discord-Bot/assets/81564712/1c103f38-33b0-4a5b-8629-4599cd570607)

A leaderboard function to encourage competition between the users in a server. When playing any minigame with at least 2 players, the winner will gain points and the remaining losers losing points. These points then can be viewed per minigame or as an overall total through the server leaderboards. Note that there are no global leaderboards as they felt unfitting as minigames are only played between users in the same server.

### Miscellaneous

Assisted the others with their respective functions and ensured consistency between the functions in terms of appearance and format.
