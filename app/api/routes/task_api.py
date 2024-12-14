from fastapi import APIRouter, HTTPException
from app.models.response import ResponseModel
import subprocess

router = APIRouter(
    prefix='/task',
    tags=['Task'],
    responses={404: {'description': 'Not found'}}
)

@router.post('/execute_rss')
def execute_rss():
    try:
        # Execute the RSS update script
        result = subprocess.run(['python', 'scripts/update_rss_content.py'], check=True, capture_output=True, text=True)
        
        # Return the result
        return ResponseModel(
            data={
                'status': 'success',
                'output': result.stdout
            },
            message="RSS update executed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
