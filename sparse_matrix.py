class SparseMatrix:
    def __init__(self, rows=None, cols=None):
        self.rows = rows
        self.cols = cols
        self.data = {}  # (row, col): value

    @classmethod
    def from_file(cls, filepath):
        """Load matrix from file in exact assignment format"""
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if len(lines) < 2:
            raise ValueError("Invalid file format")
        
        # Parse dimensions
        rows = int(lines[0].split('=')[1])
        cols = int(lines[1].split('=')[1])
        
        matrix = cls(rows, cols)
        
        # Parse elements
        for line in lines[2:]:
            if not (line.startswith('(') and line.endswith(')')):
                raise ValueError(f"Invalid format: {line}")
            
            parts = line[1:-1].split(',')
            if len(parts) != 3:
                raise ValueError(f"Invalid element: {line}")
            
            r = int(parts[0].strip())
            c = int(parts[1].strip())
            val = int(parts[2].strip())
            
            if r >= rows or c >= cols:
                raise ValueError(f"Position ({r},{c}) out of bounds")
            
            matrix.data[(r, c)] = val
            
        return matrix

    def get_element(self, row, col):
        """Get value at (row,col)"""
        return self.data.get((row, col), 0)

    def set_element(self, row, col, value):
        """Set value at (row,col)"""
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def add(self, other):
        """Matrix addition"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension mismatch for addition")
        
        result = SparseMatrix(self.rows, self.cols)
        all_keys = set(self.data.keys()) | set(other.data.keys())
        
        for (r, c) in all_keys:
            val = self.get_element(r, c) + other.get_element(r, c)
            if val != 0:
                result.set_element(r, c, val)
        return result

    def subtract(self, other):
        """Matrix subtraction"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension mismatch for subtraction")
        
        result = SparseMatrix(self.rows, self.cols)
        all_keys = set(self.data.keys()) | set(other.data.keys())
        
        for (r, c) in all_keys:
            val = self.get_element(r, c) - other.get_element(r, c)
            if val != 0:
                result.set_element(r, c, val)
        return result

    def multiply(self, other):
        """Matrix multiplication"""
        if self.cols != other.rows:
            raise ValueError("Dimension mismatch for multiplication")
        
        result = SparseMatrix(self.rows, other.cols)
        
        for (i, k), v1 in self.data.items():
            for (k2, j), v2 in other.data.items():
                if k == k2:
                    result.set_element(i, j, result.get_element(i, j) + v1 * v2)
        return result

    def __str__(self):
        """Output in assignment format"""
        lines = [f"rows={self.rows}", f"cols={self.cols}"]
        for (r, c), val in sorted(self.data.items()):
            lines.append(f"({r}, {c}, {val})")
        return "\n".join(lines)
