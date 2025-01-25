import asyncio
import click
from typing import List
from app.services.task_service import TaskService
from app.models.task import ContentTask, TaskStatus
from app.core.config import settings
from app.db.mongodb import db
from datetime import datetime

"""
任务管理命令行工具

# 初始化任务数据
python scripts/tasks.py init

# 运行指定任务
python scripts/tasks.py run 任务ID

# 批量运行10个到期任务
python scripts/tasks.py run-batch --limit 10

# 设置任务为热门
python scripts/tasks.py set-hot 任务ID

# 清空所有任务数据
python scripts/tasks.py clear
"""

async def init_mongodb():
    """初始化MongoDB连接"""
    await db.connect_to_database()

async def close_mongodb():
    """关闭MongoDB连接"""
    await db.close_database_connection()

def run_async(coro):
    """运行异步函数的辅助函数"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

@click.group()
def cli():
    """任务管理命令行工具"""
    pass

@cli.command()
def init():
    """初始化任务数据"""
    async def _init():
        await init_mongodb()
        task_service = TaskService()
        await task_service.init_collection()
        await close_mongodb()
    
    click.echo("开始初始化任务数据...")
    run_async(_init())
    click.echo("任务数据初始化完成！")

@cli.command()
@click.argument('task_id')
def run(task_id):
    """执行指定的任务"""
    async def _run_task(task_id: str):
        await init_mongodb()
        task_service = TaskService()
        task = await task_service.get_task(task_id)
        if not task:
            click.echo(f"未找到ID为 {task_id} 的任务")
            return
        
        # 更新任务状态为运行中
        await task_service.update_task(task_id, {
            "status": TaskStatus.RUNNING,
            "last_run_at": int(datetime.now().timestamp())
        })
        click.echo(f"开始执行任务: {task.source_name}")
        
        # TODO: 这里需要根据实际情况调用相应的任务执行逻辑
        # 例如: await rss_service.fetch_and_process_feed(task)
        
        # 更新任务状态为活跃
        await task_service.update_task(task_id, {
            "status": TaskStatus.ACTIVE,
            "next_run_at": int(datetime.now().timestamp()) + task.update_interval
        })
        await close_mongodb()
    
    run_async(_run_task(task_id))
    click.echo("任务执行完成！")

@cli.command()
@click.option('--limit', default=10, help='要执行的任务数量')
def run_batch(limit):
    """批量执行到期的任务"""
    async def _run_batch(limit: int):
        await init_mongodb()
        task_service = TaskService()
        tasks = await task_service.get_due_tasks()
        tasks = tasks[:limit]
        
        click.echo(f"找到 {len(tasks)} 个待执行的任务")
        for task in tasks:
            click.echo(f"执行任务: {task.source_name}")
            await task_service.update_task(task.id, {
                "status": TaskStatus.RUNNING,
                "last_run_at": int(datetime.now().timestamp())
            })
            
            # TODO: 这里需要根据实际情况调用相应的任务执行逻辑
            # 例如: await rss_service.fetch_and_process_feed(task)
            
            await task_service.update_task(task.id, {
                "status": TaskStatus.ACTIVE,
                "next_run_at": int(datetime.now().timestamp()) + task.update_interval
            })
        
        await close_mongodb()
    
    run_async(_run_batch(limit))
    click.echo("批量任务执行完成！")

@cli.command()
@click.argument('task_id')
def set_hot(task_id):
    """设置任务为热门"""
    async def _set_hot(task_id: str):
        await init_mongodb()
        task_service = TaskService()
        result = await task_service.update_task(task_id, {"is_hot": True})
        if result:
            click.echo(f"已将任务 {task_id} 设置为热门")
        else:
            click.echo(f"未找到ID为 {task_id} 的任务")
        await close_mongodb()
    
    run_async(_set_hot(task_id))

@cli.command()
def clear():
    """清空所有任务数据"""
    if not click.confirm('确定要清空所有任务数据吗？'):
        return
    
    async def _clear():
        await init_mongodb()
        task_service = TaskService()
        await task_service.collection.delete_many({})
        await close_mongodb()
    
    run_async(_clear())
    click.echo("所有任务数据已清空！")

if __name__ == '__main__':
    cli()
