"""
ElectreDistillationRank - This module provides three types of resultes performed on downwards and upwards distillation
Usage:
    ElectreDistillationRank.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   downwards.xml
                   upwards.xml
    -o DIR     Specify output directory. Files generated as output:
                   intersection.xml
                   rank.xml
                   median.xml
                   messages.xml
    --version  Show version.
    -h --help  Show this screen.
"""


from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback
from functools import partial

from algorithm import *

from docopt import docopt

from common import comparisons_to_xmcda, outranking_to_xmcda, ranks_to_xmcda, create_messages_file, get_dirs, \
    get_error_message, get_input_data, get_linear, omega, write_xmcda, Vividict

__version__ = '0.1.0'

def main():
    try:
        args = docopt(__doc__, version=__version__)
        output_dir = None
        input_dir, output_dir = get_dirs(args)
        
        filenames = [
            ('alternatives.xml', False),
            ('downwards.xml', False),
            ('upwards.xml', False),
        ]
        params = [
            'alternatives',
            'downwards',
            'upwards',
        ]
        
        d = get_input_data(input_dir, filenames, params)
    
        alternativesId = d.alternatives
        downwards = d.downwards
        upwards = d.upwards

        alg = algorithm(alternativesId, downwards, upwards)
        result = alg.Run()
        
        comparables = (alternativesId, alternativesId)
        #xmcda = comparisons_to_xmcda(result[0], comparables)
        xmcda = outranking_to_xmcda(result[0])
        write_xmcda(xmcda, os.path.join(output_dir, 'intersection.xml'))
        xmcda = ranks_to_xmcda(result[1], 'integer', None)
        write_xmcda(xmcda, os.path.join(output_dir, 'rank.xml'))
        xmcda = ranks_to_xmcda(result[2], 'integer', None)
        write_xmcda(xmcda, os.path.join(output_dir, 'median.xml'))
        
        create_messages_file(None, ('Everything OK.',), output_dir)    
        return 0
    
    except Exception, err:
        err_msg = get_error_message(err)
        log_msg = traceback.format_exc()
        print(log_msg.strip())
        create_messages_file((err_msg, ), (log_msg, ), output_dir)
        return 1            
        
           

if __name__ == '__main__':
    sys.exit(main())


            


            
