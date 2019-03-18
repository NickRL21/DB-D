# ******************************************************************
# Name:         README.txt
# Date:         March 17, 2019
# Description:  A README for running the CLI and communicating with the API.
# ******************************************************************

For using the CLI, you need to have python3 installed along with the requests package (In pip).
You can run the client by:  Python3 DBnD_Client.py

You can use the (DCI = 2521489631) and (password = password) in order to login to the system.

To use the api you need to pass a basic auth header with the username and password. I suggest using postman to do this found at https://www.getpostman.com/


API DOCUMENTATION
current base api endpoint: https://unthgdgw0h.execute-api.us-east-1.amazonaws.com/dev

REGISTER
POST on /register
basic auth username:password
username = dci_number
url params: name

AUTH REQUIRED FOR ALL ENDPOINTS BELOW

PLAYER
GET on /player
purpose: gets player dci_number, p_name


CHARACTER
GET on /character
url params: character_name
purpose: get a character by name

Get on /character/<char_name>
purpose: gets a character by name

POST on /character/<char_name>
url params: character_name
body like: { "race": "char_race",
  	     "class": "char_class",
             "background": "char_background",
             "level": "char_level"
           }
purpose: create a character

PUT on /character/<char_name>
url params: character_name
body like: { "race": "char_race",
  	     "class": "char_class",
             "background": "char_background",
             "level": "char_level"
           }
purpose: update a character

ADVENTURE_LOGS
GET on /character/<char_name>/adventure_logs
url params: character_name
purpose: get all adventure logs for a character sorted by date

POST on /character/<char_name>/adventure_logs
url params: character_name
body like:
{
	"adventure_name": "test_adventure",
	"a_date": "1921-03-24",
	"delta_downtime": 4,
	"delta_tcp_t1" : 3,
	"delta_tcp_t2" : 1,
	"delta_tcp_t3" : 7,
	"delta_tcp_t4" : 4,
	"delta_gold": 5,
	"delta_acp": 2,
	"delta_renown": 1,
	"dm_dci": "1234567891"
}
if date left null or omited, todays date will be used

DOWNTIME_LOGS

GET /character/<char_name>/downtime_logs
url params: character_name
purpose: get all downtime logs for a character sorted by date

POST /character/<char_name>/downtime_logs
url params: character_name
body like:
{
	"dt_date": "1922-03-24",
	"delta_downtime": 4,
	"delta_tcp_t1" : 3,
	"delta_tcp_t2" : 1,
	"delta_tcp_t3" : 7,
	"delta_tcp_t4" : 4,
	"delta_gold": 5,
	"delta_acp": 2,
	"delta_renown": 1
}

if date left null or omited, todays date will be used

LOGS
GET on /character/<char_name>/logs
url params: character_name
purpose: get all downtime and adventure logs for a player ordered by date

PROGRESSION
GET on /character/<char_name>/progression
url params: character_name

MAGICAL_ITEMS
GET on /magic_items/<char_name>
url params: character_name
purpose: gets all magical items for a character

POST on /magic_items/<char_name>
url params: character_name
purpose: add a new magical item

body like: {
	"item_name": "glowing bucket",
	"quantity": 3,
	"date_acquired": "2018-09-21"
}
