import os
import glob
from sparse_matrix import SparseMatrix

def find_matrix_files():
    """Automatically find matrix files in sample_inputs directories"""
    # Define paths to search
    current_dir = os.getcwd()
    sample_dirs = [
        os.path.join(current_dir, "sample_inputs"),
        os.path.join(current_dir, "..", "sample_inputs"),
        os.path.join(current_dir, "..", "..", "sample_inputs"),
    ]
    
    # List all potential matrix files
    matrix_files = []
    for sample_dir in sample_dirs:
        if os.path.exists(sample_dir):
            print(f"Found sample directory: {sample_dir}")
            # Look for .txt files in the directory
            pattern = os.path.join(sample_dir, "*.txt")
            files = glob.glob(pattern)
            print(f"Found {len(files)} .txt files in this directory")
            
            for file in files:
                print(f"Checking file: {os.path.basename(file)}")
                
                if validate_matrix_file(file):
                    print(f"✅ Valid matrix file: {file}")
                    matrix_files.append(file)
                else:
                    print(f"❌ Invalid matrix format: {file}")
    
    return matrix_files

def validate_matrix_file(path):
    """Check if file exists and has correct format"""
    if not os.path.exists(path):
        print(f"  File does not exist: {path}")
        return False
        
    # Quick format check
    try:
        with open(path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            
            if len(lines) < 2:
                print(f"  Too few lines in file: {len(lines)}")
                return False
                
            if not lines[0].startswith('rows='):
                print(f"  Missing 'rows=' in first line: {lines[0]}")
                return False
                
            if not lines[1].startswith('cols='):
                print(f"  Missing 'cols=' in second line: {lines[1]}")
                return False
                
            # Try to parse dimensions
            try:
                rows = int(lines[0].split('=')[1])
                cols = int(lines[1].split('=')[1])
                print(f"  Matrix dimensions: {rows}x{cols}")
            except (ValueError, IndexError):
                print(f"  Failed to parse dimensions")
                return False
                
            # Check elements for dimension validity
            for i, line in enumerate(lines[2:], 3):
                if not (line.startswith('(') and line.endswith(')')):
                    print(f"  Invalid element format at line {i}: {line}")
                    continue
                    
                try:
                    parts = line[1:-1].split(',')
                    if len(parts) != 3:
                        print(f"  Element needs 3 parts at line {i}: {line}")
                        continue
                        
                    r = int(parts[0].strip())
                    c = int(parts[1].strip())
                    
                    if r >= rows or c >= cols:
                        print(f"  Position ({r},{c}) out of bounds at line {i} - matrix is {rows}x{cols}")
                        continue
                except ValueError:
                    print(f"  Failed to parse element at line {i}: {line}")
                    continue
            
            return True
    except Exception as e:
        print(f"  Error validating file: {str(e)}")
        return False

def create_sample_files():
    """Create sample matrix files if none are found"""
    sample_dir = os.path.join(os.getcwd(), "sample_inputs")
    
    # Create directory if it doesn't exist
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
        print(f"Created sample_inputs directory: {sample_dir}")
    
    # Create first sample file
    matrix1_path = os.path.join(sample_dir, "matrix1.txt")
    with open(matrix1_path, 'w') as f:
        f.write("rows=3\n")
        f.write("cols=3\n")
        f.write("(0, 0, 5)\n")
        f.write("(1, 1, 10)\n")
        f.write("(2, 2, 15)\n")
    
    # Create second sample file
    matrix2_path = os.path.join(sample_dir, "matrix2.txt")
    with open(matrix2_path, 'w') as f:
        f.write("rows=3\n")
        f.write("cols=3\n")
        f.write("(0, 0, 1)\n")
        f.write("(1, 1, 2)\n")
        f.write("(2, 2, 3)\n")
    
    print(f"Created sample matrix files:")
    print(f"1. {matrix1_path}")
    print(f"2. {matrix2_path}")
    
    return [matrix1_path, matrix2_path]

def inspect_files(file_paths):
    """Display detailed information about the matrix files"""
    for i, file_path in enumerate(file_paths):
        print(f"\nInspecting matrix file {i+1}: {file_path}")
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                
                if len(lines) < 2:
                    print("  Invalid file format - too few lines")
                    continue
                
                rows = int(lines[0].split('=')[1])
                cols = int(lines[1].split('=')[1])
                print(f"  Matrix dimensions: {rows}x{cols}")
                print(f"  Non-zero elements: {len(lines) - 2}")
                
                # Show first few elements
                for j, line in enumerate(lines[2:8]):  # Show up to 6 elements
                    print(f"  Element {j+1}: {line}")
                
                if len(lines) > 10:
                    print(f"  ... {len(lines) - 10} more elements ...")
                
                # Check for potential dimension issues
                max_row = -1
                max_col = -1
                for line in lines[2:]:
                    if line.startswith('(') and line.endswith(')'):
                        parts = line[1:-1].split(',')
                        if len(parts) == 3:
                            try:
                                r = int(parts[0].strip())
                                c = int(parts[1].strip())
                                max_row = max(max_row, r)
                                max_col = max(max_col, c)
                            except ValueError:
                                continue
                
                if max_row >= rows or max_col >= cols:
                    print(f"  ⚠️ DIMENSION ISSUE: Found element at position ({max_row},{max_col}), but matrix is {rows}x{cols}")
                    print(f"  This will cause 'Position out of bounds' error when loading")
        except Exception as e:
            print(f"  ❌ Error reading file: {str(e)}")

def create_compatible_files(matrix_files):
    """Create compatible matrix files with matching dimensions"""
    print("\nCreating compatible matrix files...")
    
    # Get the first two selected files
    file1 = matrix_files[0]
    file2 = matrix_files[1]
    
    # Read dimensions
    try:
        with open(file1, 'r') as f:
            lines1 = [line.strip() for line in f if line.strip()]
            rows1 = int(lines1[0].split('=')[1])
            cols1 = int(lines1[1].split('=')[1])
        
        with open(file2, 'r') as f:
            lines2 = [line.strip() for line in f if line.strip()]
            rows2 = int(lines2[0].split('=')[1])
            cols2 = int(lines2[1].split('=')[1])
        
        # Create directory for compatible files
        sample_dir = os.path.join(os.getcwd(), "compatible_matrices")
        if not os.path.exists(sample_dir):
            os.makedirs(sample_dir)
        
        # Create files with compatible dimensions for addition/subtraction
        add_file1 = os.path.join(sample_dir, "add_matrix1.txt")
        add_file2 = os.path.join(sample_dir, "add_matrix2.txt")
        
        # Use the min dimensions to ensure compatibility
        add_rows = min(rows1, rows2)
        add_cols = min(cols1, cols2)
        
        with open(add_file1, 'w') as f:
            f.write(f"rows={add_rows}\n")
            f.write(f"cols={add_cols}\n")
            f.write("(0, 0, 5)\n")
            f.write("(1, 1, 10)\n")
        
        with open(add_file2, 'w') as f:
            f.write(f"rows={add_rows}\n")
            f.write(f"cols={add_cols}\n")
            f.write("(0, 0, 1)\n")
            f.write("(1, 1, 2)\n")
        
        # Create files with compatible dimensions for multiplication
        mult_file1 = os.path.join(sample_dir, "mult_matrix1.txt")
        mult_file2 = os.path.join(sample_dir, "mult_matrix2.txt")
        
        mult_rows = 3
        mult_mid = 4   # This is cols of first matrix and rows of second
        mult_cols = 2
        
        with open(mult_file1, 'w') as f:
            f.write(f"rows={mult_rows}\n")
            f.write(f"cols={mult_mid}\n")
            f.write("(0, 0, 1)\n")
            f.write("(0, 1, 2)\n")
            f.write("(1, 0, 3)\n")
            f.write("(1, 1, 4)\n")
        
        with open(mult_file2, 'w') as f:
            f.write(f"rows={mult_mid}\n")
            f.write(f"cols={mult_cols}\n")
            f.write("(0, 0, 5)\n")
            f.write("(1, 0, 6)\n")
            f.write("(2, 1, 7)\n")
            f.write("(3, 1, 8)\n")
        
        return {
            'add': [add_file1, add_file2],
            'multiply': [mult_file1, mult_file2]
        }
    except Exception as e:
        print(f"Error creating compatible files: {str(e)}")
        return None

def auto_select_files(matrix_files):
    """Select appropriate matrix files for the operation"""
    if len(matrix_files) < 2:
        print(f"⚠️ Not enough matrix files found. Only found {len(matrix_files)} valid files.")
        return None, None
    
    # Just grab the first two files
    return matrix_files[0], matrix_files[1]

def get_operation_choice():
    """Get user choice for matrix operation"""
    print("Sparse Matrix Operations")
    print("1. Add\n2. Subtract\n3. Multiply")
    
    while True:
        choice = input("Select operation (1-3): ").strip()
        if choice in {'1', '2', '3'}:
            return choice
        print("Invalid input. Please enter 1, 2, or 3")

def main():
    # Find matrix files automatically
    print("Searching for matrix files...")
    matrix_files = find_matrix_files()
    
    if not matrix_files:
        print("\n⚠️ No valid matrix files found.")
        choice = input("Would you like to create sample matrix files? (y/n): ").strip().lower()
        if choice.startswith('y'):
            matrix_files = create_sample_files()
        else:
            print("Please ensure matrix files are in a 'sample_inputs' directory")
            print("with the correct format (rows=X, cols=Y, followed by elements)")
            return
    else:
        # Inspect the found files for potential issues
        inspect_files(matrix_files)
        
        # Ask if user wants to use compatible files
        print("\nWould you like to:")
        print("1. Use the detected matrix files (may cause dimension errors)")
        print("2. Create new compatible files for demonstrations")
        choice = input("Enter choice (1-2): ").strip()
        
        if choice == '2':
            compatible_files = create_compatible_files(matrix_files)
            if compatible_files:
                print("\nCreated compatible matrix files:")
                print("For addition/subtraction:")
                for f in compatible_files['add']:
                    print(f"- {f}")
                print("For multiplication:")
                for f in compatible_files['multiply']:
                    print(f"- {f}")
    
    print(f"\nFound {len(matrix_files)} valid matrix files:")
    for i, file in enumerate(matrix_files):
        print(f"{i+1}. {file}")
    
    # Get operation choice
    choice = get_operation_choice()
    
    # Auto-select files
    if choice in ['1', '2']:  # Addition or Subtraction
        if 'compatible_files' in locals() and compatible_files:
            file1, file2 = compatible_files['add']
        else:
            file1, file2 = auto_select_files(matrix_files)
    else:  # Multiplication
        if 'compatible_files' in locals() and compatible_files:
            file1, file2 = compatible_files['multiply']
        else:
            file1, file2 = auto_select_files(matrix_files)
    
    if not file1 or not file2:
        return
    
    print(f"\nUsing matrix files:")
    print(f"1. {file1}")
    print(f"2. {file2}")

    try:
        # Load matrices
        m1 = SparseMatrix.from_file(file1)
        m2 = SparseMatrix.from_file(file2)
        
        # Perform operation
        if choice == '1':
            result = m1.add(m2)
            op_name = "Addition"
        elif choice == '2':
            result = m1.subtract(m2)
            op_name = "Subtraction"
        else:
            result = m1.multiply(m2)
            op_name = "Multiplication"
        
        # Save result
        outfile = f"result_{op_name.lower()}.txt"
        with open(outfile, 'w') as f:
            f.write(str(result))
        
        print(f"\n✅ {op_name} completed successfully!")
        print(f"Result saved to {os.path.abspath(outfile)}")
        print(f"Dimensions: {result.rows}x{result.cols}")
        print(f"Non-zero elements: {len(result.data)}")
    
    except ValueError as e:
        print(f"\n❌ Dimension error: {e}")
        print("For addition/subtraction: matrices must be same size")
        print("For multiplication: columns of 1st must equal rows of 2nd")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please verify:")
        print("1. File content matches exact required format")
        print("2. All values are integers")
        if os.path.exists(file1):
            with open(file1, 'r') as f:
                first_few_lines = "".join([next(f, "") for _ in range(5)])
                print(f"3. First file contents:\n{first_few_lines}...")
        if os.path.exists(file2):
            with open(file2, 'r') as f:
                first_few_lines = "".join([next(f, "") for _ in range(5)])
                print(f"4. Second file contents:\n{first_few_lines}...")

if __name__ == "__main__":
    # Print current working directory for debugging
    print(f"Current directory: {os.getcwd()}")
    
    # Check if sample_inputs directory exists relative to current or parent directory
    sample_dir_current = os.path.join(os.getcwd(), "sample_inputs")
    sample_dir_parent = os.path.join(os.getcwd(), "..", "sample_inputs")
    
    print(f"Looking for sample inputs at:")
    print(f"1. {sample_dir_current} {'(EXISTS)' if os.path.exists(sample_dir_current) else '(NOT FOUND)'}")
    print(f"2. {sample_dir_parent} {'(EXISTS)' if os.path.exists(sample_dir_parent) else '(NOT FOUND)'}")
    
    main()
