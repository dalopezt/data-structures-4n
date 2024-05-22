import math
import time
import json

PRECISION = 5

def primes_by_eratosthenes(n):
    if n == 1:
        return []
    numbers = [False for i in range(n-1)]
    primes = []

    index = 0 # 2
    while True:
        # Get new prime
        primes.append(index+2)
        numbers[index] = True

        aux = (index+2)*(index+2) - 2 # Index of the square
        while aux < n-1:
            if not numbers[aux]:
                numbers[aux] = True
            aux += (index+2)
        
        while numbers[index]:
            index += 1
            if index == n-1:
                return primes

def primes_by_divisibility(n):
    primes = []
    if n == 1:
        return primes
    
    for i in range(2, n+1):
        j = 2
        flag = True
        while j <= math.sqrt(i):
            if i%j == 0:
                flag = False
                break
            j += 1
        if flag:
            primes.append(i)
    return primes
        
def main(n):
    time_1 = time.time()
    primes_by_eratosthenes(n)
    delta_1 = time.time() - time_1
    time_2 = time.time()
    primes_by_divisibility(n)
    delta_2 = time.time() - time_2
    return {"n": n, "e": delta_1, "d": delta_2}
    # print("Eratosthenes prime count: ", len(primes_1), "Time: ", delta_1)
    # print("Divisibility prime count: ", len(primes_2), "Time: ", delta_2)

if __name__ == "__main__":
    metrics = []
    for i in range(1, 21):
        partial = []
        for j in range(PRECISION):
            print("Iteration: ", i, j)
            partial.append(main(50_000*i))
        
        new_metric = {}
        avg_e_iteration = 0
        avg_d_iteration = 0
        for partial_item in partial:
            avg_e_iteration += partial_item["e"]
            avg_d_iteration += partial_item["d"]
        avg_e_iteration /= PRECISION
        avg_d_iteration /= PRECISION

        metrics.append({
            "n": partial[0]["n"], 
            "e": avg_e_iteration, 
            "d": avg_d_iteration, 
            "ln_n": math.log(partial[0]["n"]), 
            "ln_e": math.log(avg_e_iteration), 
            "ln_d": math.log(avg_d_iteration)})
    
    with open("metrics.json", "w") as f:
        f.write(json.dumps(metrics, indent=2))