"""AutoGLM-GUI Backend API Server."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from AutoGL_GUI.phone_agent import PhoneAgent
from AutoGL_GUI.phone_agent.agent import AgentConfig
from AutoGL_GUI.phone_agent.model import ModelConfig

app = FastAPI(title="AutoGLM-GUI API", version="0.1.0")

# CORS 配置 (开发环境需要)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局单例 agent
agent: PhoneAgent | None = None


# 请求/响应模型
class InitRequest(BaseModel):
    base_url: str = "http://localhost:8080/v1"
    model_name: str = "autoglm-phone-9b"
    device_id: str | None = None
    max_steps: int = 100


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    result: str
    steps: int
    success: bool


class StatusResponse(BaseModel):
    initialized: bool
    step_count: int


# API 端点
@app.post("/api/init")
async def init_agent(request: InitRequest) -> dict:
    """初始化 PhoneAgent。"""
    global agent

    model_config = ModelConfig(
        base_url=request.base_url,
        model_name=request.model_name,
    )

    agent_config = AgentConfig(
        max_steps=request.max_steps,
        device_id=request.device_id,
        verbose=True,
    )

    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )

    return {"success": True, "message": "Agent initialized"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """发送任务给 Agent 并执行。"""
    global agent

    if agent is None:
        raise HTTPException(status_code=400, detail="Agent not initialized. Call /api/init first.")

    try:
        result = agent.run(request.message)
        steps = agent.step_count
        agent.reset()

        return ChatResponse(result=result, steps=steps, success=True)
    except Exception as e:
        return ChatResponse(result=str(e), steps=0, success=False)


@app.get("/api/status", response_model=StatusResponse)
async def get_status() -> StatusResponse:
    """获取 Agent 状态。"""
    global agent

    return StatusResponse(
        initialized=agent is not None,
        step_count=agent.step_count if agent else 0,
    )


@app.post("/api/reset")
async def reset_agent() -> dict:
    """重置 Agent 状态。"""
    global agent

    if agent is not None:
        agent.reset()

    return {"success": True, "message": "Agent reset"}


# 静态文件托管 (生产环境)
STATIC_DIR = Path(__file__).parent / "frontend" / "dist"

if STATIC_DIR.exists():
    # 托管静态资源
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    # 所有非 API 路由返回 index.html (支持前端路由)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the SPA for all non-API routes."""
        # 如果请求的是具体文件且存在，则返回该文件
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # 否则返回 index.html (支持前端路由)
        return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
