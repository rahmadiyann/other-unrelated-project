import threading
import multiprocessing
from abc import ABC, abstractmethod
from time import sleep

# OOP: Abstraction dan Inheritance
class Worker(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod  # Metode Abstraction
    def work(self):
        pass

class Developer(Worker):  # Inheritance
    def work(self):
        return self.name + " lagi coding."

class Designer(Worker):  # Inheritance 
    def work(self):
        return self.name + " lagi ngedesign."

# Polymorphism 
def assign_work(worker):
    return worker.work()

# String formatting, zip, ternary operator, list comprehension, dictionary comprehension
def process_tasks(workers, tasks):
    # zip
    task_list = []
    for worker, task in zip(workers, tasks):
        # Ternary operator
        if task:
            message = worker.name + " dikerjain sama " + task
        else:
            message = worker.name + " gak ngerjain apa apa"
        task_list.append((worker.name, message))
    
    # Dictionary comprehension
    task_dict = {name: message for name, message in task_list}
    return task_dict

# Packing, unpacking, enumerate, lambda, with statement, set
def log_worker_names(*worker_names):
    worker_set = set(worker_names)  # Set dari worker_names biar gak ada yang sama
    with open('worker_log.txt', 'w') as file:  # With statement
        for i, name in enumerate(worker_set):
            # Lambda buat ngeprint nama worker. Dibantu AI nulis lambdanya wkwk
            file.write((lambda i, n: "Worker " + str(i + 1) + ": " + n)(i, name) + '\n')

# Multithreading
def thread_worker(name, delay):
    sleep(delay)
    print(name + " selesai")

# Multiprocessing
def process_worker(name, delay):
    sleep(delay)
    print(name + " selesai")

if __name__ == "__main__":
    # Bikin objek Developer dan Designer
    dev = Developer("Rahmadiyan")
    des = Designer("Muhammad")

    # Polymorphism
    print(assign_work(dev))  # Outputs: "Rahmadiyan lagi coding."
    print(assign_work(des))  # Outputs: "Muhammad lagi ngedesign"

    # tring formatting, zip, ternary operator, list comprehension, dictionary comprehension
    workers = [dev, des]
    tasks = ["Bikin program buat tugas Day 2", "Gabut aja, jadi buat logo"]
    task_dict = process_tasks(workers, tasks)
    print(task_dict)  # Output dictionary

    # Packing and unpacking, enumerate, lambda, with statement, set
    worker_names = {"Rahmadiyan", "Muhammad"}  # Set data structure
    log_worker_names(*worker_names)  # Unpacking set dan log ke file

    # Multithreading
    thread1 = threading.Thread(target=thread_worker, args=("Thread-1", 2))
    thread2 = threading.Thread(target=thread_worker, args=("Thread-2", 3))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    # Multiprocessing
    process1 = multiprocessing.Process(target=process_worker, args=("Process-1", 2))
    process2 = multiprocessing.Process(target=process_worker, args=("Process-2", 3))

    process1.start()
    process2.start()

    process1.join()
    process2.join()
