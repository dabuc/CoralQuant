# -*- coding: utf-8 -*-
"""命令工具"""
import click
from coralquant.stock_basic import get_stock_basic


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


def main():
    cli()

if __name__ == "__main__":
    main()
