sudo cp iottly-device-agent.service /lib/systemd/system/iottly-device-agent.service
sudo chmod 644 /lib/systemd/system/iottly-device-agent.service
sudo systemctl daemon-reload
sudo systemctl enable iottly-device-agent.service

