# -*- coding: utf-8 -*-
"""命令工具"""
from datetime import datetime

import click

from coralquant import taskmanage
from coralquant.database import del_table_data
from coralquant.etl import bdl_import_k_data, bdl_import_Profit_Data
from coralquant.models.dim_model import DIM_Date
from coralquant.spider import (bs_hs300_stocks, bs_profit_data, bs_stock_basic, bs_stock_industry, bs_zz500_stocks,
                               ts_stock_basic, ts_trade_cal)
from coralquant.spider.bs_history_k_data import init_history_k_data_plus
from coralquant.stringhelper import TaskEnum
from coralquant.taskmanage import update_task_table


@click.group()
def cli():
    '''命令集'''
    pass


@cli.command()
def update_ts_stock_basic():
    """更新ts-A股股票列表
    """
    ts_stock_basic.get_stock_basic()
    click.echo("ts-A股股票列表更新完成。")


@cli.command()
def update_bs_stock_basic():
    """更新bs-A股股票列表
    """
    bs_stock_basic.get_stock_basic()
    click.echo("bs-A股股票列表更新完成。")


@cli.command()
@click.option('-f', type=click.Choice(['d', 'w', 'm', '5']), prompt=True, help='d：日线数据，w：周线数据，m：月线数据')
@click.option('-a', type=click.Choice(['1', '2', '3']), default='3', help='1：后复权；2：前复权; 3：不复权；默认不复权')
@click.pass_context
def init_history_k_data(ctx, f, a):
    """创建新的任务列表，初始化历史k线数据
    """
    click.confirm("正在初始化 {}-{} 历史k线数据，是否继续？".format(f,a), abort=True)
    #创建任务
    if f=='d':
        taskvalue = TaskEnum.日线历史A股K线数据.value
    elif f=='w':
        taskvalue = TaskEnum.周线历史A股K线数据.value
    elif f=='m':
        taskvalue = TaskEnum.月线历史A股K线数据.value
    else:
        taskvalue = TaskEnum.T5分钟线历史A股K线数据.value

    ctx.invoke(create_task, n=taskvalue, bd='1990-12-19', t=1, d=1)
    ctx.invoke(create_task, n=taskvalue, bd='1990-12-19', t=2, d=0)
    init_history_k_data_plus(f,a)
    click.echo("{}-{} 线数据初始化完成。".format(f,a))


@cli.command()
@click.option('-f', type=click.Choice(['d', 'w', 'm', '5']), prompt=True, help='d：日线数据，w：周线数据，m：月线数据')
def update_history_k_data(f):
    """创建新的任务列表，更新历史k线数据
    """
    taskEnum = TaskEnum(f)
    click.confirm("准备更新-{}，是否继续？".format(taskEnum.name), abort=True)
    #更新任务
    update_task_table(taskEnum)
    init_history_k_data_plus(f)
    click.echo("{}-线数据更新完成。".format(taskEnum.name))


@cli.command()
@click.option('-f', type=click.Choice(['d', 'w', 'm']), prompt=True, help='d：日线数据，w：导入周线数据，m：导入月线数据')
def import_dwm_data(f):
    """导入K线数据
    """
    click.confirm("正在导入导入ODL-k线数据，是否继续？", abort=True)
    bdl_import_k_data.import_data(f)
    click.echo("ODL周月线数据导入完成。")


@cli.command()
@click.option('-n', type=click.Choice(['d', 'w', 'm']), prompt=True, help='d：日线数据，w：周线数据，m：月线数据')
@click.option('-bd', type=click.STRING, prompt=True, help='开始时间,1990-12-19')
@click.option('-ed', type=click.STRING, default=datetime.now().strftime("%Y-%m-%d"), help='结束时间,默认今天')
@click.option('-t', type=click.STRING, help='证券类型，其中1：股票，2：指数,3：其它')
@click.option('-s', type=click.STRING, help='上市状态，其中1：上市，0：退市')
@click.option('-d', type=click.BOOL, default=False, help='是否删除历史相同的任务，默认否')
def create_task(n, bd, ed, t, s, d):
    """创建任务
    """
    taskEnum = TaskEnum(n)
    begin_date = datetime.strptime(bd, "%Y-%m-%d").date()
    end_date = datetime.strptime(ed, "%Y-%m-%d").date()

    taskmanage.create_task(taskEnum, begin_date, end_date, type=t, status=s, isdel=d)
    click.echo("任务创建成功")


@cli.command()
def init_dim_date():
    """
    初始化日期维度表
    """
    del_table_data(DIM_Date)
    DIM_Date.init_data()


@cli.command()
def create_cal_date():
    """
    创建交易日历
    """
    ts_trade_cal.create_cal_date()
    click.echo("创建交易日历完成")


@cli.command()
def create_stock_industry():
    """
    创建行业分类
    """
    bs_stock_industry.create_stock_industry()
    click.echo("创建行业分类完成")


@cli.command()
def get_hs300_stocks():
    """
    获取沪深300成分股
    """

    bs_hs300_stocks.get_hs300_stocks()
    click.echo("获取沪深300成分股完成")


@cli.command()
def get_zz500_stocks():
    """
    获取中证500成分股
    """

    bs_zz500_stocks.get_zz500_stocks()
    click.echo("获取中证500成分股完成")


@cli.command()
def get_profit_data():
    """
    获取季频盈利能力数据
    """

    bs_profit_data.create_profit_data_task()
    bs_profit_data.get_profit_data()
    click.echo("获取季频盈利能力数据完成")


@cli.command()
def ETL_Profit_Data():
    """
    到入季频盈利能力数据到基础数据层
    """
    click.confirm("正在导入季频盈利能力数据，是否继续？", abort=True)
    bdl_import_Profit_Data.import_data()

    click.echo("到入季频盈利能力数据完成")


def main():
    cli()
    #import_dwm_data(['-f','d'])
    #init_history_k_data(['-f','d'])
    #update_history_k_data(['-f','d'])
    #create_task(['-n','d', '-bd','1990-12-19', '-t', '1', '-d','1'])


if __name__ == "__main__":
    main()
