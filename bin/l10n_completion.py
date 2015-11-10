#!/usr/bin/env python

"""

Goes through locale files and gives a breakdown of percentage
translated by app for each locale.

Requires:

* polib

For usage help, type::

   $ python l10n_completion.py --help

"""

import datetime
import json
import os
import sys

import click
import polib


def get_language(fn):
    """Given a filename, returns the locale it applies to"""
    # FIXME - this expects the fn to be '.../XX/LC_MESSAGES/django.po'
    return fn.split(os.sep)[-3]


def get_locale_files(localedir):
    """Given a locale dir, returns a list of all .po files in that tree"""
    po_files = []
    for root, dirs, files in os.walk(localedir):
        po_files.extend(
            [os.path.join(root, fn) for fn in files
             if fn.endswith('.po')])

    return po_files


def get_completion_data_for_file(fn):
    """Parses .po file and returns completion data for that .po file

    :returns: dict with keys total, translated and percent

    """
    app_to_translations = {}

    lang = get_language(fn)

    try:
        pofile = polib.pofile(fn)
    except IOError as ioe:
        print 'Error opening file: {fn}'.format(fn=fn)
        print ioe.message
        return 1

    for poentry in pofile:
        if poentry.obsolete:
            continue

        for occ in poentry.occurrences:
            path = occ[0].split(os.sep)
            if path[0] == 'fjord':
                path = path[1]
            else:
                path = 'vendor/' + path[2]
            app_to_translations.setdefault(path, []).append(poentry)

    all_total = 0
    all_translated = 0
    all_untranslated_words = 0

    data = {}
    for app, tr_list in app_to_translations.items():
        total = len(tr_list)
        translated = len([tr for tr in tr_list if tr.translated()])
        untranslated_words = sum(
            [len(tr.msgid.split()) for tr in tr_list if not tr.translated()]
        )
        data[app] = {
            'total': total,
            'translated': translated,
            'untranslated_words': untranslated_words
        }

        all_total += total
        all_translated += translated
        all_untranslated_words += untranslated_words

    return {
        lang: {
            'total': all_total,
            'translated': all_translated,
            'untranslated_words': all_untranslated_words,
            'apps': data
        }
    }


def merge_trees(data, new_data):
    """Merges values from second tree into the first

    This takes care to add values of the same key where appropriate.

    """
    for key, val in new_data.items():
        if isinstance(val, dict):
            if key not in data:
                data[key] = new_data[key]
            else:
                merge_trees(data[key], new_data[key])

        else:
            if key not in data:
                data[key] = val
            else:
                data[key] = data[key] + val


def calculate_percents(data):
    """Traverses a tree and calculates percents at appropriate levels"""
    # calculate the percent for this node if appropriate
    if 'translated' in data and 'total' in data:
        total = float(data['total'])
        translated = float(data['translated'])
        data['percent'] = float(100.0 * translated / total)

    # traverse the tree to calculate additional percents
    for key, val in data.items():
        if isinstance(val, dict):
            calculate_percents(val)


def get_completion_data(locale_files):
    """Given a list of .po files, returns a dict of all completion data

    :returns: dict: locale -> completion data

    """
    data = {}

    for fn in locale_files:
        new_data = get_completion_data_for_file(fn)
        merge_trees(data, new_data)

    calculate_percents(data)

    return data


@click.command()
@click.option('--output', help='Abs path for output .json file')
@click.option('--locales', help='Abs path for locales/ dir')
@click.option('--truncate', default=0, help='Days to truncate results')
def main(output, locales, truncate):
    # Get list of locales dirs
    locale_files = get_locale_files(locales)

    # Generate completion data
    created = datetime.date.today().strftime('%Y-%m-%d')
    locales = get_completion_data(locale_files)

    # Merge it with historical data
    if os.path.exists(output):
        with open(output, 'rb') as fp:
            data = json.load(fp)

        # Figure out if we should replace an item with the updated data.
        for item in data:
            if item['created'] == created:
                item['locales'] = locales
                break
        else:
            data.append({
                'created': created,
                'locales': locales
            })

    else:
        data = [{
            'created': created,
            'locales': locales
        }]

    # Truncate if needed
    if truncate and len(data) > truncate:
        print 'Truncating ...'
        data = data[len(data) - truncate:]

    # Save it to disk
    with open(output, 'wb') as fp:
        json.dump(data, fp, indent=2)


if __name__ == '__main__':
    sys.exit(main())
