"""
ElectreNFSOutranking - This module computes NFS from given outranking(+non-outranking). Rankings can be a binary relation or real-value comparisons
Usage:
    ElectreNFSOutranking.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   outranking.xml
                   nonoutranking.xml (OPTIONAL see:method_parameters.xml)
                   method_parameters.xml
    -o DIR     Specify output directory. Files generated as output:
                   nfs.xml
                   strength.xml
                   weakness.xml
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

from common import ranks_to_xmcda, create_messages_file, get_dirs, \
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
            ('nonoutranking.xml', True),
            ('method_parameters.xml', False),
        ]
        params = [
            'alternatives',
            'outranking',
            'nonoutranking',
            'crisp_outranking'
        ]
        
        d = get_input_data(input_dir, filenames, params)
    
        alternativesId = d.alternatives
        outranking = d.outranking
        nonoutranking = d.nonoutranking
        crisp_outranking = d.crisp_outranking
        
        alg = algorithm(alternativesId, outranking, nonoutranking, crisp_outranking)
        result = alg.Run()
        
        type = 'real'
        if crisp_outranking == "true": type = 'integer'
        
        xmcda = ranks_to_xmcda(result[0], type, None)
        write_xmcda(xmcda, os.path.join(output_dir, 'nfs.xml'))
        xmcda = ranks_to_xmcda(result[1], type, None)
        write_xmcda(xmcda, os.path.join(output_dir, 'strength.xml'))
        xmcda = ranks_to_xmcda(result[2], type, None)
        write_xmcda(xmcda, os.path.join(output_dir, 'weakness.xml'))
        
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


            
