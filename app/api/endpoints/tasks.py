from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.database.models import TaskLog
from app.services.collectors.base_collector import BaseCollector
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["tasks"])

# Pydantic模型
class TaskRequest(BaseModel):
    task_name: str
    task_type: str  # collect, analyze, process
    parameters: Optional[dict] = None

class TaskResponse(BaseModel):
    id: int
    task_name: str
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_items: Optional[int] = None
    success_items: Optional[int] = None
    error_items: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class TaskStatusResponse(BaseModel):
    task_id: int
    status: str
    progress: float = 0.0
    message: str = ""


@router.post("/start", response_model=TaskResponse)
async def start_task(
    request: TaskRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """启动任务"""
    # 创建任务日志
    task_log = TaskLog(
        task_name=request.task_name,
        status="running",
        start_time=datetime.now(),
        total_items=0,
        success_items=0,
        error_items=0
    )
    
    db.add(task_log)
    db.commit()
    db.refresh(task_log)
    
    # 根据任务类型启动不同的后台任务
    if request.task_type == "collect":
        background_tasks.add_task(run_data_collection, task_log.id, request.parameters, db)
    elif request.task_type == "analyze":
        background_tasks.add_task(run_analysis_task, task_log.id, request.parameters, db)
    elif request.task_type == "process":
        background_tasks.add_task(run_data_processing, task_log.id, request.parameters, db)
    else:
        # 更新任务状态为失败
        task_log.status = "failed"
        task_log.error_message = f"未知的任务类型: {request.task_type}"
        task_log.end_time = datetime.now()
        db.commit()
        raise HTTPException(status_code=400, detail=f"未知的任务类型: {request.task_type}")
    
    return task_log


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    query = db.query(TaskLog)
    
    if status:
        query = query.filter(TaskLog.status == status)
    
    tasks = query.order_by(TaskLog.created_at.desc()).offset(skip).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """获取任务详情"""
    task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.get("/{task_id}/status", response_model=TaskStatusResponse)
def get_task_status(task_id: int, db: Session = Depends(get_db)):
    """获取任务状态"""
    task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 计算进度
    progress = 0.0
    if task.total_items and task.total_items > 0:
        progress = (task.success_items + task.error_items) / task.total_items * 100
    
    return TaskStatusResponse(
        task_id=task.id,
        status=task.status,
        progress=progress,
        message=f"成功: {task.success_items}, 失败: {task.error_items}, 总计: {task.total_items}"
    )


async def run_data_collection(task_id: int, parameters: Optional[dict], db: Session):
    """运行数据采集任务"""
    try:
        # 这里应该根据参数调用具体的采集器
        logger.info(f"开始数据采集任务 {task_id}")
        
        # 模拟数据采集过程
        import time
        time.sleep(2)  # 模拟处理时间
        
        # 更新任务状态
        task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
        if task:
            task.status = "completed"
            task.end_time = datetime.now()
            task.total_items = 100
            task.success_items = 95
            task.error_items = 5
            db.commit()
            
        logger.info(f"数据采集任务 {task_id} 完成")
        
    except Exception as e:
        logger.error(f"数据采集任务 {task_id} 失败: {e}")
        task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
        if task:
            task.status = "failed"
            task.end_time = datetime.now()
            task.error_message = str(e)
            db.commit()


async def run_analysis_task(task_id: int, parameters: Optional[dict], db: Session):
    """运行分析任务"""
    try:
        logger.info(f"开始分析任务 {task_id}")
        
        # 模拟分析过程
        import time
        time.sleep(3)  # 模拟处理时间
        
        # 更新任务状态
        task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
        if task:
            task.status = "completed"
            task.end_time = datetime.now()
            task.total_items = 50
            task.success_items = 48
            task.error_items = 2
            db.commit()
            
        logger.info(f"分析任务 {task_id} 完成")
        
    except Exception as e:
        logger.error(f"分析任务 {task_id} 失败: {e}")
        task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
        if task:
            task.status = "failed"
            task.end_time = datetime.now()
            task.error_message = str(e)
            db.commit()


async def run_data_processing(task_id: int, parameters: Optional[dict], db: Session):
    """运行数据处理任务"""
    try:
        logger.info(f"开始数据处理任务 {task_id}")
        
        # 模拟数据处理过程
        import time
        time.sleep(1)  # 模拟处理时间
        
        # 更新任务状态
        task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
        if task:
            task.status = "completed"
            task.end_time = datetime.now()
            task.total_items = 200
            task.success_items = 195
            task.error_items = 5
            db.commit()
            
        logger.info(f"数据处理任务 {task_id} 完成")
        
    except Exception as e:
        logger.error(f"数据处理任务 {task_id} 失败: {e}")
        task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
        if task:
            task.status = "failed"
            task.end_time = datetime.now()
            task.error_message = str(e)
            db.commit() 