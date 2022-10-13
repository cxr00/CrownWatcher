# CrownWatcher

CrownWatcher is a simple scraping tool which grabs article headlines across every category and subcategory of the Daily Mail.

Just clone, set your directory to `CrownWatcher`, and run:

```
python -m jewel
```

It will scrape and organise headlines like so:

```
archive
|-year
  |-month
    |-day
      |-category
        |-subcategory
        |-subcategory
        |-subcategory
        |-subcategory
        ...
```

Note that there is sometimes category overlap. For example, Meghan Markle shows up under U.K. and U.S. Showbiz categories.
