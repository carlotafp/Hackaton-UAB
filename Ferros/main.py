# main.py
from multiprocessing import Process
import api_access
import Troba_tren

if __name__ == "__main__":
    process1 = Process(target=api_access.main)
    process2 = Process(target=Troba_tren.troba_tren)
    
    process1.start()
    process2.start()
    
    process1.join()
    process2.join()
