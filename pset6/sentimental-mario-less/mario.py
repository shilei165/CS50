from cs50 import get_int

# Declear height to be 0
n = 0
# Get height from user
while (n <= 0 or n > 8):
    n = get_int("Height: ")
# Loop to print pyramids on screen
for i in range(1, n + 1):
    print((n - i) * " ", end="")
    print(i * "#")
