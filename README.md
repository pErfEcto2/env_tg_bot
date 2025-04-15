# env_tg_bot

## Installation
1) `git clone https://github.com/pErfEcto2/env_tg_bot.git && cd env_tg_bot`
2) `pip3 -r requirements.txt`
3) `chmod 755 run.sh`
4) `chmod 755 setup.sh`
5) `./setup.sh`
6) add facts to the `src/data/facts.txt` (separated by newline)
7) fill the buildings.csv, metal.csv, plastic.csv, metall.csv and battaries.csv with neccessary places (buildings.csv format: id, address; other files: id, description, address)

## Run
1) Put in the `src/config.py` API_KEY, FACTS_FILE_PATH, DB_NAME, SECRET_PASSWORD and MONITOR_CHAT_ID 
2) `systemctl start env_tg_bot.service`

