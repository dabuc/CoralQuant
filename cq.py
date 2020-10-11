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
def init_history_k_data_plus():
    """初始化日线数据
    """
    baostck.init_history_k_data_plus()
    click.echo("日线数据初始化完成。")





def main():
    cli()

if __name__ == "__main__":
    main()
