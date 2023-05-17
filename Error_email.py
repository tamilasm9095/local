

import logging
import traceback
from Error_func import  errorEmail


logging.basicConfig(filename='/home/ubuntu/democron/example.log', level=logging.ERROR)
a=124
try:
    b=a[:1]

except Exception as e:

    logging.exception('An error occurred:')
    error=traceback.format_exc()
    errorEmail(error)

#
