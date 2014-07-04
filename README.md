# Alfred/sqlite demo workflow #

Search the index of Project Gutenberg ebooks from Alfred.

![](https://github.com/deanishe/alfred-index-demo/raw/master/demo.gif "")

Demonstrates the usage of sqlite full-text search in a workflow and the blinding speed this offers.

## Usage ##

- `books <query>` — Search the Gutenberg catalogue for `<query>`

You can use wildcard, boolean and field-specific queries:

- `books kant AND critique`
- `books author:kant`
- `books criti*`
- `books title:criti* AND author:kant`

## How fast? ##

Here's some sample log output using [a database of ~45,000 ebooks](https://raw.githubusercontent.com/deanishe/alfred-index-demo/master/src/books.tsv) from [Project Gutenberg](http://www.gutenberg.org/):

```
11:10:53 background.py:220 DEBUG    Executing task `indexer` in background...
11:10:53 index.py:43 INFO     Creating index database
11:10:53 index.py:56 INFO     Updating index database
11:10:53 books.py:110 INFO     0 results for `im` in 0.001 seconds
11:10:53 books.py:110 INFO     0 results for `imm` in 0.001 seconds
11:10:53 books.py:110 INFO     0 results for `imma` in 0.001 seconds
11:10:55 index.py:73 INFO     44549 items added/updated in 2.19 seconds
11:10:55 books.py:110 INFO     0 results for `imman` in 1.710 seconds
11:10:55 index.py:80 INFO     Index database update finished
11:10:55 background.py:270 DEBUG    Task `indexer` finished
11:10:55 books.py:110 INFO     15 results for `immanuel` in 0.002 seconds
11:10:58 books.py:110 INFO     100 results for `p` in 0.017 seconds
11:10:59 books.py:110 INFO     4 results for `ph` in 0.002 seconds
11:10:59 books.py:110 INFO     0 results for `phi` in 0.002 seconds
11:11:00 books.py:110 INFO     9 results for `phil` in 0.002 seconds
11:11:00 books.py:110 INFO     3 results for `philo` in 0.002 seconds
11:11:00 books.py:110 INFO     0 results for `philos` in 0.001 seconds
11:11:00 books.py:110 INFO     0 results for `philosp` in 0.001 seconds
11:11:01 books.py:110 INFO     0 results for `philospo` in 0.001 seconds
11:11:01 books.py:110 INFO     0 results for `philosp` in 0.001 seconds
11:11:02 books.py:110 INFO     0 results for `philos` in 0.002 seconds
11:11:02 books.py:110 INFO     0 results for `philoso` in 0.001 seconds
11:11:02 books.py:110 INFO     0 results for `philosoh` in 0.003 seconds
11:11:02 books.py:110 INFO     0 results for `philosohp` in 0.002 seconds
11:11:02 books.py:110 INFO     0 results for `philosohpy` in 0.002 seconds
11:11:03 books.py:110 INFO     0 results for `philosohp` in 0.002 seconds
11:11:03 books.py:110 INFO     0 results for `philosoh` in 0.001 seconds
11:11:03 books.py:110 INFO     0 results for `philoso` in 0.001 seconds
11:11:03 books.py:110 INFO     0 results for `philosop` in 0.001 seconds
11:11:03 books.py:110 INFO     0 results for `philosopj` in 0.001 seconds
11:11:03 books.py:110 INFO     0 results for `philosopjy` in 0.002 seconds
11:11:04 books.py:110 INFO     0 results for `philosopj` in 0.002 seconds
11:11:04 books.py:110 INFO     0 results for `philosop` in 0.002 seconds
11:11:04 books.py:110 INFO     0 results for `philosoph` in 0.002 seconds
11:11:04 books.py:110 INFO     100 results for `philosophy` in 0.012 seconds
11:11:08 books.py:110 INFO     100 results for `philosophy ` in 0.007 seconds
11:11:09 books.py:110 INFO     2 results for `philosophy t` in 0.002 seconds
11:11:09 books.py:110 INFO     0 results for `philosophy ti` in 0.002 seconds
11:11:10 books.py:110 INFO     0 results for `philosophy tit` in 0.002 seconds
11:11:11 books.py:110 INFO     0 results for `philosophy titl` in 0.002 seconds
11:11:11 books.py:110 INFO     0 results for `philosophy title` in 0.002 seconds
11:11:11 books.py:110 INFO     100 results for `philosophy title:` in 0.007 seconds
11:11:11 books.py:110 INFO     0 results for `philosophy title:t` in 0.002 seconds
11:11:11 books.py:110 INFO     0 results for `philosophy title:th` in 0.002 seconds
11:11:11 books.py:110 INFO     72 results for `philosophy title:the` in 0.010 seconds
11:11:12 books.py:110 INFO     40 results for `philosophy a` in 0.006 seconds
11:11:13 books.py:110 INFO     0 results for `philosophy au` in 0.002 seconds
11:11:13 books.py:110 INFO     0 results for `philosophy aut` in 0.002 seconds
11:11:13 books.py:110 INFO     0 results for `philosophy auth` in 0.002 seconds
11:11:13 books.py:110 INFO     0 results for `philosophy autho` in 0.002 seconds
11:11:13 books.py:110 INFO     0 results for `philosophy author` in 0.002 seconds
11:11:14 books.py:110 INFO     100 results for `philosophy author:` in 0.009 seconds
11:11:14 books.py:110 INFO     0 results for `philosophy author:k` in 0.002 seconds
11:11:14 books.py:110 INFO     0 results for `philosophy author:ka` in 0.002 seconds
11:11:14 books.py:110 INFO     0 results for `philosophy author:kan` in 0.002 seconds
11:11:15 books.py:110 INFO     0 results for `philosophy author:kant` in 0.002 seconds
11:11:18 books.py:110 INFO     3 results for `philosophy author:a` in 0.003 seconds
11:11:18 books.py:110 INFO     0 results for `philosophy author:ar` in 0.002 seconds
11:11:19 books.py:110 INFO     0 results for `philosophy author:ari` in 0.002 seconds
11:11:19 books.py:110 INFO     0 results for `philosophy author:aris` in 0.002 seconds
11:11:20 books.py:110 INFO     0 results for `philosophy author:arist` in 0.002 seconds
11:11:20 books.py:110 INFO     0 results for `philosophy author:aristo` in 0.002 seconds
11:11:20 books.py:110 INFO     0 results for `philosophy author:aristot` in 0.002 seconds
11:11:20 books.py:110 INFO     0 results for `philosophy author:aristotl` in 0.002 seconds
11:11:20 books.py:110 INFO     0 results for `philosophy author:aristotle` in 0.002 seconds
11:11:22 books.py:110 INFO     15 results for `author:aristotle` in 0.002 seconds
```