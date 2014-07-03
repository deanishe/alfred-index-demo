# Alfred/sqlite demo workflow #

Search the index of Project Gutenberg ebooks from Alfred.

Demonstrates the usage of sqlite full-text search in a workflow and the blinding speed this offers.

## Usage ##

- `books <query>` — Search the Gutenberg catalogue for `<query>`

You can use wildcard, boolean and field-specific queries:

- `books kant AND critique`
- `books author:kant`
- `books criti*`
- `books title:criti* AND author:kant`
