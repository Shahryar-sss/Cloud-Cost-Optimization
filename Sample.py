import threading

def sample():
    thread = threading.Thread(target=abc, args=["Hey"])
    thread.start()


def abc(a):
    print(a)
    threading.Timer(2, abc, args=["hey"]).start()

sample()