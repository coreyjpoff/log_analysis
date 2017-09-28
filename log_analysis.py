#!/usr/bin/env python3
from psycopg2 import connect
from decimal import Decimal

DBNAME = "news"


def findMostReadArticles():
    db = connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "select articles.title, articleCounts.views " +
        "from (select path, count(*) as views " +
        "from log group by path " +
        "having substring(path from 1 for 9)='/article/') articleCounts " +
        "join articles " +
        "on articleCounts.path = '/article/' || articles.slug " +
        "order by articleCounts.views desc " +
        "limit 3;"
    )
    articles = c.fetchall()
    db.close()
    return articles


def findMostReadAuthors():
    db = connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "select auth.name, sum(c.views) as totalViews " +
        "from (select path, count(*) as views " +
        "from log group by path " +
        "having substring(path from 1 for 9)='/article/') c " +
        "join articles art " +
        "on c.path = '/article/' || art.slug " +
        "join authors auth " +
        "on art.author = auth.id " +
        "group by auth.name " +
        "order by totalViews desc; "
    )
    authors = c.fetchall()
    db.close()
    return authors


def printMostRead(viewsTable):
    for row in viewsTable:
        print row[0] + " -- " + str(row[1]) + " views"


def findDaysWithErrors(percent):
    db = connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "select totalRequests.date, " +
        "(errors.errCount*100.0 / totalRequests.totalCount) " +
        "from (select date_trunc('day', time) as date, " +
        "count(*) as totalCount " +
        "from log " +
        "group by date_trunc('day', time)) totalRequests " +
        "join (select date_trunc('day', time) as date, " +
        "count(*) as errCount from log " +
        "where status = '404 NOT FOUND' " +
        "group by date_trunc('day', time) " +
        ") errors " +
        "on totalRequests.date=errors.date " +
        "where (errors.errCount*100.0 / totalRequests.totalCount) >= " +
        str(percent)
    )
    errDays = c.fetchall()
    db.close()
    return errDays


def printDaysWithErrors(errDays):
    for errDay in errDays:
        print (errDay[0].strftime('%B %d, %Y') + " -- " +
        str(round(errDay[1], 1)) + "% errors")


if __name__ == '__main__':
    print '\n\n\nWhat are the most popular three articles of all time?\n'
    articles = findMostReadArticles()
    printMostRead(articles)
    print '\n\n\nWho are the most popular article authors of all time?\n'
    authors = findMostReadAuthors()
    printMostRead(authors)
    print '\n\n\nOn which days did more than 1% of requests lead to errors?\n'
    errDays = findDaysWithErrors(1)
    printDaysWithErrors(errDays)
    print '\n'
