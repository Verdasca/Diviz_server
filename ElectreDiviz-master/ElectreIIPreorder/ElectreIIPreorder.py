"""
ElectreDistillation - This module performs distillation (upwards/downwards)
Usage:
    ElectreDistillation.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   credibility.xml
                   method_parameters.xml
    -o DIR     Specify output directory. Files generated as output:
                   ranking.xml
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

from common import comparisons_to_xmcda, ranks_to_xmcda, create_messages_file, get_dirs, \
    get_error_message, get_input_data, get_linear, omega, write_xmcda, Vividict

__version__ = '0.1.0'

def main():
    try:
        args = docopt(__doc__, version=__version__)
        output_dir = None
        input_dir, output_dir = get_dirs(args)
        
        filenames = [
            ('alternatives.xml', False),
            ('outranking.xml', False),
            ('preorder.xml', True),
            ('method_parameters.xml', True),
        ]
        params = [
            'alternatives',
            'outranking',
            'preorder',
            'direction',
        ]
        
        d = get_input_data(input_dir, filenames, params)
    
        alternatives = d.alternatives
        
        preorder = None
        if (d.preorder is not None):
            preorder = d.preorder
        
        outranking = d.outranking
        direction = d.direction
        
        alg = algorithm(alternatives, outranking, preorder, direction)
        result = alg.Run()
        
        xmcda = ranks_to_xmcda(result, 'integer', None)
        write_xmcda(xmcda, os.path.join(output_dir, 'ranking.xml'))
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
