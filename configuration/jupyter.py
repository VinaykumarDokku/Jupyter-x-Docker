import os

c = get_config()

os.makedirs("/app/notebooks", exist_ok=True)

c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = int(os.environ.get("PORT", 8888))
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True
c.ServerApp.root_dir = "/app/notebooks"
