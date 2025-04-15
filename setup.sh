cat `pwd`/env_tg_bot.service > /etc/systemd/system/env_tg_bot.service
sudo systemctl daemon-reload
sudo systemctl enable env_tg_bot
mkdir -p src/data
touch src/config.py src/data/facts.txt src/data/{buildings,metall,caps,battaries,plastic}.csv

