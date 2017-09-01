# coding=utf-8
# 文章评分系统

import time
import redis

ONE_WEEK_IN_SECONDS = 7 * 84600  # 一周的秒数
VOTE_SCORE = 432  # 文章评分常量
ARTICLES_PER_PAGE = 20  # 每页返回的数据量


# 投票
def article_vote(conn, user, article):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < cutoff:
        return
    article_id = article.partition(':')[-1]
    if conn.sadd('voted:' + article_id, user):
        conn.zincrby('score:', article, VOTE_SCORE)
        conn.hincrby(article, 'votes', 1)


# 创建文章
def post_article(conn, user, title, link):
    article_id = str(conn.incr('article:'))
    voted = 'voted:' + article_id
    conn.sadd(voted, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS)

    now = time.time()
    article = 'article:' + article_id
    conn.hmset(article, {
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1
    })
    conn.zadd('score:', article, now + VOTE_SCORE)
    conn.zadd('time:', article, now)
    return article_id


# 获取文章
def get_articles(conn, page, order='score:'):
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1
    ids = conn.zrevrange(order, start, end)
    articles = []
    for i in ids:
        article_data = conn.hgetall(i)
        article_data['id'] = i
        articles.append(article_data)
    return articles


# main方法
def main():
    conn = redis.Redis()
    user = "zhangsan"
    article = "zhangsan's blog"
    # post_article(conn, user, article, "http://baidu.com/aaa.txt")
    article_vote(conn, user, article + ":1")
    articles = get_articles(conn, 1)
    for a in articles:
        print a


main()
