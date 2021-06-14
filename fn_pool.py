# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 17:59:12 2021

@author: tentative-user
"""

def prnwrit(log_f, stuff=''):
    """Print stuff and also write stuff to log_f if it is opened."""
    print(stuff)
    try:
        log_f.write(stuff + '\n')
    except NameError:
        print('**[Write Error: Cannot write to "log_f".]**')


def sl2bxl(sl_str):
    """Slash to backslash: replaces all slashes by backslashes."""
    return sl_str.replace('/', '\\')


def core_f_nam(f_nam):
    """Return file name without path and file extension."""
    norm_f_nam = sl2bxl(f_nam)
    try:
        last_bsl_pos = norm_f_nam.rindex('\\')
    except ValueError:
        last_bsl_pos = 0
    try:
        last_dot_pos = norm_f_nam.rindex('.', last_bsl_pos)
    except ValueError:
        last_dot_pos = len(norm_f_nam)
    return norm_f_nam[last_bsl_pos + 1:last_dot_pos]


def script_intro():
    """Introductory line with script version and script header."""
    from datetime import datetime
    from sys import argv

    sta_t = str(datetime.now())
    print('\nScript version: "' + str(sl2bxl(argv[0])) + '".\n')
    pout = '\n===== Starting script =====\n' + sta_t
    pout += '\n===========================\n'
    print(pout)
    return pout


def script_exit_lite(lf, starttime):
    """Note running time, finish and close log file and exit script."""
    import time
    from datetime import datetime, timedelta
    from sys import exit
    end_time = time.monotonic()
    sto_t = str(datetime.now())
    time_string = str(timedelta(seconds=end_time - starttime))
    pout = '\nCurrent script execution time (hh:mm:ss) = ' + time_string
    prnwrit(lf, pout)
    pout = '\n===== Stopping script =====\n' + sto_t
    pout += '\n===========================\n'
    prnwrit(lf, pout)
    try:
        lf.close()
    except NameError:
        pass
    exit()


def s_trim(text, recursive=False, greedy=False):
    """
    Symmetrical trimming of selected special characters ('+*:_~%|=$#?"')
    from beginning and end of each word in splitted text. Plain and recursive
    version. Examples:
                           s_trim('+++this+++') returns '++this++'
                           s_trim('+++this+++', True) returns 'this'.
                           
    With "greedy" variant those characters, as well as {}, [], ()
    pairs can be trimmed also from beginnings and ends of larger n-grams, e.g.
                           s_trim('{{science-fiction fandom}},', True, True)
                  returns
                           'science-fiction fandom,'
                  while
                           s_trim('{{science-fiction fandom}},', False, True)
                  returns                           
                           '{science-fiction fandom},'.
    """
    split_text = text.split()
    new_word_list = []
    fore_chars = '+:_~%|=$#?"{[('
    back_chars = '+:_~%|=$#?"}])'
    for i in range(len(split_text)):
        old = ''
        new = ''
        add_trail = False
        old = split_text[i]
        if old[-1] in '.,:;!?' and old[0] != old[-1]:
            trail = old[-1]
            add_trail = True
            old = old[:-1]
        for j in range(len(fore_chars)):
            if old[0] == fore_chars[j] and old[-1] == back_chars[j]\
            and len(old) > 2:
                while old[0] == fore_chars[j] and old[-1] == back_chars[j]\
                and len(old) > 2:
                    new = old[1:-1]
                    if not recursive:
                        break
                    else:
                        old = new
                if add_trail:
                    new += trail
                new_word_list.append([split_text[i], new])
                break
    for n in new_word_list:
        text = text.replace(n[0], n[1])
    if not greedy:
        return text
    split_tx_g = text.split()
    new_wrd_lst_g, single_chars, multis = [], [], []
    n = 0
    for i in range(len(split_tx_g)):
        if split_tx_g[i][0] in fore_chars:
            idx = fore_chars.index(split_tx_g[i][0])
            n = i
            c = 0
            spl_in_for = split_tx_g[n][c] in fore_chars
            while spl_in_for and c < len(split_tx_g[n]) - 1:
                c += 1
                spl_in_for = split_tx_g[n][c] in fore_chars
            if c == 0:
                try:
                    ap = [split_tx_g[n-1], split_tx_g[n], split_tx_g[n+1]]
                    single_chars.append(ap)
                except IndexError:
                    ap = [split_tx_g[n-1], split_tx_g[n], '*EoF*']
                    single_chars.append(ap)
            elif c == 1:
                new_wrd_lst_g.append([split_tx_g[i], split_tx_g[i][1:]])
                n += 1
                try:
                    s_non_eq_b = split_tx_g[n][-1] != back_chars[idx]
                    while s_non_eq_b and n < len(split_tx_g) - 1:
                        n += 1
                        s_non_eq_b = split_tx_g[n][-1] != back_chars[idx]
                    new_wrd_lst_g.append([split_tx_g[n], split_tx_g[n][:-1]])
                except IndexError:
                    pass
            else:  # c > 1
                try:
                    ap = [split_tx_g[n-1], split_tx_g[n], split_tx_g[n+1]]
                    multis.append(ap)
                except IndexError:
                    try:
                        _ = split_tx_g[n-1]
                    except IndexError:
                        try:
                            ap = ['*BoF*', split_tx_g[n], split_tx_g[n+1]]
                            multis.append(ap)
                        except IndexError:
                            ap = [split_tx_g[n-1], split_tx_g[n], '*EoF*']
                            multis.append(ap)
                try:
                    fidx = fore_chars.index(split_tx_g[n][1])
                except ValueError:
                    fidx = -3
                try:    
                    bidx = back_chars.index(split_tx_g[n][-1])
                except ValueError:
                    bidx = -1
                if fidx == bidx:
                    new_wrd_lst_g.append([split_tx_g[n], split_tx_g[n][2:-1]])
                else:  # problem with bidx
                    new_wrd_lst_g.append([split_tx_g[n], split_tx_g[n][2:]])
    text_g = ' '.join(split_tx_g)
    for n in new_wrd_lst_g:
        text_g = text_g.replace(n[0], n[1])
    return (text_g, single_chars, multis)
