.globl matmul

.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
# 	d = matmul(m0, m1)
#   The order of error codes (checked from top to bottom):
#   If the dimensions don't match, 
#   this function exits with exit code 2.
#   If the dimensions of m0 do not make sense, 
#   this function exits with exit code 3.
#   If the dimensions of m1 do not make sense, 
#   this function exits with exit code 4.
# Arguments:
# 	a0 (int*)  is the pointer to the start of m0 
#	a1 (int)   is the # of rows (height) of m0
#	a2 (int)   is the # of columns (width) of m0
#	a3 (int*)  is the pointer to the start of m1
# 	a4 (int)   is the # of rows (height) of m1
#	a5 (int)   is the # of columns (width) of m1
#	a6 (int*)  is the pointer to the the start of d
# Returns:
#	None, sets d = matmul(m0, m1)
# =======================================================
matmul:

    # Error checks


    # Prologue


outer_loop_start:




inner_loop_start:












inner_loop_end:




outer_loop_end:


    # Epilogue
    
    
    ret

