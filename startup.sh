ipfs init
nohup ipfs daemon &
gunicorn server:app -b 0.0.0.0:5000 -t 0
