from linkedin_api import Linkedin
import sys
import argparse
import os
import csv
import pandas as pd

CONPENIES_FILE = 'compenies.csv'
EXPORT_FILE = 'exported_jobs.csv'
TEXT_FILE_FORMAT = 'txt'
DEFAULT_DIR = '.\\'


def split_list(alist, parts=1):
    length = len(alist)
    return [alist[i*length // parts: (i+1)*length // parts]
            for i in range(parts)]


def export_to_csv(output, job_lst):
    keys = job_lst[0].keys()

    if output is None:
        output = DEFAULT_DIR

    if file_path(output + EXPORT_FILE, 'csv'):
        ids = get_list_by_cols(output + EXPORT_FILE, ['id'])

        with open(output + EXPORT_FILE, 'a', encoding="utf-8-sig", newline='') as output_file:
            writer_object = csv.DictWriter(output_file, keys)

            for job in job_lst:
                if job['id'] not in ids:
                    writer_object.writerow(job)
            output_file.close()
    else:
        with open(output + EXPORT_FILE, 'w', encoding="utf-8-sig", newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(job_lst)
            output_file.close()


def job_filter_wordlist(wordList, title):
    ret = True
    if wordList is not None:
        ret = False
        for word in wordList:
            if word in title:
                ret = True
    return ret


def job_filter_blacklist(blackList, title):
    ret = True
    if blackList is not None:
        for word in blackList:
            if word in title and ret is True:
                ret = False
    return ret


def get_list_by_cols(file_path, cols):
    df = pd.read_csv(file_path, usecols=cols)
    return [str(company[0]).split('.')[0] for company in df.values.tolist()]


def dir_path(ditPath):
    if os.path.isdir(ditPath):
        return ditPath
    else:
        raise NotADirectoryError(ditPath)


def file_path(filePath, file_format):
    if os.path.isfile(filePath) and filePath.endswith('.' + file_format):
        return filePath
    else:
        return False


def txt_to_list(path):
    my_file = open(path, "r")
    data = my_file.read()
    return data.split("\n")


def getArgs(argv):
    parser = argparse.ArgumentParser("Start-up Nation Job Finder")
    parser.add_argument('-u', '--username', required=True,
                        help="Linkedin username")
    parser.add_argument('-p', '--password', required=True,
                        help="Linkedin password")
    parser.add_argument('-wl', '--wordlist', help="world list filter")
    parser.add_argument('-bl', '--blacklist', help="black list filter")
    parser.add_argument(
        '-o', '--output', help="output file path", type=dir_path)
    args = parser.parse_args()

    wordlist = None
    blacklist = None

    if args.blacklist is not None:
        blacklist = txt_to_list(args.blacklist)
        if not file_path(args.blacklist, TEXT_FILE_FORMAT):
            parser.error('blacklist - file not found')

    if args.wordlist is not None:
        wordlist = txt_to_list(args.wordlist)
        if not file_path(args.blacklist, TEXT_FILE_FORMAT):
            parser.error('wordlist - file not found')

    username = args.username
    password = args.password
    output = args.output

    return username, password, wordlist, blacklist, output


def main(argv):
    [username, password, wordlist, blacklist, output] = getArgs(argv)

    api = None
    try:
        print("Connecting...")
        api = Linkedin(username, password)
    except:
        print("The username or password is incorrect.")

    # connected successfully
    if api:
        job_lst = []
        print("Connected successfully.\nSearching...")

        comp = split_list(get_list_by_cols(CONPENIES_FILE, ['Linkedin']), 10)

        for compenies in comp:
            jobs = api.search_jobs(companies=compenies, location_name="Israel")

            df = pd.read_csv(CONPENIES_FILE, usecols=[
                             'Name', 'Linkedin', 'Funding Stage'])

            for job in jobs:
                id = str(job['dashEntityUrn']).split(':')[-1]
                title = str(job['title'])
                remote = job['workRemoteAllowed']
                link = "https://www.linkedin.com/jobs/search/?currentJobId=" + id
                location = job['formattedLocation']
                company = str(job['companyDetails']['company']).split(':')[-1]

                pos = df.loc[df['Linkedin'] == company]
                company_name = pos.values.tolist()[0][0]
                funding_stage = pos.values.tolist()[0][1]

                if job_filter_wordlist(wordlist, title) and job_filter_blacklist(blacklist, title):
                    job_dic = {'Check': '', 'ID': id, 'Company': company_name,
                               'Title': title, 'Location': location, 'Link': link, 'Funding Stage': funding_stage, "Is Remote": remote}
                    job_lst.append(job_dic)

        export_to_csv(output, job_lst)
        print("Done.")
        None


if __name__ == "__main__":
    main(sys.argv[1:])
