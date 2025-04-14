# env_tg_bot

## Installation
1) `git clone https://github.com/pErfEcto2/env_tg_bot.git && cd env_tg_bot`
2) `pip3 -r requirements.txt`
3) `chmod 755 run.sh`
4) `chmod 755 setup.sh`
5) add to the table "waste_collection_points" in the users.db 
5) `./setup.sh`

## Run
1) Put in the `src/config.py` API_KEY, PLACES_FILE_PATH, FACTS_FILE_PATH, DB_NAME, SECRET_PASSWORD and MONITOR_CHAT_ID 
2) `systemctl start env_tg_bot.service`
