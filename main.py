import random
import time
import heapq
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool


def generate_random_lists(num_lists=1000, min_length=10000, max_length=100000):
    return [random.choices(range(1_000_000), k=random.randint(min_length, max_length)) for _ in range(num_lists)]


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr):
    return list(heapq.nsmallest(len(arr), arr))


def measure_sorting_time(args):
    sorting_function, arr = args
    start_time = time.time()
    sorting_function(arr.copy())
    return time.time() - start_time


def analyze_sorting_algorithms(lists):
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort
    }

    results = {name: [] for name in algorithms}

    with Pool() as pool:
        for name, func in algorithms.items():
            print(f"Se procesează {name}...")
            args = [(func, lst) for lst in lists]
            durations = list(tqdm(pool.imap(measure_sorting_time, args), total=len(args), desc=f"{name}", unit="list"))
            results[name] = durations

    avg_times = {name: sum(times) / len(times) for name, times in results.items()}
    return avg_times


def plot_results(avg_times):
    names = list(avg_times.keys())
    times = list(avg_times.values())

    plt.figure(figsize=(10, 6))
    plt.bar(names, times, color='purple')
    plt.xlabel("Algoritm")
    plt.ylabel("Timp mediu (s)")
    plt.title("Comparația algoritmilor de sortare")
    plt.show()


if __name__ == "__main__":
    print("Generarea listelor aleatorii...")
    random_lists = generate_random_lists(num_lists=1000, min_length=1000, max_length=10000)

    print("Analizarea algoritmilor de sortare...")
    avg_times = analyze_sorting_algorithms(random_lists)

    print("\nRezultate:")
    for algorithm, time_taken in avg_times.items():
        print(f"{algorithm}: {time_taken:.4f} secunde în medie")

    print("\nGenerarea graficului...")
    plot_results(avg_times)
