import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.models.content import ContentType, Content

sample_guides_data = [
    
    # 热门指南类内容1
    {
        "content_type": ContentType.GUIDES,
        "category": "bank",
        "topic": "香港银行定存利率",
        "sub_topic": "至高 *4.5%*",
        "tags": ["金额", "时间", "币种"],
        "source_list": [
            {
                "name": "HSBC",
                "link": "https://www.hsbc.com.hk",
                "logo": "https://www.hsbc.com.hk/content/dam/hsbc/hk/images/tc-hsbc-logo-2.svg"
            },
            {
                "name": "Standard Chartered",
                "link": "https://www.sc.com/hk/zh/",
                "logo": "https://av.sc.com/assets/global/images/components/header/standard-chartered-logo.svg"
            },
            {
                "name": "Bank of China",
                "link": "https://www.bochk.com",
                "logo": "https://www.bochk.com/etc/designs/bochk_web/images/logo.png"
            }
        ],
        "data": {
            "description": "香港银行定存利率对比",
            "instructions": "",
            "data_table": [
                {
                    "name": "HSBC",
                    "metrics": {
                        "deposit_rate_list": [                            
                            {"currency": "HKD", "amount": "10,000", "period": "1 month", "rate": "0.034"},
                            {"currency": "HKD", "amount": "10,000", "period": "3 months", "rate": "0.035"},
                            {"currency": "HKD", "amount": "10,000", "period": "6 months", "rate": "0.036"},
                            {"currency": "HKD", "amount": "100,000", "period": "1 month", "rate": "0.035"},
                            {"currency": "HKD", "amount": "100,000", "period": "3 months", "rate": "0.036"},
                            {"currency": "HKD", "amount": "100,000", "period": "6 months", "rate": "0.037"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "1 month", "rate": "0.036"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "3 months", "rate": "0.037"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "6 months", "rate": "0.038"},
                            {"currency": "USD", "amount": "10,000", "period": "1 month", "rate": "0.015"},
                            {"currency": "USD", "amount": "10,000", "period": "3 months", "rate": "0.016"},
                            {"currency": "USD", "amount": "10,000", "period": "6 months", "rate": "0.017"},
                            {"currency": "USD", "amount": "100,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "USD", "amount": "100,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "USD", "amount": "100,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "USD", "amount": "1,000,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "USD", "amount": "1,000,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "USD", "amount": "1,000,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "RMB", "amount": "10,000", "period": "1 month", "rate": "0.015"},
                            {"currency": "RMB", "amount": "10,000", "period": "3 months", "rate": "0.016"},
                            {"currency": "RMB", "amount": "10,000", "period": "6 months", "rate": "0.017"},
                            {"currency": "RMB", "amount": "100,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "RMB", "amount": "100,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "RMB", "amount": "100,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "1 month", "rate": "0.021"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "3 months", "rate": "0.022"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "6 months", "rate": "0.023"}
                        ],
                        "remarks": "HSBC 定存利率"
                    },
                },
                {
                    "name": "Standard Chartered",
                    "metrics": {
                        "deposit_rate_list": [                            
                            {"currency": "HKD", "amount": "10,000", "period": "1 month", "rate": "0.035"},
                            {"currency": "HKD", "amount": "10,000", "period": "3 months", "rate": "0.036"},
                            {"currency": "HKD", "amount": "10,000", "period": "6 months", "rate": "0.037"},
                            {"currency": "HKD", "amount": "100,000", "period": "1 month", "rate": "0.036"},
                            {"currency": "HKD", "amount": "100,000", "period": "3 months", "rate": "0.037"},
                            {"currency": "HKD", "amount": "100,000", "period": "6 months", "rate": "0.038"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "1 month", "rate": "0.037"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "3 months", "rate": "0.038"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "6 months", "rate": "0.039"},
                            {"currency": "USD", "amount": "10,000", "period": "1 month", "rate": "0.015"},
                            {"currency": "USD", "amount": "10,000", "period": "3 months", "rate": "0.016"},
                            {"currency": "USD", "amount": "10,000", "period": "6 months", "rate": "0.017"},
                            {"currency": "USD", "amount": "100,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "USD", "amount": "100,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "USD", "amount": "100,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "USD", "amount": "1,000,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "USD", "amount": "1,000,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "USD", "amount": "1,000,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "RMB", "amount": "10,000", "period": "1 month", "rate": "0.015"},
                            {"currency": "RMB", "amount": "10,000", "period": "3 months", "rate": "0.016"},
                            {"currency": "RMB", "amount": "10,000", "period": "6 months", "rate": "0.017"},
                            {"currency": "RMB", "amount": "100,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "RMB", "amount": "100,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "RMB", "amount": "100,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "1 month", "rate": "0.021"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "3 months", "rate": "0.022"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "6 months", "rate": "0.023"}
                        ]
                    },
                    "remarks": "Standard Chartered 定存利率"
                },
                {
                    "name": "Bank of China",
                    "metrics": {
                        "deposit_rate_list": [                            
                            {"currency": "HKD", "amount": "10,000", "period": "1 month", "rate": "0.035"},
                            {"currency": "HKD", "amount": "10,000", "period": "3 months", "rate": "0.036"},
                            {"currency": "HKD", "amount": "10,000", "period": "6 months", "rate": "0.037"},
                            {"currency": "HKD", "amount": "100,000", "period": "1 month", "rate": "0.036"},
                            {"currency": "HKD", "amount": "100,000", "period": "3 months", "rate": "0.037"},
                            {"currency": "HKD", "amount": "100,000", "period": "6 months", "rate": "0.038"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "1 month", "rate": "0.037"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "3 months", "rate": "0.038"},
                            {"currency": "HKD", "amount": "1,000,000", "period": "6 months", "rate": "0.039"},
                            {"currency": "USD", "amount": "10,000", "period": "1 month", "rate": "0.015"},
                            {"currency": "USD", "amount": "10,000", "period": "3 months", "rate": "0.016"},
                            {"currency": "USD", "amount": "10,000", "period": "6 months", "rate": "0.017"},
                            {"currency": "USD", "amount": "100,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "USD", "amount": "100,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "USD", "amount": "100,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "USD", "amount": "1,000,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "USD", "amount": "1,000,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "USD", "amount": "1,000,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "RMB", "amount": "10,000", "period": "1 month", "rate": "0.015"},
                            {"currency": "RMB", "amount": "10,000", "period": "3 months", "rate": "0.016"},
                            {"currency": "RMB", "amount": "10,000", "period": "6 months", "rate": "0.017"},
                            {"currency": "RMB", "amount": "100,000", "period": "1 month", "rate": "0.018"},
                            {"currency": "RMB", "amount": "100,000", "period": "3 months", "rate": "0.019"},
                            {"currency": "RMB", "amount": "100,000", "period": "6 months", "rate": "0.020"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "1 month", "rate": "0.021"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "3 months", "rate": "0.022"},
                            {"currency": "RMB", "amount": "1,000,000", "period": "6 months", "rate": "0.023"}
                        ],
                    },
                    "remarks": "Bank of China 定存利率"
                }
            ]
            
        },
        "is_hot": True,
    },
    
    # 热门指南类内容2
    {
        "content_type": ContentType.GUIDES,
        "category": "job",
        "topic": "香港IT行业薪资报告",
        "sub_topic": "最高 *HKD 100,000*",
        "tags": ["薪资", "行业", "IT"],
        "source_list": [
            {
                "name": "LinkedIn",
                "link": "https://www.linkedin.com"
            }
        ],
        "data": {
            "description": "香港IT行业薪资报告",
            "instructions": "",
            "data_table": [
                {
                    "name": "初级开发工程师",
                    "metrics": {"salary_range": "HKD 15,000-25,000"}
                },
                {
                    "name": "高级开发工程师",
                    "metrics": {"salary_range": "HKD 35,000-60,000"}
                },
                {
                    "name": "架构师",
                    "metrics": {"salary_range": "HKD 60,000-100,000"}
                },
                {
                    "name": "项目经理",
                    "metrics": {"salary_range": "HKD 50,000-80,000"}
                }
            ]
        },
        "is_hot": True,
    },
    
    # 普通指南类内容
    {
        "content_type": ContentType.GUIDES,
        "category": "life",
        "topic": "香港租房攻略",
        "sub_topic": "最低 *$5,000*",
        "tags": ["租房", "生活", "香港"],
        "source_list": [
            {
                "name": "香港租房网",
                "link": "https://www.hkrent.com",
                "logo": "https://www.hkrent.com/favicon.ico"
            }
        ],
        "data": {
            "description": "在香港租房的完整指南",
            "instructions": "1. 选择区域\n2. 预算规划\n3. 中介联系\n4. 看房注意事项",
            "data_table": [
                {
                    "name": "港岛区均价",
                    "metrics": {"price": "HKD 20,000起"}
                },
                {
                    "name": "九龙区均价",
                    "metrics": {"price": "HKD 15,000起"}
                },
                {
                    "name": "新界区均价",
                    "metrics": {"price": "HKD 12,000起"}
                }
            ]
        },
        "is_hot": False,
    }
]

async def insert_sample_guides_data():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    # 清空现有数据
    r = await db.guides.delete_many({})
    print(f"已清空现有指南类内容数据，共删除 {r.deleted_count} 条数据")

    # 将sample_guides_data转换为Content对象
    content_list = []
    for data in sample_guides_data:
        content = Content(**data)
        content_list.append(content.model_dump())

    # 插入示例数据
    await db.guides.insert_many(content_list)
    print(f"已插入 {len(content_list)} 条指南类内容数据")

if __name__ == "__main__":
    asyncio.run(insert_sample_guides_data()) 