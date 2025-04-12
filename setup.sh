cat env_tg_bot.service > /lib/systemd/system/env_tg_bot.service
systemctl daemon-reload
systemctl enable env_tg_bot
mkdir -p src/data
touch src/config.py src/data/places.txt src/data/facts.txt

