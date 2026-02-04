import sys
import requests

serverURL = sys.argv[1]
movieName = sys.argv[2]
endFileName = sys.argv[3]

manifestURL = serverURL + '/' + movieName + '/manifest.txt'

r = requests.get(manifestURL) 
manifestoInfo = r.text # obtêm informação do manifest
lines = manifestoInfo.splitlines(); # fica um array com a informação toda

nrTracks = lines[1]
nrSegments = int(nrTracks) * 50


i =2; # para dar skip daquela informação de cima
with open(endFileName, "w") as file:
    file.write(nrTracks + "\n")
    file.write(str(nrSegments) + "\n")
               
    for j in range(5):
        bytesOfTrack = 0
        i = i+4 # dá skip do header dos tracks

        nrSegThisTrack = int(lines[i])
        i = i+1

        for h in range(int(nrSegThisTrack)):
            SegLine = lines[i]
            i = i+1
            SegPart = SegLine.split()
            SegBytes = SegPart[1]
            bytesOfTrack = int(SegBytes) + bytesOfTrack
        file.write(str(bytesOfTrack) + "\n")
    








