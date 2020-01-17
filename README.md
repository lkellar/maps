# Crime Map
An easy way to see recent 911 calls made in Fayetteville, Arkansas

## Awards
We made this project for the [2019 JB Hunt Hackathon](https://hackathon.jbhunt.com/home) and actually won first prize!

We also submitted this project to the 2019 [Congressional App Challenge](https://www.congressionalappchallenge.us/) in our district, and won.

Here is our [demonstration video](https://www.youtube.com/watch?v=v4vO4bch_oM&t=9s).

## Installation
Installation is pretty simple. Clone the repo, install python dependencies with pipenv

`pipenv install`

Next, run the scraper with the following sample command:

`python -m maps.cli scrape fay 30`
or
`flask scrape fay 30`

which will scrape 911 calls for the past 30 days. Read the [Scraper documentation](#scraper) for more info.

Once you've scraped the data, go ahead and start the flask server, which resides in the run.py file.

#### Configuration
The following vars need to be put in a `config.py` file inside an `instance` dir in the root of the repo dir. 

- `BING_MAPS_KEY`: An API key for the [Bing Maps Geocode Dataflow API](https://docs.microsoft.com/en-us/bingmaps/spatial-data-services/geocode-dataflow-api/). It's required for cities like Springdale which don't provide coordinates.

- `MAPS_SENTRY_DSN`: A DSN for Sentry. If provided, Sentry error reporting is setup.

An example would look like this
```python
# An API key for the Bing Maps Geocode Dataflow API.
# It's required for cities like Springdale which don't provide coordinates.
BING_MAPS_KEY = "1232134234234242fdsfsfsf

# A DSN for sentry. If provided, sentry error reporting is set up.
MAPS_SENTRY_DSN = "123123@sentry.io/32423432
```


## Website
![A view of the main map view](screenshots/main.png)

Once the server is up and running, this is what users see. We hope it's pretty clear on how to use!

## Scraper

The Scraper fetches 911 calls and inserts them into the call database. You can run the scraper like this:

`python -m maps.cli scrape fay`
or
`flask scrape fay`

The above command would scrape all data back to 24 hours ago. You can also specify how far back you want to scrape:

`python -m maps.cli scrape fay 15`
or
`flask scrape fay 15`

The above command would scrape 15 days.

### Available Commands
The following scraping commands are available for use with the cli. (All commands are prefixed with calling the cli module)

- `scrape fay [days]` : Scrape Fayetteville calls, and control how many days to scrape back with the days param (int)
- `scrape spr` : Scrape the past 24 hours of Springdale calls

# Supported Cities
- Fayetteville, Arkansas
- Springdale, Arkansas (note: doesn't support historical scraping)
