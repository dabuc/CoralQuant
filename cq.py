# -*- coding: utf-8 -*-
"""命令工具"""
from datetime import datetime

import click

from coralquant import taskmanage
from coralquant.database import del_table_data
from coralquant.etl import bdl_import_Profit_Data
from coralquant.models.dim_model import DIM_Date
from coralquant.spider import (
    bs_hs300_stocks,
    bs_profit_data,
    bs_stock_basic,
    bs_stock_industry,
    bs_sz50_stocks,
    bs_zz500_stocks,
    ts_stock_basic,
)
from coralquant.stringhelper import TaskEnum


@click.group()
def cli():
    """命令集"""
    pass


@cli.command()
def update_ts_stock_basic():
    """更新ts-A股股票列表"""
    ts_stock_basic.get_stock_basic()
    click.echo("ts-A股股票列表更新完成。")


@cli.command()
def update_bs_stock_basic():
    """更新bs-A股股票列表"""
    bs_stock_basic.get_stock_basic()
    click.echo("bs-A股股票列表更新完成。")





@cli.command()
@click.option("-n", type=click.Choice(["d", "w", "m"]), prompt=True, help="d：日线数据，w：周线数据，m：月线数据")
@click.option("-bd", type=click.STRING, prompt=True, help="开始时间,1990-12-19")
@click.option("-ed", type=click.STRING, default=datetime.now().strftime("%Y-%m-%d"), help="结束时间,默认今天")
@click.option("-t", type=click.STRING, help="证券类型，其中1：股票，2：指数,3：其它")
@click.option("-s", type=click.STRING, help="上市状态，其中1：上市，0：退市")
@click.option("-m", type=click.Choice(["主板", "中小板", "创业板", "NULL", ""]), default="", help="选择市场板块")
@click.option("-d", type=click.BOOL, default=False, help="是否删除历史相同的任务，默认否")
def create_task(n, bd, ed, t, s, m, d):
    """创建任务"""
    taskEnum = TaskEnum(n)
    begin_date = datetime.strptime(bd, "%Y-%m-%d").date()
    end_date = datetime.strptime(ed, "%Y-%m-%d").date()

    if m == "":
        taskmanage.create_task(taskEnum, begin_date, end_date, type=t, status=s, isdel=d)
    else:
        taskmanage.create_task(taskEnum, begin_date, end_date, type=t, status=s, market=m, isdel=d)
    click.echo("任务创建成功")


@cli.command()
def init_dim_date():
    """
    初始化日期维度表
    """
    del_table_data(DIM_Date)
    DIM_Date.init_data()


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
def get_sz50_stocks():
    """
    获取上证50成分股
    """

    bs_sz50_stocks.get_sz50_stocks()
    click.echo("获取上证50成分股完成")


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
    # update_daily_tech()
    # update_ts_stock_basic()
    # import_dwm_data(['-f','d'])
    # init_history_k_data(['-f','d','-a','2','-m','创业板'])
    # update_history_k_data(['-f','d','-a','2','-m','创业板'])
    # create_task(['-n','d', '-bd','1990-12-19', '-t', '1', '-d','1'])


if __name__ == "__main__":
    main()
