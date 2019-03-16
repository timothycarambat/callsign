# CALLSIGN
##### A DISCORD BOT

### What is This?
This is a bot that you would deploy either locally or on AWS. This bot allows everyone in the server to keep track of and see other people aliases for other games or services. For example, a multi game clan could keep track and see what other members names are in different games - as most users have different or changing usernames depending on the game.

This bot currently supports the following commands. These commands run updating information for the user that executes it. You cannot add a callsign for another user.
`help` - Shows the help menu `@BotName help`
`add` - add or update the callsign for a game `@BotName add Vengance64 : PUBG`
`remove` - remove callsign for a game `@BotName remove PUBG`

Of course there is a lookup function as well:
`@BotName @UserOfInterest`

### Dependencies
- Python 3.6.6
- [pip pkg] discord.py
- [pip pkg] dotenv
- [pip pkg] pymysql
- MYSQL

### DB Schema
beacuse this is sucha  simple app - no automated table generation is happening here (feel free to add it as deploy script!)
- id (int) Autoincrement
- user (text) NOT NULL
- data (text) NULLABLE -> this will store a JSON string as the version of MariaDB I was using didnt support JSON Objects and its such a simple strucutre.

### Setup
Be sure you have a `.env` file in the same directory as the `callsign.py` script. That fille will contain all the proper keys and other uniqure deployment attributes.
