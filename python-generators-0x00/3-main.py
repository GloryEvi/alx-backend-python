
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)
            print()  # Add empty line between users as shown in expected output

except BrokenPipeError:
    sys.stderr.close()