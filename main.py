numbers = [5, 2, 8, 1, 9, 4, 3, 6, 7]

# Even numbers first (descending), then odd numbers (descending)
sorted_list = sorted(numbers, key=lambda x: (x % 2, -x))
print(sorted_list)  # Output: [8, 6, 4, 2, 9, 7, 5, 3, 1]
