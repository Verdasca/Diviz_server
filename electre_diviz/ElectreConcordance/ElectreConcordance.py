#!/usr/bin/env python

"""
ElectreConcordance - computes concordance matrix using procedure which is
common to the most methods from the Electre family.

The key feature of this module is its flexibility in terms of the types of
elements allowed to compare, i.e. alternatives vs alternatives, alternatives vs
boundary profiles and alternatives vs central (characteristic) profiles.

Usage:
    ElectreConcordance.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   classes_profiles.xml (optional)
                   criteria.xml
                   method_parameters.xml
                   performance_table.xml
                   profiles_performance_table.xml (optional)
                   weights.xml
    -o DIR     Specify output directory. Files generated as output:
                   concordance.xml
                   messages.xml
    --version  Show version.
    -h --help  Show this screen.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback
from functools import partial

from docopt import docopt

from common import comparisons_to_xmcda, create_messages_file, get_dirs, \
    get_error_message, get_input_data, get_linear, omega, write_xmcda, Vividict

__version__ = '0.2.0'


def get_concordance(comparables_a, comparables_perf_a, comparables_b,
                    comparables_perf_b, criteria, thresholds, pref_directions,
                    weights):

    # 'partial' in this function's name has nothing to do w/ functools.partial
    def _get_partial_concordance(x, y, criterion):
        _omega = partial(omega, pref_directions, criterion)
        _get_linear = partial(get_linear, pref_directions, criterion, x, y)
        p = _get_linear(thresholds[criterion].get('preference', 0))
        q = _get_linear(thresholds[criterion].get('indifference', 0))
        if _omega(x, y) < -p:
            return 0.0
        elif _omega(x, y) >= -q:
            return 1.0
        else:
            return (_omega(x, y) + p) / (p - q)

    def _get_aggregated_concordance(x, y):
        sum_of_weights = sum([weights[criterion] for criterion in criteria])
        s = sum([weights[criterion] * partial_concordances[x][y][criterion]
                 for criterion in criteria])
        concordance = s / sum_of_weights
        return concordance

    two_way_comparison = True if comparables_a != comparables_b else False
    # compute partial concordances
    partial_concordances = Vividict()
    for a in comparables_a:
        for b in comparables_b:
            for criterion in criteria:
                pc = _get_partial_concordance(comparables_perf_a[a][criterion],
                                              comparables_perf_b[b][criterion],
                                              criterion)
                partial_concordances[a][b][criterion] = pc
                if two_way_comparison:
                    pc = _get_partial_concordance(comparables_perf_b[b][criterion],
                                                  comparables_perf_a[a][criterion],
                                                  criterion,)
                    partial_concordances[b][a][criterion] = pc
    # aggregate partial concordances
    aggregated_concordances = Vividict()
    for a in comparables_a:
        for b in comparables_b:
            aggregated_concordances[a][b] = _get_aggregated_concordance(a, b)
            if two_way_comparison:
                aggregated_concordances[b][a] = _get_aggregated_concordance(b, a)
    return aggregated_concordances


def main():
    try:
        args = docopt(__doc__, version=__version__)
        output_dir = None
        input_dir, output_dir = get_dirs(args)
        filenames = [
            # every tuple below == (filename, is_optional)
            ('alternatives.xml', False),
            ('classes_profiles.xml', True),
            ('criteria.xml', False),
            ('method_parameters.xml', False),
            ('performance_table.xml', False),
            ('profiles_performance_table.xml', True),
            ('weights.xml', False),
        ]
        params = [
            'alternatives',
            'categories_profiles',
            'comparison_with',
            'criteria',
            'performances',
            'pref_directions',
            'profiles_performance_table',
            'thresholds',
            'weights',
        ]
        d = get_input_data(input_dir, filenames, params)

        # getting the elements to compare
        comparables_a = d.alternatives
        comparables_perf_a = d.performances
        if d.comparison_with in ('boundary_profiles', 'central_profiles'):
            # central_profiles is a dict, so we need to get the keys
            comparables_b = [i for i in d.categories_profiles]
            comparables_perf_b = d.profiles_performance_table
        else:
            comparables_b = d.alternatives
            comparables_perf_b = d.performances

        concordance = get_concordance(comparables_a, comparables_perf_a,
                                      comparables_b, comparables_perf_b,
                                      d.criteria, d.thresholds,
                                      d.pref_directions, d.weights)

        # serialization etc.
        if d.comparison_with in ('boundary_profiles', 'central_profiles'):
            mcda_concept = 'alternativesProfilesComparisons'
        else:
            mcda_concept = None
        comparables = (comparables_a, comparables_b)
        xmcda = comparisons_to_xmcda(concordance, comparables,
                                     mcda_concept=mcda_concept)
        write_xmcda(xmcda, os.path.join(output_dir, 'concordance.xml'))
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
