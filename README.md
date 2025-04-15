# env_tg_bot

## Installation
1) `git clone https://github.com/pErfEcto2/env_tg_bot.git && cd env_tg_bot`
2) `pip3 -r requirements.txt`
3) `chmod 755 run.sh`
4) `chmod 755 setup.sh`
5) add to the table "buildings" in the users.db neccessary places
6) `./setup.sh`
7) add facts to the `src/data/facts.txt` (separated by newline)

## Run
1) Put in the `src/config.py` API_KEY, PLACES_FILE_PATH, FACTS_FILE_PATH, DB_NAME, SECRET_PASSWORD and MONITOR_CHAT_ID 
2) `systemctl start env_tg_bot.service`
