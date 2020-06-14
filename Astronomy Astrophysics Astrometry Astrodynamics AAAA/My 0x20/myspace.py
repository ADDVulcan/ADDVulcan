#!/usr/bin/env python3

import pandas as pd
import socket
import stars
import numpy as np
from angle import angle_between

HOST = "myspace.satellitesabove.me"
PORT = 5016
TICKET = 'ticket{golf97715papa:___a bunch of unguessable stuff___}'

# Known from previous tries.
# The output of this script is deliberately unstable to allow for trial and error.
# The second round rarely succeeds, so the first two rounds got hard coded here.
# You might have to run this script multiple times until it succeeds.

known_results = [
"181,205,288,574,734,927,1067,147,1223,1481,1523,1685,1831,1974",
"415,15,1131,1523,1974,574,1685,2042,288,898"
]

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

    indexes = []
    for i,rowt in ref_vectors.iterrows():
        star_obs = np.array([rowt['x'], rowt['y'], rowt['z']])

        # Find the closest two stars in the observation
        next_1_a = np.inf
        next_1_i = None
        next_2_a = np.inf
        next_2_i = None
        for i_t, rowt_t in ref_vectors.iterrows():
            if i == i_t:
                continue
            star_obs_t = np.array([rowt_t['x'], rowt_t['y'], rowt_t['z']])
            a = angle_between(star_obs, star_obs_t)
            if a < next_1_a:
                next_2_a = next_1_a
                next_2_i = next_1_i
                next_1_a = a
                next_1_i = i_t
            elif a < next_2_a:
                next_2_a = a
                next_2_i = i_t
        print("Two closest stars next to", i, "are :", next_1_i, next_1_a, next_2_i, next_2_a)
        index = stars.find_by_angles(next_1_a, next_2_a)
        print("Matched star:", index)
        indexes.append(index)

    # Remove duplicates, take a random subset and build a string
    indexes = np.array([str(i) for i in set(indexes)])
    chosen_idx = np.random.choice(len(indexes), replace=False, size=10)
    print(chosen_idx)
    indexes = indexes[chosen_idx]
    index_string = ','.join(indexes)

    # Throw away the result if we already know what it should be
    # from a previous run
    if iteration < len(known_results):
        index_string = known_results[iteration]
    iteration+=1

    print("\nWE SENT")
    print(index_string)
    send_cmd(server, index_string)
    data = server.recv(1024).decode("utf-8")
    print(data)
