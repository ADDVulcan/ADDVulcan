#!/usr/bin/env python3

import pandas as pd
import socket
import stars_improved
import numpy as np
from angle import angle_between

HOST = "myspace.satellitesabove.me"
PORT = 5016
TICKET = 'ticket{golf97715papa:___a bunch of unguessable stuff___}'


def send_cmd(sock, cmd):
    cmd += "\n"
    sock.sendall(cmd.encode("utf-8"))

def wait_for_resp(sock, text, debug=True):
    data = ""
    while True:
        partial_data = sock.recv(1024).decode("utf-8")
        if len(partial_data) == 0:
            raise IOError("I think we got disconnected")
        data += partial_data
        if debug:
            print(data)

        if text in data:
            return data

# SAY HI
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting...")
server.connect((HOST, PORT))
print("Connected.")
wait_for_resp(server, "Ticket please", debug=False)
send_cmd(server, TICKET)  # send ticket

iteration = 0
while True:
    data = ''
    while 'Guesses' not in data:
        data += server.recv(2024).decode("utf-8")  # rcv data

    # PARSE INCOMING DATA
    data = data.replace('\t', '')  # remove tabs
    data = data.split('\n\n')[0]  # truncate chars after strings
    data = data.splitlines()  # split into list
    # print(data)
    cleaned_data = []
    for line in data:
        # list comp would be easier.. >_>
        line = line.split(',')
        cleaned_data.append(line)

    # create a list of dicts and make a dataframe out of it
    data_dict_list = []
    for row in cleaned_data:
        row_dict = {}
        row_dict['x'] = float(row[0])
        row_dict['y'] = float(row[1])
        row_dict['z'] = float(row[2])
        row_dict['m'] = float(row[3])
        data_dict_list.append(row_dict)

    ref_vectors = pd.DataFrame(data_dict_list)
    print("\nWE RCVD:")
    print(ref_vectors)

    # Build a simple list with numpy vectors for easier processing
    obs_positions = [np.array([rowt[1]['x'], rowt[1]['y'], rowt[1]['z']]) for rowt in ref_vectors.iterrows()]

    matches = []
    for i, obs_position in enumerate(obs_positions):
        # Calculate the angles between this observation and all other observations.
        # Find the two obervations which have the smallest angle.
        angels = [angle_between(obs_position, other_obs_pos) for other_obs_pos in obs_positions]
        closest_obs = np.argsort(angels)[:3]

        # Get the angles as well as the angle between the two closest observations.
        a1 = angels[closest_obs[1]]
        a2 = angels[closest_obs[2]]
        ab = angle_between(obs_positions[closest_obs[1]], obs_positions[closest_obs[2]])

        print(f"Two closest observations next to observation {i} are {closest_obs[1]} and {closest_obs[2]}")
        index, error = stars_improved.find_by_angles(a1, a2, ab)
        print(f"Matched star from catalog: {index} (Error: {error:.6})")
        matches.append((index, error))

    # Take the 5 best matches (smallest error) and build a string
    matches.sort(key = lambda x: x[1])
    index_string = ','.join([str(i[0]) for i in matches[:5]])

    print("\nWE SENT")
    print(index_string)
    send_cmd(server, index_string)
    data = server.recv(1024).decode("utf-8")
    print(data)
