import progressbar
import argparse
import radiko as R
import search as S

def main():
    parser = argparse.ArgumentParser(
        description='Get a program list and get all programs that interested in.')
    parser.add_argument('url', metavar='URL', type=str, nargs=1, 
                        help='API URL')
    parser.add_argument('--keyword', type=str, nargs=1, default=[''],
                        help='Keyword to search for')
    parser.add_argument('--output', type=bool, default=True,
                        help='if a csv file of output is needed')
    parser.add_argument('--save', type=str, default='output/',
                        help='specify the save path')
    args = parser.parse_args()
    mapping = {'No Live': 
                {
                'duration': 0, 
                'start_time': '--', 
                'end_time': '--', 
                'info': '--',
                'pfm': '--',
                'url': '--',
                'keywords': []
                }
        }
    df, mapping = R.radiko(args.url[0], mapping)
    S.search(df, args.keyword[0], mapping, args.output, args.save)

if __name__ == '__main__':
    main()