import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.content import ContentType, Content
from datetime import datetime, timedelta
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

sample_data_information = [
    # 热门资讯类内容1
    {
        "content_type": ContentType.INFORMATION,
        "category": "life",
        "topic": "港区app下载榜单📱(Mock)",
        "tags": ["购物", "必备", "游戏", "生活", "旅游"],
        "original_data_path": "http://mock/appstore",
        "source_list": [
            {
                "name": "App Store",
                "link": "https://apps.apple.com",
                "logo": "https://www.apple.com/favicon.ico",
            }
        ],
        "data": [
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
        "created_at": int(datetime.now().timestamp()),
        "updated_at": int(datetime.now().timestamp()),
        "next_update_at": int((datetime.now() + timedelta(days=1)).timestamp()),
    }, 

    # 热门资讯内容2
    {
        "content_type": ContentType.INFORMATION,
        "category": "food",
        "topic": "本周美食排行榜(Mock)",
        "title": "本周美食排行榜",
        "sub_title": "香港美食",
        "tags": ["美食", "香港", "必吃"],
        "original_data_path": "http://mock/openrice",
        "source_list": [
            {
                "name": "OpenRice",
                "link": "https://www.openrice.com",
                "logo": "https://www.openrice.com/favicon.ico",
            }
        ],
        "data": [
            {
                "name": "申子居酒屋",
                "link": "https://www.openrice.com/restaurant/hk/hongkong/shengzi-izakaya",
                "remarks": "申子居酒屋，香港知名居酒屋，提供各种日本美食",
                "metrics": {
                    "rating": "4.5",
                    "reviews": 1000
                }
            },
            {
                "name": "Harlan’s",
                "link": "https://www.openrice.com/restaurant/hk/hongkong/harlands",
                "remarks": "Harlan’s，香港知名牛排馆，提供各种牛排美食",
                "metrics": {
                    "rating": "4.2",
                    "reviews": 900
                }
            },
            {
                "name": "YAKINIKU GREAT SOHO",
                "link": "https://www.openrice.com/restaurant/hk/hongkong/yakiniku-great-soho",
                "remarks": "YAKINIKU GREAT SOHO，香港知名烤肉店，提供各种烤肉美食",
                "metrics": {
                    "rating": "4.0",
                    "reviews": 800
                }
            },
            {
                "name": "普庆餐厅",
                "link": "https://www.openrice.com/restaurant/hk/hongkong/puking-restaurant",
                "remarks": "普庆餐厅，香港知名粤菜餐厅，提供各种粤菜美食",
                "metrics": {
                    "rating": "4.1",
                    "reviews": 700
                }
            },
            {
                "name": "GARIGUETTE",
                "link": "https://www.openrice.com/restaurant/hk/hongkong/gariguette",
                "remarks": "GARIGUETTE，香港知名法式餐厅，提供各种法式美食",
                "metrics": {
                    "rating": "4.3",
                    "reviews": 600
                }
            }
        ],
        "is_hot": True,
        "created_at": int(datetime.now().timestamp()),
        "updated_at": int(datetime.now().timestamp()),
        "next_update_at": int((datetime.now() + timedelta(days=1)).timestamp()),
    },

    # 热门资讯类内容3
    {
        "content_type": ContentType.INFORMATION,
        "category": "shopping",
        "topic": "每周电子产品热销排行榜(Mock)",
        "tags": ["电子", "购物", "手机"],
        "original_data_path": "http://mock/hot_electronics",
        "source_list": [
            {
                "name": "Price.com.hk",
                "link": "https://price.com.hk",
                "logo": "https://price.com.hk/favicon.ico"
            }
        ],
        "data": [
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
        "created_at": int(datetime.now().timestamp()),
        "updated_at": int(datetime.now().timestamp()),
        "next_update_at": int((datetime.now() + timedelta(days=1)).timestamp()),
    },

    # 普通资讯类内容1
    {
        "content_type": ContentType.INFORMATION,
        "category": "food",
        "topic": "11月香港美食餐厅推介(Mock)",
        "tags": ["美食", "香港", "餐厅"],
        "original_data_path": "http://mock/timeout",
        "source_list": [
            {
                "name": "TimeOut",
                "link": "https://www.timeout.com.hk",
                "logo": "https://www.timeout.com.hk/favicon.ico",
            }
        ],
        "data": [
            {
                "name": "Tozzo：新派甜品咖啡室",
                "link": "https://www.timeout.com.hk/hongkong/restaurant/tozzo-new-school-dessert-cafe",
                "remarks": "Tozzo：新派甜品咖啡室，提供各种新派甜品和咖啡",
            },
            {
                "name": "Samsen：中环开第三间分店",
                "link": "https://www.timeout.com.hk/hongkong/restaurant/samsen-central",
                "remarks": "Samsen：中环开第三间分店，提供各种泰国美食",
            },
            {
                "name": "日月楼：怀旧京菜馆",
                "link": "https://www.timeout.com.hk/hongkong/restaurant/the-butcher-s-club",
                "remarks": "日月楼：怀旧京菜馆，提供各种怀旧京菜",
            },
            {
                "name": "Pecorino：红爆上环",
                "link": "https://www.timeout.com.hk/hongkong/restaurant/pecorino-red-hot-upper-sheungwan",
                "remarks": "Pecorino：红爆上环，提供各种意大利美食",
            },
            {
                "name": "The Butcher's Club",
                "link": "https://www.timeout.com.hk/hongkong/restaurant/the-butcher-s-club",
                "remarks": "The Butcher's Club，提供各种高品质肉类和海鲜",
            }
        ],
        "is_hot": False,
    },

    # 普通资讯类内容2
    {
        "content_type": ContentType.INFORMATION,
        "category": "news",
        "topic": "今日热门新闻📰(Mock)",
        "tags": ["新闻", "资讯", "香港"],
        "original_data_path": "http://mock/hk01/hot",
        "source_list": [
            {
                "name": "HK01",
                "link": "https://www.hk01.com",
                "logo": "https://www.hk01.com/favicon.ico"
            }
        ],
        "data": [
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
                "name": "屯门友爱村谋杀案",
                "link": "https://www.hk01.com/news/1800000000000000",
                "remarks": "屯门友爱村谋杀案，警方正在调查",
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
        "created_at": int(datetime.now().timestamp()),
        "updated_at": int(datetime.now().timestamp()),
        "next_update_at": int((datetime.now() + timedelta(days=1)).timestamp()),
    },

]

async def insert_sample_information_data(clear_mode=None):
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Clear data based on mode
    if clear_mode == 'all':
        result = await db.information.delete_many({})
        print(f"已清空所有资讯类内容数据，共删除 {result.deleted_count} 条数据")
    elif clear_mode == 'sample':
        sample_orginal_data_pathes = [item['original_data_path'] for item in sample_data_information]
        result = await db.information.delete_many({"original_data_path": {"$in": sample_orginal_data_pathes}})
        print(f"已清空示例资讯类内容数据，共删除 {result.deleted_count} 条数据")
    
    if not clear_mode:
        # Insert sample data only if no clear mode specified
        for item in sample_data_information:
            content = Content(**item)
            await db.information.insert_one(content.model_dump())
            
        print(f"已插入 {len(sample_data_information)} 条资讯类内容数据")
    
    client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Insert or clear sample information data')
    parser.add_argument('--clear', choices=['sample', 'all'], help='Clear mode: "sample" to clear only sample data, "all" to clear all data')
    args = parser.parse_args()
    
    asyncio.run(insert_sample_information_data(clear_mode=args.clear))