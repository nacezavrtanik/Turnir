"""Module for creating a user interface for the TIMELESS tournament format."""

import string
import textwrap
import time
import datetime

from tabulate import tabulate

from config import RIGHT_MARGIN, INDENT, LARGE_INDENT, LINE_WIDTH, TIMELESS, GIT, YOUTUBE, BOLD_LINE
from config import PRELIMINARY_ROUNDS


text_wrapper = textwrap.TextWrapper(width=RIGHT_MARGIN, initial_indent=INDENT, subsequent_indent=INDENT)


def typewriter(text, delay=0.1, ignore_whitespaces=False):

    for character in text:
        print(character, sep='', end='', flush=True)
        if ignore_whitespaces and character == ' ':
            continue
        time.sleep(delay)


def print_centered_table(table, **kwargs):
    table = tabulate(table, **kwargs)
    rows = table.split('\n')
    max_row_length = max(map(len, rows))
    for row in rows:
        print(f'{row:<{max_row_length}}'.center(LINE_WIDTH))  # padded with ' ' for propper alignment when centered
    print()


def segment_initial():

    time.sleep(1.5)
    print('\n\n')
    typewriter(TIMELESS, delay=0.2, ignore_whitespaces=True)
    print(f'\n\n{GIT}')
    print(f'{YOUTUBE}\n')
    print(BOLD_LINE)
    print()
    time.sleep(1)
    typewriter(text_wrapper.fill('Welcome to Yugioh TIMELESS!'))
    print('\n')


def segment_format():
    description = '''Timeless je poseben turnirski format za štiri igralce.
Ti se pomerijo v treh predrundah (vsak z vsakim), nato
pa sledi še finalna runda. Nobena izmed teh ni časovno
omejena. Igra se z naborom štirih deckov, ki so med
igralce razdeljeni naključno. Po vsaki rundi se decki
ponovno naključno razdelijo med igralce, in sicer tako,
da v štirih rundah vsak igralec igra z vsakim izmed
štirih deckov natanko enkrat. Na voljo sta dva nabora
deckov:

 1) BASIC
 2) EXTRA'''
    output = text_wrapper.fill(description)

    print(output)
    print()


def segment_entry_fee():
    print()
    entry_fee = """Kaj pa prijavnina?
Ta gre v celoti v nagradni sklad in se na koncu glede
na dosežke razdeli nazaj med igralce.

 1) 5 €
 2) 10 €
 3) brez"""
    output = text_wrapper.fill(entry_fee)
    print(output)
    print()


def segment_duelists():
    print()
    print(text_wrapper.fill('Now enter duelist names.'))
    print()


def segment_start():
    tournament_date = str(datetime.datetime.today().date())
    print()
    print(BOLD_LINE)
    print()
    print(TIMELESS)
    print('Format'.center(LINE_WIDTH))
    print(tournament_date.center(LINE_WIDTH))
    print()
    print(BOLD_LINE)


def segment_pairings(pairings, round_):
    header = f' ROUND {round_ + 1} ' if round_ in (0, 1, 2) else ' FINAL ROUND '
    print(f'\n{header:-^{LINE_WIDTH}}\n\n')
    print_centered_table(pairings, tablefmt='plain')


def segment_standings(standings, round_):

    colalign = ('center', 'left', 'center') if round_ in PRELIMINARY_ROUNDS else ('center', 'left', 'center', 'center')
    print('\n')
    print_centered_table(standings, headers='keys', tablefmt='double_outline', colalign=colalign)


def segment_final():
    print(BOLD_LINE)
    input()


segments = {
    'initial': segment_initial,
    'format': segment_format,
    'entry_fee': segment_entry_fee,
    'duelists': segment_duelists,
    'start': segment_start,
    'pairings': segment_pairings,
    'standings': segment_standings,
    'final': segment_final
}


def is_string_of_integer(input_string):
    """Check if a string represents an integer."""
    try:
        int(input_string)
    except ValueError:
        return False
    return True


def supervised_input(prompt, conditions, options=None):
    """Require user input to satisfy specified conditions.

    The user is asked to provide an input value. If the provided value violates
    a specified condition, a tip for correcting the input is displayed, then
    the user is once again asked to provide an input value. This process is
    repeated until all specified conditions are satisfied.

    Parameters
    ----------
    prompt : str
        Description of desired input.
    conditions: str, list of str
        Names of conditions. A string can be passed if only one condition is
        specified, otherwise a list of strings.
    options: list of str, optional
        Valid input options if argument `conditions` is set to 'choose_from'.
        If `conditions` does not include 'choose_from', this argument is not
        relevant.

        As user input first is passed to the `string.capwords` function,
        strings in `options` should adhere to that same format as well.
        (defaults to None)

    Returns
    -------
    str
        User input, satisfying all conditions in `conditions`. Words are
        capitalised, consecutive whitespaces are replaced by a single
        whitespace, and leading and trailing whitespaces are removed.

    Notes
    -----
    User input is immediately passed to the `string.capwords` function, which
    capitalises words, strips leading and trailing whitespaces, and replaces
    consecutive whitespaces by a single whitespace. There are two reasons for
    this.

    (1) It is more convenient for the user. As all the checks will aplly to
    the modified string, user input will not be sensitive to choice of case
    nor to consecutive whitespaces.
    (2) It looks cleaner.

    Examples
    --------
    >>> supervised_input('Favourite integer: ', 'integer')
    Favourite integer: >? 3.14
    TIP: Enter an integer.
    Favourite integer: >? 3
    '3'

    >>> supervised_input('Your name: ',
    ...                  ['alphabetical', 'less_than_30_characters'])
    Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart 1756
    TIP: Use only letters and whitespaces.
    Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart
    TIP: Use less than 30 characters.
    Your name: >? Amadeus
    'Amadeus'

    >>> supervised_input('Do you like yes or no questions?',
    ...                 'choose_from', options=['Yes', 'No'])
    Do you like yes or no questions?>? I'm not sure
    TIP: Enter one of these: Yes, No.
    Do you like yes or no questions?>? No
    'No'
    """

    condition_checks = {
        'choose_from': lambda input_string: input_string in options,
        'alphabetical': lambda input_string: input_string.replace(' ', '').isalpha(),
        'less_than_25_characters': lambda input_string: len(input_string) < 25,
        'integer': lambda input_string: is_string_of_integer(input_string),
        'multiple_of_10': lambda input_string: int(input_string) % 10 == 0 and int(input_string) >= 0,
    }

    input_tips = {
        'choose_from': f'''Enter one of these: {options.__str__()[1: -1].replace("'", "")}.''',
        'alphabetical': 'Use only letters and whitespaces.',
        'less_than_25_characters': 'Use less than 25 characters.',
        'integer': 'Enter an integer.',
        'multiple_of_10': 'Pick a non-negative multiple of 10.',
    }

    if isinstance(conditions, str):
        conditions = [conditions]

    while True:

        typewriter(LARGE_INDENT + prompt)
        user_input = string.capwords(input())
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                print(f'\r{LARGE_INDENT}TIP: {input_tips.get(condition)}', flush=True)
                break

        if check:
            return user_input
