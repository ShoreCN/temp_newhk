from datetime import datetime, UTC, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import sys
sys.path.append(".")  # 添加项目根目录到路径
from app.core.config import settings

sample_data_category = [
    {
        "name": "daily",
        "category_type": "information",
        "description": "日常生活中常用的各类产品"
    },
    {
        "name": "shopping",
        "category_type": "information",
        "description": "香港购物各类资讯"
    },
    {
        "name": "news",
        "category_type": "information",
        "description": "香港新闻资讯"
    },
    {
        "name": "bank",
        "category_type": "guide",
        "description": "香港银行相关攻略"
    },
    {
        "name": "insurance",
        "category_type": "guide",
        "description": "香港保险相关攻略"
    },
    {
        "name": "tax",
        "category_type": "guide",
        "description": "香港税务相关攻略"
    },
    {
        "name": "job",
        "category_type": "guide",
        "description": "香港求职相关攻略"
    },
    {
        "name": "life",
        "category_type": "guide",
        "description": "香港生活相关攻略"
    }
]

sample_data = [
    # 热门资讯类内容1
    {
        "content_type": "information",
        "category": "daily",
        "topic": "港区app下载榜单📱",
        "tags": ["购物", "必备", "游戏", "生活", "旅游"],
        "source_list": [
            {
                "name": "App Store",
                "link": "https://apps.apple.com",
                "logo": "https://www.apple.com/favicon.ico"
            }
        ],
        "content": [
            {
                "name": "7-Eleven HK",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "香港7-Eleven官方应用程序，提供购物、优惠券、积分等多种服务",
                "metrics": {
                    "logo": "https://apps.apple.com/favicon.ico"
                }
            },
            {
                "name": "HKTVmall",
                "link": "https://apps.apple.com/app/id4104170339",
                "remarks": "香港电视购物官方应用程序，提供购物、优惠券、积分等多种服务",
                "metrics": {
                    "logo": "https://apps.apple.com/favicon.ico"
                }
            },
            {
                "name": "HoneyNote",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "香港HoneyNote官方应用程序，提供购物、优惠券、积分等多种服务",
                "metrics": {
                    "logo": "https://apps.apple.com/favicon.ico"
                }
            },
            {
                "name": "拼多多",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "拼多多香港官方应用程序，提供购物、优惠券、积分等多种服务",
                "metrics": {
                    "logo": "https://apps.apple.com/favicon.ico"
                }
            },
            {
                "name": "大家乐",
                "link": "https://apps.apple.com/app/id1516486887",
                "remarks": "大家乐香港官方应用程序，提供餐饮、优惠券、积分等多种服务",
                "metrics": {
                    "logo": "https://apps.apple.com/favicon.ico"
                }
            }
        ],
        "is_hot": True,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "next_update_at": datetime.now(UTC) + timedelta(days=1),
    }, 

    # 热门资讯类内容2
    {
        "content_type": "information",
        "category": "shopping",
        "topic": "每周电子产品热销排行榜",
        "tags": ["电子", "购物", "手机"],
        "source_list": [
            {
                "name": "Price.com.hk",
                "link": "https://price.com.hk",
                "logo": "https://price.com.hk/favicon.ico"
            }
        ],
        "content": [
            {
                "name": "MOMAX 10000mAh 流动电源",
                "link": "https://www.taobao.com/product/10000mAh-MOMAX-Power-Bank-Black-10000mAh-MOMAX-Power-Bank-Black.html",
                "remarks": "MOMAX 10000mAh 流动电源，便携式充电宝，支持多种设备充电",
                "metrics": {
                    "price": "HKD 199",
                    "sold": 1000,
                    "rating": "95%"
                }
            },
            {
                "name": "Apple iPhone 15 Pro Max",
                "link": "https://www.taobao.com/product/Apple-iPhone-15-Pro-Max-128GB-Space-Black-Apple-iPhone-15-Pro-Max-128GB-Space-Black.html",
                "remarks": "Apple iPhone 15 Pro Max，128GB，空间黑色，支持5G",
                "metrics": {
                    "price": "HKD 11,999",
                    "sold": 800,
                    "rating": "90%"
                }
            },
            {
                "name": "Sony PlayStation 5",
                "link": "https://www.taobao.com/product/Sony-PlayStation-5.html",
                "remarks": "Sony PlayStation 5，支持4K高清游戏，支持8K蓝光播放",
                "metrics": {
                    "price": "HKD 3,999",
                    "sold": 500,
                    "rating": "85%"
                }
            },
            {
                "name": "Apple MacBook Pro",
                "link": "https://www.taobao.com/product/Apple-MacBook-Pro.html",
                "remarks": "Apple MacBook Pro，16GB内存，512GB SSD，M3芯片，支持Touch Bar",
                "metrics": {
                    "price": "HKD 19,999",
                    "sold": 300,
                    "rating": "80%"
                }
            },
            {
                "name": "Samsung Galaxy S23 Ultra",
                "link": "https://www.taobao.com/product/Samsung-Galaxy-S23-Ultra.html",
                "remarks": "Samsung Galaxy S23 Ultra，12GB内存，512GB SSD，Snapdragon 8 Gen 2，支持5G",
                "metrics": {
                    "price": "HKD 14,999",
                    "sold": 200,
                    "rating": "75%"
                }
            }
        ],
        "is_hot": True,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "next_update_at": datetime.now(UTC) + timedelta(days=1),
    },

    # 普通资讯类内容
    {
        "content_type": "information",
        "category": "news",
        "topic": "今日热门新闻📰",
        "tags": ["新闻", "资讯", "香港"],
        "source_list": [
            {
                "name": "HK01",
                "link": "https://www.hk01.com",
            }
        ],
        "content": [
            {
                "name": "桃芝风球 | 周四或周五影响香港",
                "link": "https://www.hk01.com/news/1800000000000000",
                "remarks": "桃芝风球或影响香港，周四或周五可能会有影响",
            },
            {
                "name": "屯门公路车祸 | 1死1伤",
                "link": "https://www.hk01.com/news/1800000000000000",
                "remarks": "屯门公路车祸，1死1伤",
            },
            {
                "name": "香港迪士尼乐园 | 12月1日起恢复营业",
                "link": "https://www.hk01.com/news/1800000000000000",
                "remarks": "香港迪士尼乐园12月1日起恢复营业",
            },
            {
                "name": "恒指低开92点报20334点",
                "link": "https://www.hk01.com/news/1800000000000000",
                "remarks": "恒指低开92点报20334点",
            },
            {
                "name": "警犬队75周年推微电影",
                "link": "https://www.hk01.com/news/1800000000000000",
                "remarks": "警犬队75周年推微电影",
            }
        ],
        "is_hot": False,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "next_update_at": datetime.now(UTC) + timedelta(days=1),
    },
    
    # 热门指南类内容1
    {
        "content_type": "guide",
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
        "content": {
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
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "next_update_at": datetime.now(UTC) + timedelta(days=1),
    },
    
    # 热门指南类内容2
    {
        "content_type": "guide",
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
        "content": {
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
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "next_update_at": datetime.now(UTC) + timedelta(days=1),
    },
    
    # 普通指南类内容
    {
        "content_type": "guide",
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
        "content": {
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
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "next_update_at": datetime.now(UTC) + timedelta(days=1),
    }
]

async def insert_sample_data():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    # 清空现有数据
    await db.category.delete_many({})
    await db.information.delete_many({})
    await db.guide.delete_many({})

    # 插入分类数据, 并设置created_at和updated_at
    for data in sample_data_category:
        data["created_at"] = datetime.now(UTC)
        data["updated_at"] = datetime.now(UTC)
    await db.category.insert_many(sample_data_category)
    
    # 插入示例数据
    for data in sample_data:
        content_type = data["content_type"]
        collection = db[content_type]
        await collection.insert_one(data)
        print(f"已插入 {content_type} 类型的内容: {data['topic']}")

if __name__ == "__main__":
    asyncio.run(insert_sample_data()) 