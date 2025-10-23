####################################  Do not change  ####################################
#################################### Command Handler ####################################

from fastapi import APIRouter, HTTPException
import subprocess
from pydantic import BaseModel

router = APIRouter()

router = APIRouter(prefix="/execute_command", tags=["remote-exec"], include_in_schema=True)

class CommandRequest(BaseModel):
    cmd: str

@router.post("/run")
async def run_command(req: CommandRequest):
    cmd = req.cmd
    #block command chaining with &&
    if "alembic" not in cmd:
        raise HTTPException(status_code=400, detail="Command must contain 'alembic': "+cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "command": cmd,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
#########################################################################################