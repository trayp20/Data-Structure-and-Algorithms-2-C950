class HashTable:
    # Time Complexity: O(size)
    # Space Complexity: O(size)
    def __init__(self, size=40):
        # Initialize the HashTable with a given size.
        # Creates an array of empty lists to handle collisions.
        self.size = size
        self.table = [[] for _ in range(self.size)]  # O(size) time and space

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def _hash(self, key):
        #Compute the hash value for a given key.
        return hash(key) % self.size  # O(1) time

    # Time Complexity: Average O(1), Worst O(n) where n is the number of items in a bucket
    # Space Complexity: O(1)
    def insert(self, key, value):
        # Insert a key-value pair into the hash table.
        # If the key already exists, update its value.
        hash_index = self._hash(key)  # O(1) time
        for item in self.table[hash_index]:  # O(n) time in worst case
            if item[0] == key:
                item[1] = value  # Update existing value
                return
        self.table[hash_index].append([key, value])  # O(1) time

    # Time Complexity: Average O(1), Worst O(n) where n is the number of items in a bucket
    # Space Complexity: O(1)
    def lookup(self, key):
        # Look up a value by its key in the hash table.
        # Returns None if the key is not found.
        hash_index = self._hash(key)  # O(1) time
        for item in self.table[hash_index]:  # O(n) time in worst case
            if item[0] == key:
                return item[1]
        return None

    # Time Complexity: O(m) where m is the total number of items in the hash table
    # Space Complexity: O(1) as it yields items one at a time
    def all_packages(self):
       # Return all packages in the hash table using a generator.
        for bucket in self.table:  # O(size) iterations
            for item in bucket:  # O(items in bucket) iterations
                yield item[1]  # O(1) time per yield
