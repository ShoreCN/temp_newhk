import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import json
from datetime import datetime, UTC
import argparse
import sys
sys.path.append(".")  # 添加项目根目录到路径

from app.core.config import settings

class DBOperations:
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """连接数据库"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.db = self.client[settings.DATABASE_NAME]
            await self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB: {settings.DATABASE_NAME}")
        except Exception as e:
            print(f"Could not connect to MongoDB: {e}")
            raise e

    async def close(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

    async def clear_database(self, collection_name=None):
        """清空数据库或指定集合"""
        try:
            if collection_name:
                result = await self.db[collection_name].delete_many({})
                print(f"Cleared collection {collection_name}: {result.deleted_count} documents deleted")
            else:
                collections = await self.db.list_collection_names()
                for collection in collections:
                    result = await self.db[collection].delete_many({})
                    print(f"Cleared collection {collection}: {result.deleted_count} documents deleted")
        except Exception as e:
            print(f"Error clearing database: {e}")

    async def export_data(self, collection_name=None, output_file=None):
        """导出数据到JSON文件"""
        try:
            data = {}
            if collection_name:
                collections = [collection_name]
            else:
                collections = await self.db.list_collection_names()

            for coll in collections:
                cursor = self.db[coll].find({})
                documents = await cursor.to_list(length=None)
                # 转换ObjectId和datetime为字符串
                for doc in documents:
                    doc['_id'] = str(doc['_id'])
                    if 'created_at' in doc:
                        doc['created_at'] = doc['created_at'].isoformat()
                    if 'updated_at' in doc:
                        doc['updated_at'] = doc['updated_at'].isoformat()
                data[coll] = documents

            output_file = output_file or f"db_backup_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Data exported to {output_file}")
        except Exception as e:
            print(f"Error exporting data: {e}")

    async def import_data(self, input_file):
        """从JSON文件导入数据"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for collection_name, documents in data.items():
                # 转换字符串ID为ObjectId，字符串时间为datetime
                for doc in documents:
                    doc['_id'] = ObjectId(doc['_id'])
                    if 'created_at' in doc:
                        doc['created_at'] = datetime.fromisoformat(doc['created_at'])
                    if 'updated_at' in doc:
                        doc['updated_at'] = datetime.fromisoformat(doc['updated_at'])
                
                result = await self.db[collection_name].insert_many(documents)
                print(f"Imported {len(result.inserted_ids)} documents to {collection_name}")
        except Exception as e:
            print(f"Error importing data: {e}")

async def main():
    parser = argparse.ArgumentParser(description='Database Operations Tool')
    parser.add_argument('operation', choices=['clear', 'export', 'import'],
                      help='Operation to perform')
    parser.add_argument('--collection', '-c',
                      help='Specific collection to operate on')
    parser.add_argument('--file', '-f',
                      help='Input/output file for import/export')

    args = parser.parse_args()
    
    db_ops = DBOperations()
    await db_ops.connect()

    try:
        if args.operation == 'clear':
            await db_ops.clear_database(args.collection)
        elif args.operation == 'export':
            await db_ops.export_data(args.collection, args.file)
        elif args.operation == 'import':
            if not args.file:
                print("Error: Import operation requires a file path")
                return
            await db_ops.import_data(args.file)
    finally:
        await db_ops.close()

if __name__ == "__main__":
    asyncio.run(main()) 