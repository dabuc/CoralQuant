# -*- coding: utf-8 -*-
"""命令工具"""
import click
from coralquant.stock_basic import get_stock_basic
from coralquant import baostck

@click.group()
def cli():
    '''命令集'''
    pass


@cli.command()
def update_stock_basic():
    """更新A股股票列表
    """
    get_stock_basic()
    click.echo("A股股票列表更新完成。")

@cli.command()
def init_d_history_k_data_plus():
    """初始化日线数据
    """
    click.confirm("正在初始化日线数据，是否继续？", abort=True)
    baostck.init_history_k_data_plus('d','tmp_history_A_stock_k_data')
    click.echo("日线数据初始化完成。")

@cli.command()
def init_w_history_k_data_plus():
    """初始化周线数据
    """
    click.confirm("正在初始化周线数据，是否继续？", abort=True)
    baostck.init_history_k_data_plus('w','tmp_w_history_A_stock_k_data')
    click.echo("周线线数据初始化完成。")

@cli.command()
def init_m_history_k_data_plus():
    """初始化月线数据
    """
    click.confirm("正在初始化月线数据，是否继续？", abort=True)
    baostck.init_history_k_data_plus('w','tmp_m_history_A_stock_k_data')
    click.echo("月线数据初始化完成。")


def main():
    cli()

if __name__ == "__main__":
    main()
