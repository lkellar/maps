import click

from maps import app, db


def register(cli):
    @cli.command()
    def init():
        print("Initializing database...")
        db.create_all()

    @cli.group()
    def scrape():
        pass

    @scrape.command()
    @click.argument('days', default=1)
    def fay(days):
        with app.app_context():
            from maps.scraper import scrape_fayetteville
            scrape_fayetteville(days)

    @scrape.command()
    def spr():
        with app.app_context():
            from maps.scraper import scrape_springdale
            scrape_springdale()


if __name__ == '__main__':
    @click.group()
    def main_cli():
        pass
    register(main_cli)

    main_cli()
