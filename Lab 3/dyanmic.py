import time

# * timer wrapper function
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        # format to 5 decimal places and ms
        print(f"{func.__name__} took {(end - start) * 1000:.5f} ms")
    return wrapper

# * create an object with weight and profit that can be added to knapsack, and multiplied
class Item:
    def __init__(self, weight, profit, id, is_multiple = False, multiplier = 1):
        self.weight = weight
        self.profit = profit
        self.id = id
        self.is_multiple = is_multiple
        self.multiplier = multiplier

    # getter
    def get_weight(self):
        return self.weight

    def get_profit(self):
        return self.profit

    # method which creates a new object with n times the weight and profit and id
    # ? this is to turn the problem into a 0/1 knapsack problem
    def multiply(self, n):
        return Item(self.weight * n, self.profit * n, self.id, True, n)

# * create a knapsack class with a capacity and a list of items
class Knapsack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.original_items = []

    def add_item(self, item):
        self.items.append(item)
    
    # ? for adding multiple items to the knapsack so it becomes a 0/1 knapsack problem
    def add_multiples_of_items(self):
        items_clone = self.items[:]
        self.original_items = items_clone
        # loop through the items
        for n in range(2, self.capacity + 1):
            for item in items_clone:
                # add the n multiple of the item to the items list
                self.items.append(item.multiply(n))

    #*########################################################################################
    #*####################################TABLE METHOD #######################################
    #*########################################################################################
    # ! table method for calculating the optimal solution
    def table(self):
        # create a capacity by number of items table, with all values set to -1
        table = [[-1 for i in range(self.capacity + 1)] for j in range(len(self.items) + 1)]
        # set the first row and column to 0
        for i in range(len(self.items) + 1):
            table[i][0] = 0
        for i in range(self.capacity + 1):
            table[0][i] = 0
        
        # start looping through the table
        # starting from the second row
        for i in range(1, len(self.items) + 1):
            # starting from the second column
            item = self.items[i - 1]
            for j in range(1, self.capacity + 1):
                prev_value = table[i - 1][j]
                # if j is greater than the weight of the item, use the previous value
                if j >= item.get_weight():
                    prev_row_weight_diff = table[i - 1][j - item.get_weight()]
                else:
                    prev_row_weight_diff = 0
                # if the item weight is less than the capacity
                # table[i][j] = max(table[i-1][j], table[i-1][j-item.weight] + item.profit)
                if j < item.get_weight():
                    table[i][j] = prev_value # add previous row since item weight is too big
                else:
                    table[i][j] = max(prev_value, prev_row_weight_diff + item.get_profit())
        return table

    # print optimal solution
    @timer
    def print_solution_table(self, print_table = True):
        table = self.table()
        # print the table
        print("\nTable Method:")
        print("----------------------------------------------------")
        if print_table:
            i = 0
            multiple = 1
            for row in table:
                if (i != 0):
                    print(f"{multiple} of Item {i}: \t", end = "")
                    print(row)
                i += 1
                if i > len(self.original_items):
                    i = 1
                    multiple += 1

        # print the solution
        print("\nSolution:")
        # find the highest profit in the table and find the corresponding coordinates
        max_profit = max(table[-1]) # highest profit in the last row
        print("Max profit:", max_profit)
        # loop through the table forwards to find the first time the highest profit is reached
        i = 0
        while(i < len(table)):
            if max_profit <= 0:
                break

            if max_profit in table[i]:
                # item i is included in the solution
                item = self.items[i - 1]
                print(f"{item.multiplier} times of item {item.id} at weight {item.weight} for a profit {item.profit}")
                max_profit -= item.get_profit()
                if max_profit <= 0:
                    break
                # ? restart the loop
                i = 0
            i += 1

    #*########################################################################################
    #*#################################### SET METHOD ########################################
    #*########################################################################################
    # merge 2 sets of tuples, the first set is given priority over the second 
    # unless the current tuple has a greater weight and profit than the first tuple of the second set
    # this is to help with dominance later
    def merge_sets(self, set_1, set_2):
        merged_set = []
        # loop through the first set
        for tuple_1 in set_1:
            # get first tuple of the second set
            # if second set is not empty
            if len(set_2) > 0:
                tuple_2 = set_2[0]
                # if the first tuple has a greater weight and profit than the second tuple
                if tuple_1[0] > tuple_2[0] and tuple_1[1] > tuple_2[1]:
                    # add the second tuple to the merged set
                    merged_set.append(tuple_2)
                    # remove the second tuple from the second set
                    set_2.remove(tuple_2)
                else:
                    # add the first tuple to the merged set
                    merged_set.append(tuple_1)
            else:
                # if the second set is empty, add the first tuple to the merged set
                merged_set.append(tuple_1)
        # add the remaining tuples of the second set to the merged set
        merged_set += set_2   
        return merged_set                 
    # set method for calculating optimal solution
    def set_method(self):
        # create a base set of all items being included and not
        # the first tuple is when no items are included
        set_of_sets = []
        base_set = [(0,0)]
        set_of_sets.append([(0,0)])
        # loop through all items
        for item in self.items:
            # loop through all tuples in the set,create a new tuple with the values of the item's weight and profit added to the tuple. (weight, profit)
            # add the new tuple to a temporary set
            temp_set = []
            for tuple in base_set:
                temp_tuple = (tuple[0] + item.get_weight(), tuple[1] + item.get_profit())
                # if weight is greater than capacity, don't add the tuple
                if temp_tuple[0] <= self.capacity:
                    temp_set.append(temp_tuple)
            # add the temporary set to the base set
            base_set = self.merge_sets(base_set, temp_set)
            # dominance rule
            # for each tuple in the base set if the profit of current tuple is smaller than equal the profit of the next tuple
            # and the weight of the current tuple is greater than the weight of the next tuple current tuple pointless
            for i in range(len(base_set) - 1):
                # check that there is a next tuple
                if i + 1 < len(base_set):
                    profit_diff = base_set[i][1] - base_set[i+1][1]
                    weight_diff = base_set[i][0] - base_set[i+1][0]
                    if profit_diff <= 0 and weight_diff > 0:
                        base_set.remove(base_set[i])
            # add a deep copy of the base set to the set of sets
            set_of_sets.append(base_set[:])
        return set_of_sets

    # print optimal solution using set method
    @timer
    def print_solution_set(self, print_sets = True):
        set_of_sets = self.set_method()
        print("\nSet Method:")
        print("----------------------------------------------------")
        # print the set of sets
        if print_sets:
            i = 0
            multiple = 1
            for set in set_of_sets:
                if i != 0:
                    print(f"{multiple} of Item {i}:\t\t", end = "")
                    print(set)
                i += 1

                if i > len(self.original_items):
                    i = 1
                    multiple += 1
        # print the solution
        print("\nSolution:")
        # find the tuple containing the highest profit
        max_profit_tuple = max(set_of_sets[-1])
        print("Max profit:", max_profit_tuple[1])
        # loop through the set of sets forwards
        # find the first time the highest profit is reached
        i = 0
        while (i < len(set_of_sets)):
            if max_profit_tuple[1] <= 0:
                break
            else:
                for tuple in set_of_sets[i]:
                    if tuple[1] == max_profit_tuple[1]:
                        # if the highest profit is reached, it is the first time
                        # the row corresponds to the item that is added
                        item = self.items[i-1]
                        print(f"{item.multiplier} times of item {item.id} at weight {item.weight} for a profit {item.profit}")
                        # new max profit is old max profit - item profit
                        max_profit_tuple = (max_profit_tuple[0] - item.get_weight(), max_profit_tuple[1] - item.get_profit())
                        if max_profit_tuple[1] <= 0:
                            break
                        i = 0
            i+=1
    
    def print_original_items(self):
        print("\nOriginal items:")
        for item in self.original_items:
            print(f"Item {item.id}: \t", end = "")
            print(f"{item.weight} kg for {item.profit} profit")
                
        


        
# # knapsack of capacity 8
# knapsack = Knapsack(8)
# # add items to the knapsack
# knapsack.add_item(Item(2, 1, 1))
# knapsack.add_item(Item(3, 2, 2))
# knapsack.add_item(Item(4, 5, 3))
# knapsack.add_item(Item(5, 6, 4))
# knapsack.add_multiples_of_items()
# # print the solutions
# knapsack.print_original_items()
# knapsack.print_solution_table(False)
# knapsack.print_solution_set(False)

# knapsack of capacity 14
knapsack = Knapsack(14)
# add items to the knapsack
knapsack.add_item(Item(4, 7, 1))
knapsack.add_item(Item(6, 6, 2))
knapsack.add_item(Item(8, 9, 3))
# print the solutions
knapsack.add_multiples_of_items()
knapsack.print_original_items()
knapsack.print_solution_table(True)
knapsack.print_solution_set(False)


