from datetime import datetime, UTC, timedelta

import argparse
import asyncio
import sys
sys.path.append(".")  # 添加项目根目录到路径
from app.core.config import settings
from scripts.sample_category_data import insert_sample_category_data
from scripts.sample_guides_data import insert_sample_guides_data
from scripts.sample_information_data import insert_sample_information_data

parser = argparse.ArgumentParser(description="处理示例数据")
# 指定要处理的示例数据类型, 默认处理所有类型, 可以不指定
parser.add_argument("--type", type=str, help="指定要处理的示例数据类型", choices=["category", "guides", "information", "all"], default="all")
parser.add_argument("--insert", action="store_true", help="插入示例数据")
parser.add_argument("--delete", action="store_true", help="删除示例数据")
args = parser.parse_args()

async def insert_sample_data():
    await insert_sample_category_data()
    await insert_sample_guides_data()
    await insert_sample_information_data()


if __name__ == "__main__":
    # 根据用户输入的命令行参数，删除或者插入相应的示例数据
    if args.type == "category":
        asyncio.run(insert_sample_category_data()) 
    elif args.type == "guides":
        asyncio.run(insert_sample_guides_data()) 
    elif args.type == "information":
        asyncio.run(insert_sample_information_data()) 
    elif args.type == "all":
        asyncio.run(insert_sample_data()) 
    else:
        print("无效的示例数据类型")
        parser.print_help()
