from os import listdir as ls

import re
import requests

import face_recognition

# image = face_recognition.load_image_file('adam.jpg')
# encoding=face_recognition.face_encodings(image)
# print(type(encoding))
# print(encoding)

# from queue import *
# import threading
# import time

# import csv

# from multiprocessing.dummy import Pool  # This is a thread-based Pool
# from multiprocessing import cpu_count
known=[]
# f = open('out.txt','w')
def batchEncoding(images):
    # print(images)


    image = face_recognition.load_image_file("recognition/"+images)
    encoding=face_recognition.face_encodings(image)[0]
    # print(str(image))
    known.append(encoding)
    # print(type(encoding),known)
    return encoding


# if __name__ == "__main__":
#   # fileName = "SomeSiteValidURLs.csv"
#   pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
#   # with open(FileName, "rb") as f:
#   array_of_image = [x for x in ls() if x[-4:]==(".jpg")]
#   # print(array_of_text)
#   # theurls=array_of_text[:3000]
#   # theurls = ["1.jpg", "2.jpg","3.jpg","4.jpg","adam.jpg","adam1.jpg","anoop.jpg","ponnu.jpg"]
#   results = pool.map(batchEncoding, array_of_image)
#   # results is a list of all the placeHolder lists returned from each call to crawlToCSV
#   # print(results)
#     # pool.start()
#   # pool.start()
#   print(results[0][0])
#   # with open("Output.csv", "ab") as f:
#   #     writeFile = csv.writer(f)
#   # for result in results:
#   #     f.write(' '.join(str(line) for line in result[0].tolist())+'\n')
def recog_face(image_name):
    known[:] = []
    # dict={}
    # print(image_name)
    path = "./recognition"
    array_of_image = [x for x in ls(path) if x[-4:]==(".jpg")]
    print(array_of_image)
    for item in array_of_image:
        # print(item)
        try:
            dict[item]=batchEncoding(item)
        except:
            pass
    file_ = 'images/'+image_name
    unknown_image = face_recognition.load_image_file(file_)
    try:
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        print(unknown_face_encoding)
    except IndexError:
        name = "Face not found"
        return name
    results = face_recognition.compare_faces(known, unknown_face_encoding, tolerance=0.5)

# if True in results:
#   print(in)
    print (results)
    try:

        name=array_of_image[results.index(True)]
        name=name[:-4]
    except ValueError:
        name = "Unknown Face"
        print(name)
        return name
    print(name)
    sentence = "This is "+name
    r = requests.post("http://www.iitm.ac.in/donlab/hts/festival_cs.php", data={'op':sentence, 'Languages':'englishm',  'ex':'execute', 'ip':''})
    m = re.search('(\d+).wav', r.text)
    print (m.group(1))
    url = "http://www.iitm.ac.in/donlab/hts/wav_output/hts_out"+m.group(1)+".wav"
    return url
# print(dict)
# for key, value in dict.items():
#   print(key)
# # print(type(dict['arun1.jpg']))