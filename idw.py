# -*- coding: utf-8 -*-
"""数据仓库管理工具"""
import click
from coralquant.database import engine
from coralquant.models import bdl_model, odl_model,orm_model
from coralquant.settings import CQ_Config


@click.group()
def odl():
    '''操作数据层'''
    pass


@click.group()
def bdl():
    '''基础数据层'''
    pass


@click.group()
def idl():
    '''接口数据层'''
    pass


@click.group()
def dim():
    '''DIM 字典层'''
    pass


@odl.command()
def create_dw():
    """创建数据仓库
    """
    click.confirm("正在创建操作数据层数据表，是否继续？", abort=True)

    odl_model.Base.metadata.create_all(engine)
    bdl_model.Base.metadata.create_all(engine)
    orm_model.Base.metadata.create_all(engine)


    click.echo("数据层数据表创建完成")


def main():
    odl()


if __name__ == "__main__":
    main()