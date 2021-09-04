
import numpy as np
import time

def insertion_sort(array):

    for step in range(1, len(array)):
        key = array[step]
        j = step - 1
        
        # Compare the element with the ones before it
        # If it is smaller than the ones before it, then move the larger ones to current position 
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j = j - 1
        
        # Once an element smaller than it is found 
        # Place key at after it
        array[j + 1] = key
    
    return array 

def mergesort(array):

    # If the array only got 1 element 
    if (len(array) > 1):
        mid = len(array) // 2 
        left = array[:mid].copy()
        right = array[mid:].copy()

        mergesort(left)
        # print(left, right)
        mergesort(right)
        
        merge(array, left, right)
    
    return array
    

def merge(array, left, right):
    

    i = j = k = 0
    
    # while length of both right and left are not 0 z
    while(i < len(left) and j < len(right)):
        # compare first element of the 2 halves 
        if(left[i] < right[j]):
            array[k] = left[i]                
            i += 1
            k += 1
        else:
            array[k] = right[j]
            j += 1
            k += 1 

    # If there are still remaining elements in either half 
    while (i < len(left)):
        array[k] = left[i]
        i += 1
        k += 1

    while (j < len(right)):
        array[k] = right[j]
        k += 1
        j += 1
    
    return array

def hybrid_sort(array, S):
    if (len(array) <= S):
        insertion_sort(array)
    else:
        mid = len(array) // 2 
        left = array[:mid].copy()
        right = array[mid:].copy()

        mergesort(left)
        mergesort(right)

        merge(array, left, right)

    return array 

MIN_MERGE = 32
 
def calcMinRun(n):

    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r



array_test_0 = np.array(np.random.randint(10, size = 10))
array_test_0_copy = array_test_0
array_correct_0 = np.array(sorted(array_test_0)) # to compare against our implemented algorithms to make sure they work

array_test_1 = np.array(np.random.randint(10, size = 100))
array_test_1_copy = array_test_1
array_correct_1 = np.array(sorted(array_test_1))

array_test_2 = np.array(np.random.randint(10, size = 1000))
array_test_2_copy = array_test_2
array_correct_2 = np.array(sorted(array_test_2))

array_test_3 = np.array(np.random.randint(10, size = 10000))
array_test_3_copy = array_test_3
array_correct_3 = np.array(sorted(array_test_3))

array_test_4 = np.array(np.random.randint(10, size = 100000))
array_test_4_copy = array_test_4
array_correct_4 = np.array(sorted(array_test_4))

array_test_5 = np.array(np.random.randint(10, size = 1000000))
array_test_5_copy = array_test_5
array_correct_5 = np.array(sorted(array_test_5))

# print("Array", array_test_1)
# timer = time.perf_counter()
# print("Sorted Array: ", mergesort(array_test_1))
# print("Time take (Merge Sort) n = ", (time.perf_counter() - timer))

# # Check accuragcy 
# if np.array_equal(array_test_1, array_correct_1):
#     print(f"Merge sorted correctly")

# timer = time.perf_counter()
# print("Sorted Array: ", hybrid_sort(array_test_1, 7))
# print("Time taken (Hybrid Algorithm) = ", (time.perf_counter() - timer))

# if np.array_equal(array_test_1, array_correct_1):
#     print(f"Hybrid sorted correctly")

for i in range(5):

    # timer = time.perf_counter()
    # test = insertion_sort(np.copy(eval(f"array_test_{i}")))
    # array_size = len(eval(f"array_test_{i}"))
    # print(f"Time to sort array of size {array_size} is {time.perf_counter() - timer} seconds")
    # if np.array_equal(test, eval(f"array_correct_{i}")):
    #     print(f"Insertion sorted correctly")

    timer = time.perf_counter()
    test = hybrid_sort(np.copy(eval(f"array_test_{i}")), 7)
    array_size = len(eval(f"array_test_{i}"))
    print(f"Time to sort array of size {array_size} is {time.perf_counter() - timer} seconds")
    if np.array_equal(test, eval(f"array_correct_{i}")):
        print(f"Hybrid sorted correctly")

    timer = time.perf_counter()
    test = mergesort(np.copy(eval(f"array_test_{i}")))
    array_size = len(eval(f"array_test_{i}"))
    print(f"Time to sort array of size {array_size} is {time.perf_counter() - timer} seconds")
    if np.array_equal(test, eval(f"array_correct_{i}")):
        print(f"Merge sorted correctly \n")