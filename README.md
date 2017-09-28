# log_analysis
Command line application that interfaces with the news
database to give a report on a few FAQs

To run, enter command:
 `python log_analysis.py`

The results will be printed to the console. No views are used. An example of the output is provided in output.txt.

**_What are the most popular three articles of all time?_**
Method:
 - count the log table's views grouped by path
 - where the path starts with 'article'
 - join on the path col with the article table's slug col
 - order by the most views and limited to 3

**_What are the most popular article authors of all time?_**
Method:
 - count the log table's views grouped by path
 - where the path starts with 'article'
 - join with the articles table on the slug
 - join with the authors table on the id
 - group by the author name
 - and order with the most views at the top

**_On which days did more than 1% of requests lead to errors?_**
Method:
 - Truncate the time column to be just date, and count the requests grouped by day in the log table
 - join with another log query, this one also truncating the time column to the date, and only counting queries that resulted in an error in the status column; these are also grouped by day
 - They are joined on the date (truncated time columns)
 - And filtered to only days where the portion of total requests that resulted in error is greater than 0.01.
