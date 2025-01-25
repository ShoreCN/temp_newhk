from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.task import ContentTask, TaskStatus, TaskProcessStatus
from app.models.response import ResponseModel
from app.services.task_service import TaskService
from scripts.update_rss_content import update_rss_content
import subprocess
from datetime import datetime

router = APIRouter(
    prefix='/task',
    tags=['Task'],
    responses={404: {'description': 'Not found'}}
)

@router.post('/tasks', response_model=ResponseModel)
async def create_task(task: ContentTask):
    task_service = TaskService()
    created_task = await task_service.create_task(task)
    return ResponseModel(
        data=created_task.model_dump(),
        message="Task created successfully"
    )

@router.get('/tasks/{task_id}', response_model=ResponseModel)
async def get_task(task_id: str):
    task_service = TaskService()
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return ResponseModel(
        data=task.model_dump(),
        message="Task retrieved successfully"
    )

@router.get('/tasks', response_model=ResponseModel)
async def list_tasks(skip: int = 0, limit: int = 10):
    task_service = TaskService()
    tasks = await task_service.list_tasks(skip, limit)
    return ResponseModel(
        data=[task.model_dump() for task in tasks],
        message="Tasks retrieved successfully"
    )

@router.put('/tasks/{task_id}', response_model=ResponseModel)
async def update_task(task_id: str, task_update: dict):
    task_service = TaskService()
    updated_task = await task_service.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return ResponseModel(
        data=updated_task.model_dump(),
        message="Task updated successfully"
    )

@router.delete('/tasks/{task_id}', response_model=ResponseModel)
async def delete_task(task_id: str):
    task_service = TaskService()
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return ResponseModel(
        data={"task_id": task_id},
        message="Task deleted successfully"
    )

@router.post('/execute_rss')
async def execute_rss():
    try:
        # Execute the RSS update script
        result = subprocess.run(['python', 'scripts/update_rss_content.py'], check=True, capture_output=True, text=True)
        
        return ResponseModel(
            data={
                'status': 'success',
                'output': result.stdout
            },
            message="RSS update executed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/execute_task/{task_id}')
async def execute_task(task_id: str):
    task_service = TaskService()
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        # Update task status to running
        await task_service.update_task(task_id, {"process_status": TaskProcessStatus.RUNNING})
        
        # Execute different types of tasks
        if task.task_type == "rss":
            # result = subprocess.run(['python', 'scripts/update_rss_content.py'], check=True, capture_output=True, text=True)
            # 通过update_rss_content.py 更新rss内容
            await update_rss_content(task.source_url)
        # Add other task type handlers here
        
        # Update task execution time and status
        current_time = int(datetime.now().timestamp())
        await task_service.update_task(task_id, {
            "process_status": TaskProcessStatus.SUCCESS,
            "last_run_at": current_time,
            "next_run_at": current_time + task.update_interval
        })
        
        return ResponseModel(
            data={
                'status': 'success',
                'task_id': task_id
            },
            message="Task executed successfully"
        )
    except Exception as e:
        # Update task status to failed
        await task_service.update_task(task_id, {"process_status": TaskProcessStatus.FAILED})
        raise HTTPException(status_code=500, detail=str(e))
