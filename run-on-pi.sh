scp *.py pi@192.168.1.110:chess
ssh pi@192.168.1.110 'cd chess; sudo python chesstimer.py'
