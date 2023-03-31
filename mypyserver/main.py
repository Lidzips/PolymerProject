from neunet_retrain import retrain
from neunet_predict import predict
from data_uploadneunetspecimen import uploadspecimen
import socket
from data_login import login
from data_userhistory import history
from data_newuser import newuser
from neunet_predict import predict
from PIL import Image


HOST = "192.168.100.46"
PORT = 8080
SIZE = 1024
FORMAT = "utf-8"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print("Listening... ")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                action = conn.recv(SIZE)
                
                if not action:
                    break

                action = action.decode().strip()
                print(action)
                print("Command received: " + action)
                print(str(type(action)) + " | " + str(len(action)))
                if (action == "predict"):
                    print("Match")
                else:
                    print("No match")
                match action:
                    case "login":
                        print("Selected case")
                        action += "\r"
                        conn.sendall(action.encode(FORMAT))
                        print("Sent green light")

                        log = conn.recv(SIZE)
                        print("Login var received")
                        log = log.decode().strip()

                        reply = "Login value received\r"
                        conn.sendall(reply.encode(FORMAT))
                        print("Response sent")

                        password = conn.recv(SIZE)
                        print("Password var received")
                        password = password.decode().strip()

                        # reply = "Password value received\r"
                        # conn.sendall(reply.encode(FORMAT))
                        # print("Response sent")

                        result = login(log, password)
                        print("Query queried")

                        if result == 0:
                            reply = "No match\r"
                        elif result == 1:
                            reply = "User\r"
                        elif result == 2:
                            reply = "Admin\r"

                        conn.sendall(reply.encode(FORMAT))
                        print("Response sent")

                    case "predict":  # expects <specimen> as b64 string
                        print("Selected case")
                        action += "\r"
                        conn.sendall(action.encode(FORMAT))
                        print("Sent green light")

                        specimen = ""  # continue
                        no = 0
                        while True:
                            data = conn.recv(SIZE)
                            data = data.decode().strip()
                            print("Got data: " + data + "\nOf length: " + str(len(data)))
                            no += 1
                            print("Data frag " + str(no) + " recieved")
                            specimen += data
                            if (len(data) < SIZE):
                                break

                        specimen = specimen.encode(FORMAT)
                        print("All data gathered")

                        prediction = predict(specimen)  # continue
                        print("Prediction generated")
                        prediction += "\r"

                        conn.sendall(prediction.encode(FORMAT))
                        print("Prediction sent")

                    case "user_db_summary":
                        print("Selected case")
                        action += "\r"
                        conn.sendall(action.encode(FORMAT))
                        print("Sent green light")

                        log = conn.recv(SIZE)
                        print("Login var received")
                        log = log.decode().strip()

                        # reply = "Login value received\r"
                        # conn.sendall(reply.encode(FORMAT))
                        # print("Response sent")

                        result = history(log)  # result contains json dump
                        result += "\r"
                        conn.sendall(result.encode(FORMAT))

                    case "admin_upload_specimen":  # expects to receive two msgs: <label> and <specimen>, latter as b64 string
                        print("Selected case")
                        action += "\r"
                        conn.sendall(action.encode(FORMAT))
                        print("Sent green light")

                        label = conn.recv(SIZE)
                        label = label.decode().strip()
                        print("Label received")

                        reply = "Label recieved\r"
                        conn.sendall(reply.encode(FORMAT))
                        print("Response sent")

                        specimen = ""
                        no = 0
                        while True:
                            data = conn.recv(SIZE)
                            data = data.decode().strip()
                            print("Got data: " + data + "\nOf length: " + str(len(data)))
                            no += 1
                            print("Data frag " + str(no) + " recieved")
                            specimen += data
                            if (len(data) < SIZE):
                                break
                        specimen = specimen.encode(FORMAT)
                        print("All data gathered")
                        uploadspecimen(specimen, label)
                        print("Sending response")
                        reply = "Speciment upload success\r"
                        conn.sendall(reply.encode(FORMAT))
                    
                    case "admin_db_query": #---------------------------v-v-TODO-v-v--------------------------
                        data = conn.recv(SIZE)
                        
                    case "test":
                        print("Selected case")
                        action = action + "\r"
                        print(str(type(action)) + " | " + str(len(action)))
                        print(action)
                        conn.sendall(action.encode(FORMAT))
                        print("green light")
                        data = conn.recv(SIZE).decode().strip()
                        print("Msg 2 received")
                        conn.sendall(data.encode(FORMAT))
                        print("Response sent")

                    case "admin_retrain_neunet":
                        print("Selected case")
                        action += "\r"
                        conn.sendall(action.encode(FORMAT))
                        print("Sent green light")

                        batches = conn.recv(SIZE)
                        print("Batch var received")
                        batches = batches.decode().strip()

                        reply = "Batch value received\r"
                        conn.sendall(reply.encode(FORMAT))
                        print("Response sent")

                        epochs = conn.recv(SIZE)
                        print("Epoch var received")
                        epochs = epochs.decode().strip()

                        reply = "Epoch value received\r"
                        conn.sendall(reply.encode(FORMAT))
                        print("Response sent")

                        layers = conn.recv(SIZE)
                        print("Layers var received")
                        layers = layers.decode().strip()
                        layers = layers.replace("[", "")
                        layers = layers.replace("]", "")
                        layers = layers.split(", ")

                        arr_layers = [int(i) for i in layers]

                        # reply = "Layer values received\r"
                        # conn.sendall(reply.encode(FORMAT))
                        # print("Response sent")

                        retrain(int(batches), int(epochs), arr_layers)

                        reply = "NeuNet retrained successfully\r"
                        conn.sendall(reply.encode(FORMAT))

                    case "new_acct":
                        print("Selected case")
                        action += "\r"
                        conn.sendall(action.encode(FORMAT))
                        print("Sent green light")

                        login = conn.recv(SIZE)
                        print("Login var received")
                        login = login.decode().strip()

                        reply = "Login value received\r"
                        conn.sendall(reply.encode(FORMAT))
                        print("Response sent")

                        password = conn.recv(SIZE)
                        print("Password var received")
                        password = password.decode().strip()

                        # reply = "Password value received\r"
                        # conn.sendall(reply.encode(FORMAT))
                        # print("Response sent")

                        result = newuser(login, password)
                        print("Query queried")

                        if result is False:
                            reply = "Login taken\r"
                        else:
                            reply = "User created\r"

                        conn.sendall(reply.encode(FORMAT))
                        print("Response sent")
