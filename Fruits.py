import heapq
from collections import defaultdict

# B - banana, A - aplle, O - orange
fruit_order=["A", "B", "O"]

data = [
    [('O', 7), ('A', 1), ('A', 2), ('A', 4), ('A', 7), ('B', 10), ('B', 5), ('B', 1), ('B', 8), ('B', 3)], 
    [('B', 4), ('B', 7), ('B', 2), ('B', 9), ('B', 6), ('O', 3), ('O', 4), ('A', 3), ('O', 2), ('O', 9)], 
    [('O', 6), ('O', 10), ('O', 5), ('O', 1), ('O', 8), ('A', 8), ('A', 9), ('A', 6), ('A', 10), ('A', 5)]
    ]

def A_star(primary_layout, data):
    visited = []  # List to store the visited layouts
    queue = [(Manhattan_h(primary_layout), 0, primary_layout)]  # The priority queue with the primary layout

    while queue:
        _, moves, layout = heapq.heappop(queue)  # _ - means not needed, pop the layout with the lowest heuristic cost
        if layout == [
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
            [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 
            [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
                ]:
            
            print("Final layout")
            for sublist in get_primary_data(layout, data):
                print(sublist)

            return moves  # Return the number of moves if the goal layout is reached

        for new_layout in possible_moves(layout):  # Generate all possible next layouts
            if new_layout in visited:
                continue  # Skip if the layout has already been visited
            cost = Manhattan_h(new_layout) + moves + 1  # Calculate the cost of the new layout
            heapq.heappush(queue, (cost, moves + 1, new_layout))  # Add the new layout to the priority queue

    return -1  # No solution

#The heuristic value is calculated by computing the Manhattan distance between each fruit in the layout 
# and its sorted position in the final layout.
def Manhattan_h(layout):
    flat_layout = [item for row in layout for item in row]
    sorted_layout = sorted(flat_layout)
    return sum(abs(x - y) for x, y in zip(flat_layout, sorted_layout))

#Gets the sizes of the data to 2D list 
# and depending on the order normalizes it till 30
def get_sizes(data):
    sizes = [[],[],[]]
    k = 0
    for row in data:
        for fruit, size in row:
            if fruit == 'A':
                sizes[k].append(size+10)
            elif fruit == 'B':
                sizes[k].append(size)
            else:
                sizes[k].append(size+20)
        k+=1
    return sizes


#Generates a list of all possible next layouts with two types of moves: 
# horizontal swap (two fruits in the same column) 
# vertical swap (two fruits in different columns).
def possible_moves(layout):
    moves = []
    
    # generate all possible new layouts from horizontal swaps
    horizontal_moves = [[(i, j), (i, j+1)] for i in range(3) for j in range(9)]
    for move in horizontal_moves:
        new_layout = [column.copy() for column in layout]
        (i1, j1), (i2, j2) = move
        new_layout[i1][j1], new_layout[i2][j2] = new_layout[i2][j2], new_layout[i1][j1]
        moves.append(new_layout)
        
    # generate all possible new layouts from vertical swaps
    vertical_moves = [[(i, j), (i+1, j)] for i in range(2) for j in range(10)]
    for move in vertical_moves:
        new_layout = [list(column) for column in layout]
        (i1, j1), (i2, j2) = move
        new_layout[i1][j1], new_layout[i2][j2] = new_layout[i2][j2], new_layout[i1][j1]
        moves.append(new_layout)
    return moves


def get_primary_data(input_data, data):
    # Flatten the data
    flat_data = [item for sublist in data for item in sublist]
    
    # Group fruits by their types and sort the sizes
    fruits = defaultdict(list)
    for fruit, size in flat_data:
        fruits[fruit].append(size)
    for sizes in fruits.values():
        sizes.sort()
    
    # Map the input_data to original data
    output = []
    for row in input_data:
        original_list = [(fruit_order[(item-1)//10], fruits[fruit_order[(item-1)//10]].pop(0)) for item in row]
        output.append(original_list)
            
    return output

def main():
    print("Primary layout")
    for sublist in data:
        print(sublist)
    primary_layout = get_sizes(data) 
    moves = A_star(primary_layout, data)
    print(f"Least number of moves: {moves}")

if __name__ == "__main__":
    main()






