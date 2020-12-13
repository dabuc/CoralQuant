import click
from coralquant import taskmanage
from coralquant.stringhelper import TaskEnum
from coralquant.odl.baostock import daily_hfq as bs_daily_hfq

@click.group()
def cli():
    '''命令集'''
    pass

@cli.command()
@click.option('--reset', type=click.BOOL, default=False, help='是否重置任务列表，默认否')
def update_daily_hfq(reset):
    """更新每日指标
    """
    click.confirm("正在更新BS日线后复权行情数据，是否继续？", abort=True)


    bs_daily_hfq.update_task(reset)

    bs_daily_hfq.get_daily_hfq()

    click.echo("BS日线后复权行情数据更新完成。")



def main():
    cli()


if __name__ == "__main__":
    main()