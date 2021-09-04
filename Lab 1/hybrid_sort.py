# Insertion sort in Python

import time
import numpy as np 
import random

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


def merge_sort(array):

    # If the array only got 1 element 
    if (len(array) > 1):
        mid = len(array) // 2 
        left = array[:mid]
        right = array[mid:]

        merge_sort(left)
        # print(left, right)
        merge_sort(right)
        
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
        left = array[:mid]
        right = array[mid:]

        # print(left)
        # print(right)

        merge_sort(left)
        merge_sort(right)

        merge(array, left, right)

    return array 



array_10 = [0, 2, 5, 7, 1, 6, 3]
array_10_copy = array_10

# print("Array", array_10)
# timer = time.perf_counter()
# print("Sorted Array: ", mergesort(array_10))
# print("Time take (Merge Sort) n = ", (time.perf_counter() - timer))

print("Array", array_10_copy)
timer = time.perf_counter()
print("Sorted Array: ", hybrid_sort(array_10_copy, 32))
print("Time take (hybrid Sort) n = ", (time.perf_counter() - timer))

print("Array", array_10)
timer = time.perf_counter()
print("Sorted Array: ", merge_sort(array_10))
print("Time take (insertion Sort) n = ", (time.perf_counter() - timer))