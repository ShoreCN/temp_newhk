from datetime import datetime, UTC
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import sys
sys.path.append(".")  # 添加项目根目录到路径
from app.core.config import settings

sample_data = [
    # 热门信息类内容
    {
        "content_type": "information",
        "domain": {
            "name": "日常",
            "description": "日常生活中常用的各类产品"
        },
        "topic": "港区app下载榜单📱",
        "content": [
            {
                "name": "7-Eleven HK",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "香港7-Eleven官方应用程序，提供购物、优惠券、积分等多种服务"
            },
            {
                "name": "HKTVmall",
                "link": "https://apps.apple.com/app/id4104170339",
                "remarks": "香港电视购物官方应用程序，提供购物、优惠券、积分等多种服务"
            },
            {
                "name": "HoneyNote",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "香港HoneyNote官方应用程序，提供购物、优惠券、积分等多种服务"
            },
            {
                "name": "拼多多",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "拼多多香港官方应用程序，提供购物、优惠券、积分等多种服务"
            },
            {
                "name": "大家乐",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "大家乐香港官方应用程序，提供餐饮、优惠券、积分等多种服务"
            }
        ],
        "is_hot": True,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    },
    
    # 热门指南类内容
    {
        "content_type": "guide",
        "domain": {
            "name": "教育",
            "description": "香港教育相关指南"
        },
        "topic": "香港国际学校申请指南",
        "content": {
            "description": "详细的国际学校申请流程",
            "instructions": "1. 准备材料\n2. 提交申请\n3. 面试准备",
            "data_table": {
                "申请时间": "每年9-11月",
                "所需文件": ["成绩单", "推荐信", "护照复印件"]
            }
        },
        "is_hot": True,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    },
    
    # 普通信息类内容
    {
        "content_type": "information",
        "domain": {
            "name": "就业",
            "description": "香港就业市场信息"
        },
        "topic": "香港IT行业薪资报告",
        "content": [
            {
                "name": "初级开发工程师",
                "metrics": {"薪资范围": "HKD 15,000-25,000"}
            },
            {
                "name": "高级开发工程师",
                "metrics": {"薪资范围": "HKD 35,000-60,000"}
            },
            {
                "name": "架构师",
                "metrics": {"薪资范围": "HKD 60,000-100,000"}
            },
            {
                "name": "项目经理",
                "metrics": {"薪资范围": "HKD 50,000-80,000"}
            }
        ],
        "is_hot": False,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    },
    
    # 普通指南类内容
    {
        "content_type": "guide",
        "domain": {
            "name": "生活",
            "description": "香港生活指南"
        },
        "topic": "香港租房攻略",
        "content": {
            "description": "在香港租房的完整指南",
            "instructions": "1. 选择区域\n2. 预算规划\n3. 中介联系\n4. 看房注意事项",
            "data_table": {
                "港岛区均价": "HKD 20,000起",
                "九龙区均价": "HKD 15,000起",
                "新界区均价": "HKD 12,000起"
            }
        },
        "is_hot": False,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }
]

async def insert_sample_data():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    # 清空现有数据
    await db.information.delete_many({})
    await db.guide.delete_many({})
    
    # 插入示例数据
    for data in sample_data:
        content_type = data["content_type"]
        collection = db[content_type]
        await collection.insert_one(data)
        print(f"已插入 {content_type} 类型的内容: {data['topic']}")

if __name__ == "__main__":
    asyncio.run(insert_sample_data()) 