import cv2
import requests
import numpy as np
from datetime import datetime
import os
import glob


def delete_data(path):
    """function deletes data library"""
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)


def record_video(length_secs, path_to_stream, path_to_wd, path_to_data):
    """function records video from <stream> of length <length_secs>"""

    r = requests.get(path_to_stream, stream=True)
    if r.status_code == 200:
        bytes_loc = bytes()
        time_start = datetime.now()
        for chunk in r.iter_content(chunk_size=1024):
            bytes_loc += chunk
            a = bytes_loc.find(b'\xff\xd8')  # JPEG start
            b = bytes_loc.find(b'\xff\xd9')  # JPEG end
            if a != -1 and b != -1:
                jpg = bytes_loc[a:b+2]  # actual image
                bytes_loc = bytes_loc[b+2:]  # other information
                # decode to colored image ( another option is cv2.IMREAD_GRAYSCALE)
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                datetimeobj = datetime.now()  # get time stamp
                cv2.imshow('img', i)
                cv2.imwrite(path_to_wd + path_to_data + '/img' + str(datetimeobj) + '.jpg', i)
                if cv2.waitKey(1) == 27 or (datetimeobj -time_start).seconds > length_secs:  # if user  hit esc
                    exit(0)  # exit program
    else:
        print("Received unexpected status code {}".format(r.status_code))


#record_video(30)


def main():

    # set parameters
    path_to_stream = 'http://192.168.11.115:8080/?action=streaming'
    path_to_data_directory = '/data'
    dir_path = os.path.dirname(os.path.realpath(__file__))

    delete_data(dir_path + path_to_data_directory)
    record_video(30, path_to_stream, dir_path, path_to_data_directory)

    return 0


if __name__ == "__main__":

    main()
