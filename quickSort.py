import random
import time
from typing import List

def random_quicksort(arr: List[int]) -> List[int]:
    """
    Sorts an array using the randomized quicksort algorithm.
    
    Args:
        arr (List[int]): The input array to be sorted
        
    Returns:
        List[int]: The sorted array
        
    Time Complexity:
        - Average case: O(n log n)
        - Worst case: O(n^2) (very unlikely due to randomization)
        - Best case: O(n log n)
        
    Space Complexity:
        - O(log n) average and best case for recursion stack
        - O(n) worst case for recursion stack
    """
    # Make a copy to avoid modifying the input array
    arr = arr.copy()
    _random_quicksort(arr, 0, len(arr) - 1)
    return arr

def _random_quicksort(arr: List[int], low: int, high: int) -> None:
    """
    Internal recursive implementation of randomized quicksort.
    
    Args:
        arr (List[int]): The array being sorted (modified in-place)
        low (int): Starting index of the current subarray
        high (int): Ending index of the current subarray
    """
    if low < high:
        # Choose random pivot and partition the array
        pivot_idx = partition(arr, low, high)
        
        # Recursively sort the left and right subarrays
        _random_quicksort(arr, low, pivot_idx - 1)
        _random_quicksort(arr, pivot_idx + 1, high)

def partition(arr: List[int], low: int, high: int) -> int:
    """
    Partitions the array around a randomly chosen pivot.
    
    Args:
        arr (List[int]): The array to partition
        low (int): Starting index of the partition range
        high (int): Ending index of the partition range
        
    Returns:
        int: The final position of the pivot element
    """
    # Choose a random pivot and swap it with the last element
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    pivot = arr[high]
    
    # Initialize the position for elements smaller than pivot
    i = low - 1
    
    # Partition the array
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in its final position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def generate_number_list(n: int, list_type: str) -> list:
    """
    Generate a list of n numbers based on the specified type.
    
    Args:
        n (int): The number of elements to generate
        list_type (str): Type of list to generate ('ascending', 'descending', 'random', or 'duplicates')
        
    Returns:
        list: Generated list of numbers
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
        
    if list_type.lower() not in ['ascending', 'descending', 'random', 'duplicates']:
        raise ValueError("list_type must be 'ascending', 'descending', 'random', or 'duplicates'")
    
    if list_type.lower() == 'ascending':
        return list(range(1, n + 1))
    elif list_type.lower() == 'descending':
        return list(range(n, 0, -1))
    elif list_type.lower() == 'duplicates':
        # Generate a list with many duplicates by using a smaller range
        # This will ensure many numbers are repeated
        return [random.randint(1, n // 4) for _ in range(n)]
    else:  # random
        return random.sample(range(1, n * 2), n)  # Using n*2 to have a wider range of numbers

if __name__ == "__main__":
    list_ascending = generate_number_list(1000000, 'ascending')
    list_descending = generate_number_list(1000000, 'descending')
    list_random = generate_number_list(1000000, 'random')
    list_duplicates = generate_number_list(1000000, 'duplicates')
    # Timing randomized quicksort on each list
    print("Sorting ascending list with randomized quicksort...")
    start = time.perf_counter()
    sorted_asc_quick = random_quicksort(list_ascending)
    elapsed = time.perf_counter() - start
    print(f"Elapsed time: {elapsed:.6f} seconds")

    print("Sorting descending list with randomized quicksort...")
    start = time.perf_counter()
    sorted_desc_quick = random_quicksort(list_descending)
    elapsed = time.perf_counter() - start
    print(f"Elapsed time: {elapsed:.6f} seconds")

    print("Sorting random list with randomized quicksort...")
    start = time.perf_counter()
    sorted_rand_quick = random_quicksort(list_random)
    elapsed = time.perf_counter() - start
    print(f"Elapsed time: {elapsed:.6f} seconds")

    print("Sorting list with duplicates using randomized quicksort...")
    start = time.perf_counter()
    sorted_dup_quick = random_quicksort(list_duplicates)
    elapsed = time.perf_counter() - start
    print(f"Elapsed time: {elapsed:.6f} seconds")
