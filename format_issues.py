import re
import pandas as pd

from pathlib import Path
from string import Template

TITLE_FIELD_WIDTH = 75

translation = str.maketrans({"-":  r"\-",
                             "]":  r"\]",
                             "\\": r"\\",
                             "^":  r"\^",
                             "$":  r"\$",
                             "&":  r"\&",
                             "*":  r"\*"})

def load_issues_csv(filename):
    names = ['id', 'state', 'title', 'labels', 'date']
    issues_df = pd.read_csv(filename, sep=';', names=names)

    #issues_df.set_index(issues_df['id'], inplace=True)
    issues_df['date']= pd.to_datetime(issues_df['date'], format='%Y-%m-%d %H:%M:%S +0000 %Z')
    issues_df['date'] = issues_df['date'].dt.tz_convert('Europe/Zurich')

    return issues_df


def print_summary(issues_df):
    action_template = '{:<4} {:<7} {:<75} {:<20} {:>15} {:>10}'
    header = action_template.format('ID', 'State', 'Title', 'Responsible Person', 'Category', 'Date')

    print(header)

    for i, row in issues_df.iterrows():
        labels = row['labels'].split()
        label_string = 'multiple' if len(labels) > 1 else labels[0]
        date_string = row['date'].strftime('%Y-%m-%d')
        resp_person = "P. Responsible"

        title = row['title']

        has_remainder = True
        if len(title) > TITLE_FIELD_WIDTH:
            title_part = title[:TITLE_FIELD_WIDTH]
            title_remainder = title[TITLE_FIELD_WIDTH:]
        else:
            title_part = title
            has_remainder = False

        print(action_template.format(row['id'], row['state'], title_part, 
                                     resp_person, label_string, date_string))


        while(has_remainder):
            if len(title_remainder) > TITLE_FIELD_WIDTH:
                title_part = title_remainder[:TITLE_FIELD_WIDTH]
                title_remainder = title_remainder[TITLE_FIELD_WIDTH:]
            else:
                title_part = title_remainder
                has_remainder = False

            print(action_template.format('', '', title_remainder, 
                                        '', '', ''))

def make_summary_table(issues_df, state='open'):
    if state == 'open':
        issues_df = issues_df[issues_df['state'] == 'OPEN']
    elif state == 'closed':
        issues_df = issues_df[issues_df['state'] == 'CLOSED']
    elif state == 'all':
        pass
    else:
        raise ValueError('Unknown state: {}'.format(state))

    latex_table = ("\\begin{longtable}"
                   "{|m{0.8cm} | m{6cm} | m{3.5cm} | m{2.5cm} | m{2cm}|}\n"
                   "\\hline\n"
                   "ID & Title & Responsible Person & Category & Date \\\\\n"
                   "\\hline\n")

    latex_table_template = "\#{} & {} & {} & {} & {} \\\\ \n"

    issues_repo = 'https://github.com/fcccollab/fcc-action-items/issues/'
    for i, row in issues_df.iterrows():
        issue_id = r'\href{{{}{}}}{{{}}}'.format(issues_repo, row['id'], row['id'])

        labels = row['labels'].split()
        label_string = 'multiple' if len(labels) > 1 else labels[0]
        date_string = row['date'].strftime('%Y-%m-%d')

        title = ''.join(row['title'].split('-')[:-1]).strip().translate(translation)
        resp_person = str(row['title'].split('-')[-1]).strip()
        latex_table += latex_table_template.format(issue_id, title, 
                                                   resp_person, label_string, date_string)
        latex_table += '\\hline\n'

    latex_table+="\\end{longtable}\n"
    #print(latex_table)

    return latex_table


def replace_latex_template(issues_df, latex_template='latex_template/action-item-list.tpl', outdir='latex_build'):
    open_items = make_summary_table(issues_df, state='open')
    closed_items = make_summary_table(issues_df, state='closed')

    with open(latex_template, 'r') as infile:
        template_string = Template(infile.read())

    replace_dict = {'__OPENITEMS__': open_items, 
                             '__CLOSEDITEMS__': closed_items,}

    rendered_string = template_string.safe_substitute(**replace_dict)

    outfilename = Path(outdir) / Path(latex_template).name.replace('.tpl', '.tex')

    with open(outfilename, 'w') as outfile:
        outfile.write(rendered_string)
    






def main():
    filename = 'issues.csv'
    issues_df = load_issues_csv(filename)
    replace_latex_template(issues_df)
    # print_summary(issues_df)
    #make_summary_table(issues_df, state='open')
    #print('\n\n')
    #make_summary_table(issues_df, state='closed')

if __name__ == '__main__':
    main()