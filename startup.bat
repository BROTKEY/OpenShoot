cd .\echoserver\
start "Server" python3.11 echoserver.py
cd ..
cd .\track-n-trace\
start "Tracker" python3.11 OpenShoot.py
cd ..
cd .\angular-client\
start "Client" npm start