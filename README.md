# Crime Map
An easy way to see recent 911 calls made in Fayetteville, Arkansas

## History
We made this project for the [2019 JB Hunt Hackathon](https://hackathon.jbhunt.com/home) and actually won first prize!

## Installation
Installation is pretty simple. Clone the repo, install python dependencies with pipenv

`pipenv install`

Next, initialize the db with the cli, with the following command

`python -m maps.cli refresh`

Then, run the scraper via the cli, with the following sample command

`python -m maps.cli scrape 30`

which will scrape 911 calls for the past 30 days. I highly recommend reading the [CLI documentation](#cli) for more info.

Once you've scraped the data, go ahead and start the flask server!, which resides in the maps.app file.

## Website
![A view of the main map view](screenshots/main.png)

Once the server is up and running, this is what users see. We hope it's pretty clear on how to use!

## CLI

The CLI has two different commands, `scrape` and `refresh`.

It can be run by just running the `maps/cli.py` file, with one of the commands as a parameter.

#### `scrape`

Scrape is the command to scrape the 911 call database. After the `scrape` command, put the number of days you want to scrape.

`python -m maps.cli scrape 15`

The above command would scrape 15 days. 

#### `refresh`

Refresh wipes the database, and initializes it again. This command can also be used to initialize the database for the first time (which must be done in order to start scraping data).

`python -m maps.cli refresh`
