"""FastAPI application exposing the BlackRoad agent API.

This is the unified API surface for the BlackRoad OS agent system.
It provides endpoints for:
- Health checks and telemetry
- Device flashing and management
- Model inference (local LLMs)
- Transcription services
- Job execution
- Settings management
"""
from __future__ import annotations

import asyncio
import contextlib
import json
import os
import pathlib
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import (
    Body,
    Depends,
    FastAPI,
    File,
    Header,
    HTTPException,
    Request,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.websockets import WebSocketState

# Import agent modules with fallback for missing dependencies
try:
    from agent import discover, flash, jobs, models, telemetry, transcribe
    from agent.auth import TokenAuthMiddleware
    from agent.config import (
        DEFAULT_USER,
        active_target,
        auth_token as get_auth_token,
        load as load_cfg,
        save as save_cfg,
        set_target,
    )
    AGENT_MODULES_AVAILABLE = True
except ImportError:
    AGENT_MODULES_AVAILABLE = False
    DEFAULT_USER = "jetson"


# =============================================================================
# Configuration
# =============================================================================

JETSON_HOST = os.getenv("JETSON_HOST", "jetson.local")
JETSON_USER = os.getenv("JETSON_USER", "jetson")
AUTH_TOKEN = os.getenv("AGENT_AUTH_TOKEN", "")

KNOWN_IMAGES = [
    {
        "name": "Raspberry Pi OS Lite (arm64)",
        "url": "https://downloads.raspberrypi.com/raspios_lite_arm64_latest",
    },
    {
        "name": "Ubuntu Server 24.04 (RPI arm64)",
        "url": "https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04.1-preinstalled-server-arm64+raspi.img.xz",
    },
    {
        "name": "BlackRoad OS (latest)",
        "url": "https://releases.blackroad.io/os/latest.img.xz",
        "sha256": "https://releases.blackroad.io/os/latest.sha256",
    },
]


# =============================================================================
# FastAPI Application
# =============================================================================

app = FastAPI(
    title="BlackRoad Agent API",
    version="2.0.0",
    description="Unified API for BlackRoad OS agent system",
    docs_url="/_docs",
    redoc_url="/_redoc",
)

# Add middleware if available
if AGENT_MODULES_AVAILABLE:
    app.add_middleware(TokenAuthMiddleware)

# Templates directory
_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
if _TEMPLATES_DIR.exists():
    templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
else:
    templates = None


# =============================================================================
# Request/Response Models
# =============================================================================

class JobRequest(BaseModel):
    """Request model for job execution."""
    command: str
    host: Optional[str] = None
    user: Optional[str] = None


class ModelRunRequest(BaseModel):
    """Request model for local model inference."""
    model: str
    prompt: str
    n: int = 128


class SettingsAuthRequest(BaseModel):
    """Request model for authentication token update."""
    token: str


class TargetRequest(BaseModel):
    """Request model for setting target device."""
    host: str
    user: str = DEFAULT_USER


# =============================================================================
# Authentication
# =============================================================================

def require_bearer_token(authorization: str = Header(default="")) -> None:
    """Validate Bearer token for protected endpoints."""
    if not AUTH_TOKEN:
        return  # No auth required if token not configured

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )


# =============================================================================
# WebSocket Connection Manager
# =============================================================================

class ConnectionManager:
    """WebSocket connection manager for streaming logs and events."""

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)

    async def broadcast(self, message: str) -> None:
        for ws in list(self._connections):
            try:
                await ws.send_text(message)
            except RuntimeError:
                self.disconnect(ws)


manager = ConnectionManager()


# =============================================================================
# Health & Dashboard Endpoints
# =============================================================================

@app.get("/healthz")
def healthcheck() -> Dict[str, Any]:
    """Return a minimal health payload."""
    auth_enabled = bool(AUTH_TOKEN) if not AGENT_MODULES_AVAILABLE else bool(get_auth_token())
    return {
        "ok": True,
        "auth": auth_enabled,
        "modules_available": AGENT_MODULES_AVAILABLE,
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    """Serve the dashboard UI."""
    if templates is None:
        return HTMLResponse("<h1>BlackRoad Agent API</h1><p>Dashboard not available</p>")

    context: Dict[str, Any] = {"request": request}
    if AGENT_MODULES_AVAILABLE:
        context["target"] = active_target()
    return templates.TemplateResponse("dashboard.html", context)


# =============================================================================
# Settings Endpoints
# =============================================================================

@app.get("/settings")
def get_settings(_: None = Depends(require_bearer_token)) -> Dict[str, Any]:
    """Return the active configuration."""
    if not AGENT_MODULES_AVAILABLE:
        return {
            "jetson": {"host": JETSON_HOST, "user": JETSON_USER},
            "raw": {},
        }

    host, user = active_target()
    return {
        "jetson": {"host": host, "user": user},
        "raw": load_cfg(),
    }


@app.post("/settings/auth")
def set_auth_token(payload: SettingsAuthRequest) -> Dict[str, Any]:
    """Persist a new shared authentication token."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}

    token = payload.token.strip()
    cfg = load_cfg()
    cfg.setdefault("auth", {})["token"] = token
    save_cfg(cfg)
    return {"ok": True, "enabled": bool(token)}


@app.post("/settings/jetson")
def set_jetson_target(target: TargetRequest) -> Dict[str, Any]:
    """Set the active Jetson target."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}

    try:
        set_target(target.host, target.user)
        return {"ok": True, "jetson": {"host": target.host, "user": target.user}}
    except (ValueError, OSError) as exc:
        return {"ok": False, "error": str(exc)}


# =============================================================================
# Discovery Endpoints
# =============================================================================

@app.get("/discover/scan")
def discover_scan() -> Dict[str, Any]:
    """Scan for available devices."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}
    return discover.scan()


@app.get("/discover/target")
def discover_target() -> Dict[str, Any]:
    """Return the currently active target."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "jetson": None}

    target = active_target()
    if not target:
        return {"ok": False, "jetson": None}
    return {"ok": True, "jetson": target}


@app.post("/discover/set")
def discover_set(payload: TargetRequest) -> Dict[str, Any]:
    """Set the active target device."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}

    try:
        set_target(payload.host, payload.user)
        return {"ok": True}
    except (ValueError, OSError) as exc:
        return {"ok": False, "error": str(exc)}


# =============================================================================
# Telemetry Endpoints
# =============================================================================

@app.get("/status")
def status_endpoint(_: None = Depends(require_bearer_token)) -> Dict[str, Any]:
    """Return telemetry for Pi and Jetson."""
    if not AGENT_MODULES_AVAILABLE:
        return {
            "target": {"host": JETSON_HOST, "user": JETSON_USER},
            "pi": {"status": "unavailable"},
            "jetson": {"status": "unavailable"},
        }

    try:
        pi = telemetry.collect_local()
    except Exception as exc:
        pi = {"status": "error", "detail": str(exc)}

    try:
        jetson = telemetry.collect_remote(JETSON_HOST, user=JETSON_USER)
    except Exception as exc:
        jetson = {"status": "error", "detail": str(exc)}

    return {
        "target": {"host": JETSON_HOST, "user": JETSON_USER},
        "pi": pi,
        "jetson": jetson,
    }


@app.get("/telemetry/local")
def telemetry_local() -> Dict[str, Any]:
    """Expose local telemetry for the dashboard."""
    if not AGENT_MODULES_AVAILABLE:
        return {"status": "unavailable"}
    return telemetry.collect_local()


@app.get("/telemetry/remote")
def telemetry_remote(
    host: Optional[str] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """Expose remote telemetry, allowing overrides via query parameters."""
    if not AGENT_MODULES_AVAILABLE:
        return {"status": "unavailable"}
    return telemetry.collect_remote(host=host, user=user)


@app.get("/connect/test")
def connect_test() -> Dict[str, Any]:
    """Attempt to gather telemetry from the Pi and Jetson."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}

    try:
        pi = telemetry.collect_local()
        jetson = telemetry.collect_remote()
        ok = all(not str(value).startswith("error") for value in jetson.values())
        return {"ok": ok, "pi": pi, "jetson": jetson}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# =============================================================================
# Job Execution Endpoints
# =============================================================================

@app.post("/run")
def run_job(req: JobRequest, _: None = Depends(require_bearer_token)) -> Dict[str, Any]:
    """Run a command on the Jetson."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}

    try:
        result = jobs.run_remote(
            req.host or JETSON_HOST,
            req.command,
            user=req.user or JETSON_USER,
        )
        return {
            "ok": result.returncode == 0,
            "stdout": (result.stdout or "").strip(),
            "stderr": (result.stderr or "").strip(),
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/jobs/run")
def jobs_run(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Execute a remote command on the Jetson target."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}

    command = payload.get("command")
    host = payload.get("host")
    user = payload.get("user")
    if not command:
        return {"ok": False, "error": "command required"}

    result = jobs.run_remote(command, host=host, user=user)
    return {
        "ok": result.returncode == 0,
        "stdout": (result.stdout or "").strip(),
        "stderr": (result.stderr or "").strip(),
    }


# =============================================================================
# Flash Endpoints
# =============================================================================

@app.get("/flash/devices")
async def flash_devices() -> Dict[str, Any]:
    """Return removable block devices available for flashing."""
    if not AGENT_MODULES_AVAILABLE:
        return {"devices": [], "error": "Agent modules not available"}

    try:
        data = await asyncio.to_thread(flash.list_devices)
        if isinstance(data, dict):
            message = data.get("error", "Failed to enumerate devices")
            raise HTTPException(status_code=500, detail=message)
        return {"devices": data}
    except HTTPException:
        raise
    except Exception as exc:
        return {"devices": [], "error": str(exc)}


@app.get("/flash/images")
def flash_images() -> Dict[str, Any]:
    """Return curated image suggestions."""
    return {"images": KNOWN_IMAGES}


@app.get("/flash/probe")
def flash_probe(
    host: Optional[str] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """Call the flash probe helper."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}
    return flash.probe(host=host, user=user)


@app.websocket("/ws/flash")
async def ws_flash(ws: WebSocket) -> None:
    """Stream flashing progress to the dashboard."""
    if not AGENT_MODULES_AVAILABLE:
        await ws.accept()
        await ws.send_text("ERROR: Agent modules not available")
        await ws.close()
        return

    await ws.accept()
    stop = threading.Event()
    queue: asyncio.Queue[Optional[str]] = asyncio.Queue()
    thread: Optional[threading.Thread] = None

    try:
        msg = await ws.receive_json()
        device = msg.get("device")
        image_url = msg.get("image_url")
        safe_hdmi = bool(msg.get("safe_hdmi", True))
        enable_ssh = bool(msg.get("enable_ssh", True))

        if not device or not image_url:
            await ws.send_text("ERROR: device and image_url are required")
            await ws.send_text("[[BLACKROAD_DONE]]")
            return

        loop = asyncio.get_running_loop()

        def worker() -> None:
            try:
                for line in flash.flash(
                    image_url,
                    device,
                    safe_hdmi=safe_hdmi,
                    enable_ssh=enable_ssh,
                ):
                    if stop.is_set():
                        break
                    asyncio.run_coroutine_threadsafe(queue.put(line), loop)
            except Exception as exc:
                asyncio.run_coroutine_threadsafe(queue.put(f"ERROR: {exc}"), loop)
            finally:
                asyncio.run_coroutine_threadsafe(queue.put(None), loop)

        thread = threading.Thread(target=worker, name="flash-writer", daemon=True)
        thread.start()

        while True:
            line = await queue.get()
            if line is None:
                break
            await ws.send_text(line)

        await ws.send_text("[[BLACKROAD_DONE]]")
    except WebSocketDisconnect:
        return
    except Exception as exc:
        await ws.send_text(f"ERROR: {exc}")
        await ws.send_text("[[BLACKROAD_DONE]]")
    finally:
        stop.set()
        if thread is not None:
            thread.join(timeout=1)
        if ws.client_state == WebSocketState.CONNECTED:
            await ws.close()


# =============================================================================
# Model Endpoints
# =============================================================================

@app.get("/models")
async def get_models() -> JSONResponse:
    """Return available local models."""
    if not AGENT_MODULES_AVAILABLE:
        return JSONResponse({"models": [], "error": "Agent modules not available"})
    return JSONResponse({"models": models.list_local_models()})


@app.post("/models/run")
def models_run(payload: ModelRunRequest) -> Dict[str, Any]:
    """Run a llama.cpp model once with the provided prompt."""
    if not AGENT_MODULES_AVAILABLE:
        return {"error": "Agent modules not available"}

    model_path = Path(payload.model)
    if not model_path.exists():
        candidate = models.MODELS_DIR / payload.model
        model_path = candidate if candidate.exists() else model_path

    try:
        resolved = model_path.resolve(strict=True)
    except FileNotFoundError:
        return {"error": f"model not found: {payload.model}"}

    try:
        resolved.relative_to(models.MODELS_DIR.resolve())
    except ValueError:
        return {"error": "model must live under /var/lib/blackroad/models"}

    return models.run_llama(str(resolved), payload.prompt, n_predict=payload.n)


@app.websocket("/ws/model")
async def ws_model(ws: WebSocket) -> None:
    """Stream llama.cpp output over the websocket connection."""
    if not AGENT_MODULES_AVAILABLE:
        await ws.accept()
        await ws.send_text("[error] Agent modules not available")
        await ws.send_text("[[BLACKROAD_MODEL_DONE]]")
        await ws.close()
        return

    await ws.accept()
    try:
        message = await ws.receive_json()
        model = message.get("model")
        prompt = message.get("prompt", "")
        try:
            n_predict = int(message.get("n", 128))
        except (TypeError, ValueError):
            n_predict = 128

        if not model:
            await ws.send_text("[error] model path missing")
            await ws.send_text("[[BLACKROAD_MODEL_DONE]]")
            return

        loop = asyncio.get_running_loop()
        done_event = asyncio.Event()

        def stream_tokens() -> None:
            try:
                for token in models.run_llama_stream(model, prompt, n_predict=n_predict):
                    send_future = asyncio.run_coroutine_threadsafe(
                        ws.send_text(token), loop
                    )
                    try:
                        send_future.result()
                    except WebSocketDisconnect:
                        break
            except Exception as exc:
                asyncio.run_coroutine_threadsafe(
                    ws.send_text(f"[error] {exc}"), loop
                ).result()
            finally:
                asyncio.run_coroutine_threadsafe(
                    ws.send_text("[[BLACKROAD_MODEL_DONE]]"), loop
                ).result()
                loop.call_soon_threadsafe(done_event.set)

        await asyncio.gather(asyncio.to_thread(stream_tokens), done_event.wait())
    except WebSocketDisconnect:
        return
    except Exception as exc:
        await ws.send_text(f"[error] {exc}")
        await ws.send_text("[[BLACKROAD_MODEL_DONE]]")
    finally:
        with contextlib.suppress(RuntimeError):
            await ws.close()


# =============================================================================
# Transcription Endpoints
# =============================================================================

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)) -> Dict[str, str]:
    """Accept an uploaded audio file and run whisper.cpp locally."""
    if not AGENT_MODULES_AVAILABLE:
        return {"error": "Agent modules not available"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        data = await file.read()
        tmp.write(data)
        tmp_path = pathlib.Path(tmp.name)

    try:
        text = transcribe.run_whisper(str(tmp_path))
    finally:
        tmp_path.unlink(missing_ok=True)

    return {"text": text}


@app.post("/transcribe/upload")
async def transcribe_upload(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload audio for transcription and get a token for streaming."""
    if not AGENT_MODULES_AVAILABLE:
        return {"error": "Agent modules not available"}

    data = await file.read()
    suffix = pathlib.Path(file.filename or "audio.wav").suffix
    path = transcribe.save_upload(data, suffix=suffix)
    token = pathlib.Path(path).name
    return {"token": token}


@app.websocket("/ws/transcribe/run")
async def ws_transcribe(ws: WebSocket) -> None:
    """Stream transcription output over WebSocket."""
    if not AGENT_MODULES_AVAILABLE:
        await ws.accept()
        await ws.send_text("[error] Agent modules not available")
        await ws.close()
        return

    await ws.accept()
    try:
        try:
            msg = await ws.receive_text()
        except WebSocketDisconnect:
            return
        except Exception:
            await ws.send_text("[error] invalid request")
            return

        try:
            payload = json.loads(msg)
        except json.JSONDecodeError:
            await ws.send_text("[error] invalid json")
            return

        token = payload.get("token")
        lang = payload.get("lang", "en")
        model = payload.get("model")

        if not token:
            await ws.send_text("[error] missing token")
            return

        candidate = (transcribe.TMP_DIR / token).resolve()
        try:
            candidate.relative_to(transcribe.TMP_DIR)
        except ValueError:
            await ws.send_text("[error] bad token")
            return

        if not candidate.exists():
            await ws.send_text("[error] audio not found")
            return

        queue: asyncio.Queue[tuple[str, Optional[str]]] = asyncio.Queue()
        loop = asyncio.get_running_loop()

        def pump_stream() -> None:
            try:
                for line in transcribe.run_whisper_stream(
                    str(candidate), model_path=model, lang=lang
                ):
                    loop.call_soon_threadsafe(queue.put_nowait, ("data", line))
            except Exception as exc:
                loop.call_soon_threadsafe(queue.put_nowait, ("error", str(exc)))
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, ("done", None))

        thread = threading.Thread(target=pump_stream, name="whisper-stream", daemon=True)
        thread.start()

        try:
            while True:
                kind, payload_data = await queue.get()

                try:
                    if kind == "data" and payload_data is not None:
                        await ws.send_text(payload_data)
                    elif kind == "error" and payload_data is not None:
                        await ws.send_text(f"[error] {payload_data}")
                    elif kind == "done":
                        await ws.send_text("[[BLACKROAD_WHISPER_DONE]]")
                        break
                except WebSocketDisconnect:
                    break
        finally:
            if thread.is_alive():
                await asyncio.to_thread(thread.join)
    finally:
        try:
            await ws.close()
        except (WebSocketDisconnect, RuntimeError):
            pass


# =============================================================================
# WebSocket Logs
# =============================================================================

@app.websocket("/ws/logs")
async def logs_websocket(websocket: WebSocket) -> None:
    """Simple echo socket that allows clients to keep an open channel."""
    await manager.connect(websocket)
    try:
        while True:
            try:
                payload = await websocket.receive_text()
            except RuntimeError:
                break
            await manager.broadcast(json.dumps({"echo": payload}))
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)


# =============================================================================
# SSH Key Installation
# =============================================================================

@app.post("/connect/install-key")
def install_key() -> Dict[str, Any]:
    """Generate an SSH key for the `pi` user and copy it to the Jetson target."""
    if not AGENT_MODULES_AVAILABLE:
        return {"ok": False, "error": "Agent modules not available"}

    import subprocess

    host, user = active_target()
    home = pathlib.Path("/home/pi")
    ssh_dir = home / ".ssh"
    ssh_dir.mkdir(parents=True, exist_ok=True)
    key_path = ssh_dir / "id_rsa"

    if not key_path.exists():
        subprocess.run(
            [
                "sudo",
                "-u",
                "pi",
                "ssh-keygen",
                "-t",
                "rsa",
                "-N",
                "",
                "-f",
                str(key_path),
            ],
            check=True,
        )

    result = subprocess.call(
        [
            "sudo",
            "-u",
            "pi",
            "ssh-copy-id",
            "-i",
            f"{key_path}.pub",
            f"{user}@{host}",
        ]
    )
    note = (
        "If this returned false, run ssh-copy-id manually in a shell to enter the password."
    )
    return {"ok": result == 0, "note": note}


# =============================================================================
# Module Exports
# =============================================================================

__all__ = ["app", "manager", "ConnectionManager"]
