import sys
import requests 
import time

start = time.time()


serverURL = sys.argv[1]
movieName = sys.argv[2]
endFileName = sys.argv[3]

manifestURL = serverURL + '/' + movieName + '/manifest.txt'

r1 = requests.get(manifestURL) 
manifestoInfo = r1.text 
lines = manifestoInfo.splitlines()
nrTracks = int(lines[1])
i = 2

with open(endFileName , "w") as resultFile:
    for h in range(nrTracks):

        bytesOfTrack = 0
        trackName = lines[i] # coco-1.mp4
        nrSegThisTrack = int(lines[i+4])

        idxSeg = i + 5

        trackURL = serverURL + '/' + movieName + '/' + trackName

        with open(trackName, "wb") as movieFile:
            start = time.time()

            for h in range(nrSegThisTrack):
                SegLine = lines[idxSeg + h]
                SegPart = SegLine.split()

                SegOffSet = int(SegPart[0])
                SegBytes = int(SegPart[1])

                bytesOfTrack = bytesOfTrack + SegBytes

                headers = {"Range": f"bytes={SegOffSet}-{SegOffSet + SegBytes - 1}"}
                r = requests.get(trackURL, headers=headers)

                movieFile.write(r.content)

            end = time.time()

        downloadTime = end - start
        downloadRate = bytesOfTrack / downloadTime

        resultFile.write(str(downloadTime) + '\n')
        resultFile.write(str(downloadRate) + '\n')

        
        i = i + 5 + nrSegThisTrack # avança para o próximo track







