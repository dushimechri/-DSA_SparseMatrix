class CompactMatrix:
    def __init__(self, num_rows=None, num_cols=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.values = {}  # Dictionary storing (row,col) -> value mappings

    @classmethod
    def load_from_file(cls, file_path):
        """Create matrix from file with specified format"""
        try:
            with open(file_path, 'r') as file:
                content = [line.strip() for line in file if line.strip()]
            
            if len(content) < 2:
                raise ValueError("File format is incorrect")

            # Extract dimensions
            height = int(content[0].split('=')[1].strip())
            width = int(content[1].split('=')[1].strip())
            
            matrix = cls(height, width)
            
            # Process non-zero elements
            for entry in content[2:]:
                if not entry.startswith('(') or not entry.endswith(')'):
                    raise ValueError(f"Malformed entry: {entry}")
                
                # Parse (row,col,value) tuple
                nums = entry[1:-1].split(',')
                if len(nums) != 3:
                    raise ValueError(f"Invalid tuple format: {entry}")
                
                row, col, value = map(int, map(str.strip, nums))
                
                if row >= height or col >= width:
                    raise ValueError(f"Coordinates ({row},{col}) exceed matrix dimensions")
                
                matrix.values[(row, col)] = value
                
            return matrix
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")

    def fetch_value(self, row, col):
        """Retrieve value at specified position"""
        return self.values.get((row, col), 0)

    def update_value(self, row, col, value):
        """Assign value at specified position"""
        if value != 0:
            self.values[(row, col)] = value
        else:
            self.values.pop((row, col), None)

    def add_matrices(self, other):
        """Perform matrix addition"""
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices must have matching dimensions for addition")
        
        result = CompactMatrix(self.num_rows, self.num_cols)
        coordinates = set(self.values.keys()) | set(other.values.keys())
        
        for pos in coordinates:
            sum_val = self.fetch_value(*pos) + other.fetch_value(*pos)
            if sum_val != 0:
                result.update_value(*pos, sum_val)
        return result

    def subtract_matrices(self, other):
        """Perform matrix subtraction"""
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices must have matching dimensions for subtraction")
        
        result = CompactMatrix(self.num_rows, self.num_cols)
        coordinates = set(self.values.keys()) | set(other.values.keys())
        
        for pos in coordinates:
            diff = self.fetch_value(*pos) - other.fetch_value(*pos)
            if diff != 0:
                result.update_value(*pos, diff)
        return result

    def multiply_matrices(self, other):
        """Perform matrix multiplication"""
        if self.num_cols != other.num_rows:
            raise ValueError("Inner dimensions must match for multiplication")
        
        result = CompactMatrix(self.num_rows, other.num_cols)
        
        for (i, k), val1 in self.values.items():
            for (k2, j), val2 in other.values.items():
                if k == k2:
                    curr_val = result.fetch_value(i, j)
                    result.update_value(i, j, curr_val + val1 * val2)
        return result

    def __str__(self):
        """Format matrix as string in required format"""
        output = [f"rows={self.num_rows}", f"cols={self.num_cols}"]
        for (row, col), value in sorted(self.values.items()):
            output.append(f"({row}, {col}, {value})")
        return "\n".join(output)
