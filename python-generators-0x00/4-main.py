
import sys

# Import and run the memory-efficient aggregate function
aggregate = __import__('4-stream_ages')

try:
    aggregate.calculate_average_age()
except BrokenPipeError:
    sys.stderr.close()