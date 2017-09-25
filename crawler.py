from inscrawler import InsCrawler
import sys
import argparse

# ins_crawler = InsCrawler()
# print(ins_crawler.get_user_posts('cal_foodie'))
# print(ins_crawler.get_user_posts('instagram'))
# print(ins_crawler.get_user_posts('1d.legendary.updates'))
# print(len(ins_crawler.get_latest_posts_by_tag('foodie', 10)))

# python crawler.py posts -u cal_foodie -n 100 -o /tmp/aa
# python crawler.py profile -u cal_foodie -o /tmp/aa
# python crawler.py hashtag taiwan -o /tmp/aa


def usage():
    return '''
        python crawler.py posts -u cal_foodie -n 100 -o ./output
        python crawler.py profile -u cal_foodie -o ./output
        python crawler.py hashtag taiwan -o ./output
    '''


def get_posts_by_user(username, number=None):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_posts(username, number)


def get_profile(username):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_profile(username)


def get_posts_by_hashtag(tag, number):
    ins_crawler = InsCrawler()
    return ins_crawler.get_latest_posts_by_tag(tag, number)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instagram Crawler',
                                     usage=usage())
    parser.add_argument('mode',
                        help='options: [posts, profile, hashtag]')
    parser.add_argument('-n', '--number',
                        type=int, default=100,
                        help='number of returned posts')
    parser.add_argument('-u', '--username',
                        help='instagram\'s username')
    parser.add_argument('-t', '--tag',
                        help='instagram\'s tag name')
    parser.add_argument('-o', '--output', help='output file name(json format)')
    args = parser.parse_args()

    if args.mode == 'posts':
        arg_required('username')
        print(get_posts_by_user(args.username, args.number))
    elif args.mode == 'profile':
        arg_required('username')
        print(get_profile(args.username))
    elif args.mode == 'hashtag':
        arg_required('tag')
        print(get_posts_by_hashtag(args.tag, args.number))
    else:
        usage()

    # print(ins_crawler.get_user_posts('cal_foodie'))