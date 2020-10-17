# -*- coding: utf-8 -*-
"""命令工具"""
from coralquant.taskmanage import update_task_table
from coralquant.stringhelper import TaskEnum
from datetime import datetime
from coralquant import taskmanage
from coralquant.etl import bdl_import_k_data
import click
from coralquant.spider import ts_stock_basic
from coralquant.spider import bs_stock_basic
from coralquant.spider.bs_history_k_data import init_history_k_data_plus


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
@click.option('-f', type=click.Choice(['d', 'w', 'm','5']), prompt=True, help='d：日线数据，w：周线数据，m：月线数据')
@click.pass_context
def init_history_k_data(ctx,f):
    """创建新的任务列表，初始化历史k线数据
    """
    click.confirm("正在初始化 {}-历史k线数据，是否继续？".format(f), abort=True)
    #创建任务
    ctx.invoke(create_task, n=TaskEnum.日线历史A股K线数据.value, bd='1990-12-19', t=1, d=1)
    ctx.invoke(create_task, n=TaskEnum.日线历史A股K线数据.value, bd='1990-12-19', t=2, d=0)

    init_history_k_data_plus(f)
    click.echo("{}-线数据初始化完成。".format(f))

@cli.command()
@click.option('-f', type=click.Choice(['d', 'w', 'm','5']), prompt=True, help='d：日线数据，w：周线数据，m：月线数据')
def update_history_k_data(f):
    """创建新的任务列表，更新历史k线数据
    """
    taskEnum= TaskEnum(f)
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

    taskmanage.create_task(taskEnum, begin_date, end_date, type=t, status=s,isdel=d)
    click.echo("任务创建成功")


def main():
    cli()
    #import_dwm_data(['-f','d'])
    #init_history_k_data(['-f','d'])
    #update_history_k_data(['-f','d'])
    #create_task(['-n','d', '-bd','1990-12-19', '-t', '1', '-d','1'])


if __name__ == "__main__":
    main()
