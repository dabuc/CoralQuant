# -*- coding: utf-8 -*-
"""命令工具"""

from datetime import datetime
import click
from coralquant.crawl.tushare import daily_basic



@click.group()
def cli():
    '''命令集'''
    pass


@cli.command()
def update_daily_basic():
    """更新每日指标
    """
    daily_basic.update_daily_basic()
    click.echo("每日指标更新完成。")






def main():
    cli()


if __name__ == "__main__":
    main()
