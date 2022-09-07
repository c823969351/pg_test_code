#start pytest -vs .\test_M695_1.py --count=5000  --repeat-scope=session 
#start pytest -vs .\test_M695_2.py --count=5000  --repeat-scope=session 
start pytest -vs test_ON-OFF1.py --count=10000 --repeat-scope=session 
start pytest -vs test_ON-OFF2.py --count=10000 --repeat-scope=session 