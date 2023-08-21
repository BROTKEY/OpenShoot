cd .\echoserver\
start "Server" python echoserver.py
cd ..
cd .\track-n-trace\
start "Tracker" python OpenShoot.py
cd ..
cd .\angular-client\
start "Client" npm start