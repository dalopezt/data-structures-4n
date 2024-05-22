def get_sandclock_values(matrix, x, y):
    return [
        matrix[y][x], matrix[y][x+1], matrix[y][x+2], matrix[y+1][x+1], matrix[y+2][x], matrix[y+2][x+1], matrix[y+2][x+2]
    ]

def weight(matrix, x, y):
    sandclock_values = get_sandclock_values(matrix, x, y)
    result = 0
    for value in sandclock_values:
        result += value
    return result

def read_matrix(path):
    matrix = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            words = line.split()
            matrix_row = []
            for word in words:
                matrix_row.append(eval(word))
            matrix.append(matrix_row)
    return matrix

def main():
    matrix = read_matrix("input.txt")
    sandclocks_matrix = []
    for i in range(4):
        sandclocks_row = []
        for j in range(4):
            sandclocks_row.append(weight(matrix, j, i))
        sandclocks_matrix.append(sandclocks_row)
    
    min_weight = sandclocks_matrix[0][0]
    for row in sandclocks_matrix:
        for item in row:
            if item < min_weight:
                min_weight = item
    
    print("Weight matrix: ", sandclocks_matrix)
    print("Min value: ", min_weight)

    

if __name__ == "__main__":
    main()
