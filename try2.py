from icmplib import ping
from threading import Thread
from queue import Queue
import csv

def main():
    a,b,c,d=127,0,0,0
    que = Queue()
    count= 0
    done = False

    def asyncPing(a1,b1,c1,d1,count1,q ):
        if ping(f"{a1}.{b1}.{c1}.{d1}", interval=0.001, id = count1).is_alive: q.put(f"{a1}.{b1}.{c1}.{d1}")

    def readQueue(q):
        with open("internet.csv", "w",newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Address"])
            while not done or not q.empty():
                try:  address = q.get_nowait();writer.writerow([address])
                except: pass

    Thread(target = readQueue,  args = (que,)).start()
    while c!=1:
        Thread(target = asyncPing, args = (a,b,c,d,count,que)).start()
        count,d=count+1,d+1
        if d == 256: c+=1;d=0
        if c == 256: b+=1;c,d=0,0
        if b == 256: a+=1;b,c,d=0,0,0
    done  = True

if __name__ == "__main__":
    main()
