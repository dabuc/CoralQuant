# -*- coding: utf-8 -*-
"""命令工具"""
from coralquant.etl import bdl_import_k_data
import click
from coralquant.spider import ts_stock_basic
from coralquant.spider import bs_stock_basic
from coralquant import baostck


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
def init_d_history_k_data_plus():
    """初始化日线数据
    """
    click.confirm("正在初始化日线数据，是否继续？", abort=True)
    baostck.init_history_k_data_plus('d', 'odl_history_A_stock_k_data')
    click.echo("日线数据初始化完成。")


@cli.command()
def init_w_history_k_data_plus():
    """初始化周线数据
    """
    click.confirm("正在初始化周线数据，是否继续？", abort=True)
    baostck.init_history_k_data_plus('w', 'odl_w_history_A_stock_k_data')
    click.echo("周线线数据初始化完成。")


@cli.command()
def init_m_history_k_data_plus():
    """初始化月线数据
    """
    click.confirm("正在初始化月线数据，是否继续？", abort=True)
    baostck.init_history_k_data_plus('w', 'odl_m_history_A_stock_k_data')
    click.echo("月线数据初始化完成。")


@cli.command()
@click.option('-f', type=click.Choice(['d','w', 'm']), prompt=True, help='d：日线数据，w：导入周线数据，m：导入月线数据')
def import_dwm_data(f):
    """导入K线数据
    """
    click.confirm("正在导入导入ODL-k线数据，是否继续？", abort=True)
    bdl_import_k_data.import_data(f)
    click.echo("ODL周月线数据导入完成。")


def main():
    cli()


if __name__ == "__main__":
    main()
