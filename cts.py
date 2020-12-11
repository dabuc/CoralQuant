# -*- coding: utf-8 -*-
"""命令工具"""

from coralquant.stringhelper import TaskEnum
from datetime import datetime
import click
from coralquant.crawl.tushare import daily_basic
from coralquant.crawl.tushare import daily
from coralquant import taskmanage



@click.group()
def cli():
    '''命令集'''
    pass


@cli.command()
@click.option('--reset', type=click.BOOL, default=False, help='是否重置任务列表，默认否')
def update_daily_basic(reset):
    """更新每日指标
    """

    if reset:
        taskmanage.create_ts_cal_task(TaskEnum.TS更新每日指标)

    daily_basic.update_daily_basic()
    click.echo("每日指标更新完成。")

@cli.command()
@click.option('--reset', type=click.BOOL, default=False, help='是否重置任务列表，默认否')
def update_daily(reset):
    """更新日线行情
    """

    if reset:
        daily.update_task()

    daily.get_daily()
    click.echo("日线行情更新完成。")




def main():
    cli()


if __name__ == "__main__":
    main()
