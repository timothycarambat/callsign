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
beacuse this is such a simple app - no automated table generation is happening here (feel free to add it as deploy script!)
- id (int) Autoincrement
- user (text) NOT NULL
- data (text) NULLABLE -> this will store a JSON string as the version of MariaDB I was using didn't support JSON Objects and its such a simple structure.

### Setup
Be sure you have a `.env` file in the same directory as the `callsign.py` script. That file will contain all the proper keys and other unique deployment attributes.

Since its running on an EC2 instance for me:
- make sure Python Version is good
- install requiremnts.txt
- setup .env
- run  `export $(cat .env | xargs)`
- check .env was exported properly to env vars
- then run as daemon `python callsign.py > output.log &`
- check bot is up and running!
