# coding=utf-8
# 文章评分系统

import time
import redis

ONE_WEEK_IN_SECONDS = 7 * 84600  # 一周的秒数
VOTE_SCORE = 432  # 文章评分常量


def article_vote(conn, user, article):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < cutoff:
        return
    article_id = article.partition(':')[-1]
    if conn.sadd('voted:' + article_id, user):
        conn.zincrby('score:', article, VOTE_SCORE)
        conn.hincrby(article, 'votes', 1)


# main方法
def main():
    conn = redis.Redis()
    user = "zhangsan"
    article = "article"
    article_vote(conn, user, article)


main()
