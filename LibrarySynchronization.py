from sys import argv
from time import sleep
import threading


# semaphore objects
# lock objects for book1 copies
semBook1 = threading.BoundedSemaphore(3)

# lock objects for book2 copies
semBook2 = threading.BoundedSemaphore(2)

# lock objects for book3 copies
semBook3 = threading.BoundedSemaphore(2)

# lock objects for global counter how many times 3 books were lend
counterSem = threading.BoundedSemaphore()

# lock objects for global counter how many times each student lend 3 books
counterListSem = threading.BoundedSemaphore()

# lock objects for global boolean whether a student has all three books now or not
hasAllBooksListSem = threading.BoundedSemaphore()


# function to lend a copy of each book
def lend_the_books():

    # definition of several global variables
    global waiting_time
    global counter_list
    global counter
    global hasAllBooksList
    global output_interval

    # while loop to acquire and release all 3 books
    while True:
        # acquiring of all three books
        semBook1.acquire()
        semBook2.acquire()
        semBook3.acquire()

        # entering "True" in list hasAllBooksList because this student process
        # has a copy of all three books
        hasAllBooksListSem.acquire()
        hasAllBooksList[int(threading.currentThread().getName()) - 1] = True
        hasAllBooksListSem.release()

        # this student process has now to "read" its three books
        # for waiting_time seconds
        sleep(float(waiting_time))

        # several outputs
        # increase the counter variable which counts, how often three books
        # were lent over all student processes
        counterSem.acquire()
        counter += 1

        # increase the counter in list counter_list which stores how often
        # this special student process has lent all three books
        counterListSem.acquire()
        counter_list[int(threading.currentThread().getName()) - 1] += 1

        # "if" handles how often we print our outputs to the console.
        # If output_interval is 1, every time all three books were lent this output
        # is printed to the console. If output_interval = 100, every 100 loans
        # this output is printed to the console.
        if counter % output_interval == 0:
            # for loop prints how often every single student process has lent all three books
            for i in range(int(amountStudents)):
                print("Student " + str(i + 1) + " hat " + str(counter_list[i]) + " Mal alle drei Buecher bekommen!\r")
            print("")
            # for loop prints, which student processes have all three books at the moment
            for j in range(int(amountStudents)):
                if hasAllBooksList[j]:
                    print("Student " + str(j + 1) + " hat aktuell alle drei Buecher.\r")
            print("")
        counterListSem.release()
        counterSem.release()

        # releasing of all three books
        semBook1.release()
        semBook2.release()
        semBook3.release()

        # entering "False" in list hasAllBooksList because this student process
        # has no copy of any of the three books
        hasAllBooksListSem.acquire()
        hasAllBooksList[int(threading.currentThread().getName()) - 1] = False
        hasAllBooksListSem.release()


# main function
def main():

    # list to start and collect a thread for every student
    students = []

    # for loop creates the required amount of student processes,
    # appends the current created student process in our list students
    # of student processes, initializes the corresponding loan counter
    # of this current created student process in list counter_list, sets the
    # corresponding boolean in list hasAllBooksList of this current
    # created student process to false (because it has not all three books
    # at the moment) and starts the current created student process.
    for i in range(int(amountStudents)):
        t = threading.Thread(target=lend_the_books, name=str(i + 1))
        students.append(t)
        counter_list.append(0)
        hasAllBooksList.append(False)
        t.start()

    # for loop joins all student processes
    for student in students:
        student.join()


# reads number of students from console input (first argument)
amountStudents = argv[1]

# time a student has to "read" when he/she has all three books (second argument)
waiting_time = argv[2]


# time a student has to "read" when he/she has all three books (second argument)
output_interval = 20

# counter for how many times 3 books were lent
counter = 0

# list how many times each student lend 3 books
counter_list = []

# list of boolean whether a student has all three books now or not
hasAllBooksList = []

# call of main function
main()
