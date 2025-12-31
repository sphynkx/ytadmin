import asyncio
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

async def exec_grpcurl(
    host: str,
    port: int,
    method: str,
    data: Optional[Dict] = None,
    plaintext: bool = True,
    headers: Optional[List[str]] = None,
    timeout_sec: int = 3,
) -> Dict:
    """
    Universal grpcurl call via Server Reflection, WITHOUT local .proto.
    Returns parsed JSON or dict with "error".
    """
    target = f"{host}:{port}"
    cmd = ["grpcurl"]
    if plaintext:
        cmd.append("-plaintext")
    if headers:
        for h in headers:
            cmd.extend(["-H", h])
    if data is not None:
        cmd.extend(["-d", json.dumps(data)])
    cmd.append(target)
    cmd.append(method)

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)
        except asyncio.TimeoutError:
            proc.kill()
            return {"error": "timeout", "cmd": " ".join(cmd)}

        if proc.returncode != 0:
            err_text = stderr.decode("utf-8", errors="ignore").strip()
            logger.warning(f"grpcurl error [{proc.returncode}]: {err_text}")
            return {"error": err_text, "cmd": " ".join(cmd)}

        out_text = stdout.decode("utf-8", errors="ignore").strip()
        if not out_text:
            return {}
        try:
            return json.loads(out_text)
        except json.JSONDecodeError:
            return {"raw": out_text}
    except FileNotFoundError:
        return {"error": "grpcurl not found in PATH"}
    except Exception as e:
        logger.exception("grpcurl exec failed")
        return {"error": str(e)}