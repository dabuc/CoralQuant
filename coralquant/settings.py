# -*- coding: utf-8 -*-
"""配置文件"""
import os, sys
from dotenv import load_dotenv
load_dotenv()
base_dir = os.path.dirname(os.path.realpath(__file__))

class BaseConfig():
    """
    基本配置类
    """
    DATABASE_URL = os.getenv("DATABASE_URL",'')
    TUSHARE_TOKEN= os.getenv("TUSHARE_TOKEN",'')


class DevelopmentConfig(BaseConfig):
    """
    开发配置类
    """
    pass

class ProductionConfig(BaseConfig):
    """
    生成环境正式配置类
    """
    pass

config={
    'development':DevelopmentConfig,
    'production':ProductionConfig
}

config_name = os.getenv("CQ_CONFIG", 'development')
CQ_Config= config[config_name]()





if __name__ == "__main__":
    pass