from InstagramAPI import InstagramAPI
import time
import random
import argparse
import sys

def GetAllFollowing(bot, user_id):
    following = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = bot.getUserFollowings(user_id, maxid=next_max_id)
        following.extend(bot.LastJson.get('users', []))
        next_max_id = bot.LastJson.get('next_max_id', '')
    following = set([_['pk'] for _ in following])
    return following

def GetAllFollowers(bot, user_id):
    followers = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = bot.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(bot.LastJson.get('users', []))
        next_max_id = bot.LastJson.get('next_max_id', '')
    followers = set([_['pk'] for _ in followers])
    return followers

if __name__ == '__main__':

    # parse cmd line args
    parser = argparse.ArgumentParser(description='Batch unfollow users on Instagram')
    parser.add_argument('username', help='Your Instagram username')
    parser.add_argument('password', help='Your Instagram password')

    parser.add_argument('-u', '--num_unfollows', type=int, default=50,
                        help='Number of users to unfollow')
    parser.add_argument('-t', '--max_delay', type=int, default=10,
                        help='Maximum amount of seconds to wait before the script unfollows the next person. Use caution, as too little of a delay can flag you to Instagram')

    args = parser.parse_args()

    # get credentials and authenticate
    ig = InstagramAPI(args.username, args.password)

    # successful login handler
    success = ig.login()
    if not success:
        print('INSTAGRAM LOGIN FAILED')
        sys.exit()

    # fetch your own primary key
    ig.getSelfUsernameInfo()
    self_id = ig.LastJson['user']['pk']

    # loop through json for followers/following
    followers = GetAllFollowers(ig, self_id)
    following = GetAllFollowing(ig, self_id)
    print('- following {} users'.format(len(following)))
    print('- followed by {} users'.format(len(followers)))

    # loop through following users w/ random delay
    for _ in list(following)[:min(len(following), args.num_unfollows)]:
        ig.getUsernameInfo(str(_))
        print('  - unfollowing user {}'.format(ig.LastJson['user']['username']))
        ig.unfollow(str(_))
        time.sleep(random.uniform(1, args.max_delay))
