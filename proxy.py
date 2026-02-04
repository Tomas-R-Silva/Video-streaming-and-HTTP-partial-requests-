import sys
import requests
import threading
import socket
import queue


def main():
    HOST = "localhost"
    PORT = "8000"
    q = queue.Queue()
    baseURL = sys.argv[1].rstrip('/')
    movieName = sys.argv[2]
    track = sys.argv[3]

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST, int(PORT)))

    producerThread = threading.Thread(target = producer, args=(baseURL, movieName, track, q))
    consumerThread = threading.Thread(target=consumer, args=(q, connection))

    producerThread.start()
    consumerThread.start()

    producerThread.join()
    consumerThread.join()

    connection.close()

def producer(baseURL, movieName, trackIndex, q):
    manifestURL = baseURL + '/' + "movies/" +movieName + '/manifest.txt'
    #print(manifestURL)
    r = requests.get(manifestURL) 
    manifestoInfo = r.text # obtêm informação do manifest
    lines = manifestoInfo.splitlines(); # fica um array com a informação toda

    trackName = movieName + "-" + str(trackIndex) + ".mp4"
    trackURL = baseURL + "/" + "movies" + "/" + movieName + "/" +trackName
    #print(trackURL)
    #print(trackName)

    idx = 0
    while(lines[idx] != trackName):
        idx = idx +1
    
    nrSegThisTrack = int(lines[idx + 4])
    firstSegLine = idx +5

    for i in range(nrSegThisTrack):
        SegLine = lines[firstSegLine + i]
        SegPart = SegLine.split()
        SegOffSet = int(SegPart[0])
        SegBytes = int(SegPart[1])

        headers = {"Range": f"bytes={SegOffSet}-{SegOffSet + SegBytes - 1}"}
        r = requests.get(trackURL, headers=headers)

        q.put(r.content)
    
    q.put(None)




def consumer(q, connection):
    while True :
        
        segment = q.get()
        if segment is None:
           break
        
        connection.sendall(segment)
        q.task_done()
    connection.close()



main()

