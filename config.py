config_api_key = "hlelr8uiebs37NgfwM"
config_api_key_secret = "bL38f19z7aT1fD573tbsxyHrTZWnzAdb88kC"
account_type = "CONTRACT"

"""
NOTES: It will use the default leverage set on the token pair you want to trade
so if theres not enough margin it will throw an error and not make the trade

- Need to make it so that the program is able to read the api keys in from a spreadsheet and then
make trades across all accounts that selectedd that token, so we can update without stoppping the program

- make it so that if a shut down were to occur that, whether the position on each token is 
open or closed is known and that it imeadiately starts on reboot and goes back to that state

- web ui that would interact with the database that would interact with the programe

- Indicating when a trade is made by sending out a broadcast email




config_api_key = "jmQAITS8HZuJnuYnp3"
config_api_key_secret = "21BlzjQp6HLrdr4SOpre20YCrLmdxMsMUvsf"
account_type = "CONTRACT"

"""