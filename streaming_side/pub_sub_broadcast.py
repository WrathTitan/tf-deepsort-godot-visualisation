"""pub_sub_broadcast.py -- broadcast OpenCV stream using PUB SUB."""

import sys
import socket
import traceback
import datazmq
import random
import json

if __name__ == "__main__":
    # Publish on port
    port = 5555
    sender = datazmq.JSONSender("tcp://*:{}".format(port), REQ_REP=False)
    print("Ready to broadcast")


    # Send hostname with each json data
    # This might be unnecessary in this pub sub mode, as the receiver will
    #    already need to know our address and can therefore distinguish streams
    # Keeping it anyway in case you wanna send a meaningful tag or something
    #    (or have a many to many setup)
    rpi_name = socket.gethostname()

    try:
        counter = 0
        while True:
            json_data = {
                "bounding_box":[random.randint(1,9), random.randint(0,4),random.randint(4,10)],
                "class":random.randint(0,4)
            }
            # frame = capture.read()
            # ret_code, jpg_buffer = cv2.imencode(
            #     ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            # sender.send_jpg(rpi_name, jpg_buffer)
            sender.send_data(rpi_name,json.dumps(json_data))
            print("Sent data {}".format(counter))
            counter = counter + 1
    except (KeyboardInterrupt, SystemExit):
        print('Exit due to keyboard interrupt')
    except Exception as ex:
        print('Python error with no Exception handler:')
        print('Traceback error:', ex)
        traceback.print_exc()
    finally:
        # capture.stop()
        sender.close()
        sys.exit()