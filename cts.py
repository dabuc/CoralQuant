# -*- coding: utf-8 -*-
"""命令工具"""

from coralquant.stringhelper import TaskEnum
from datetime import datetime
import click
from coralquant.odl.tushare import adj_factor, daily_basic, daily
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
    click.confirm("正在更新每日指标，是否继续？", abort=True)

    if reset:
        taskmanage.create_ts_cal_task(TaskEnum.TS更新每日指标)

    daily_basic.update_daily_basic()
    click.echo("每日指标更新完成。")


@cli.command()
@click.option('--reset', type=click.BOOL, default=False, help='是否重置任务列表，默认否')
def update_daily(reset):
    """更新日线行情
    """
    click.confirm("正在更新日线行情，是否继续？", abort=True)

    if reset:
        daily.update_task()

    daily.get_daily()
    click.echo("日线行情更新完成。")


@cli.command()
@click.option('--reset', type=click.BOOL, default=False, help='是否重置任务列表，默认否')
def update_adj_factor(reset):
    """更新复权因子
    """
    click.confirm("正在更新复权因子，是否继续？", abort=True)

    if reset:
        adj_factor.update_task()

    adj_factor.get_adj_factor()
    click.echo("复权因子更新完成。")


def main():
    cli()


if __name__ == "__main__":
    main()
