import subprocess
import time

import comparison.constants as c
from comparison.logging import setup_logging, get_logger

logger = get_logger()


def swarm_server(
    address: str,
    users: int,
    spawn_rate: int,
    duration: int,
    save_results_to: str,
    locust_file: str,
) -> None:
    command = [
        "poetry",
        "run",
        "locust",
        "--locustfile",
        locust_file,
        "--host",
        f"http://{address}",
        "--users",
        str(users),
        "--spawn-rate",
        str(spawn_rate),
        "--run-time",
        str(duration),
        "--csv",
        save_results_to,
        "--headless",
    ]
    logger.info(" ".join(command))
    subprocess.run(command)


def start_flask(num_workers: int, flask_address: str) -> None:
    command = [
        "poetry",
        "run",
        "gunicorn",
        "comparison.main_flask:app",
        "--workers",
        str(num_workers),
        "--bind",
        flask_address,
    ]
    logger.info(" ".join(command))
    subprocess.Popen(command)
    logger.info("Wait 15 seconds for the server to start")
    time.sleep(15)

def start_fastapi(num_workers: int, fastapi_port: int) -> None:
    command = [
        "poetry",
        "run",
        "uvicorn",
        "comparison.main_fastapi:app",
        "--workers",
        str(num_workers),
        "--port",
        str(fastapi_port),
    ]
    logger.info(" ".join(command))
    subprocess.Popen(command)
    logger.info("Wait 15 seconds for the server to start")
    time.sleep(15)

def kill_server(port: int) -> None:
    try:
        proc = subprocess.Popen(['lsof', '-ti', f':{port}'], stdout=subprocess.PIPE)
        pids = proc.stdout.read().decode('utf-8').strip().split('\n')
        for pid in pids:
            if pid:
                subprocess.run(['kill', '-9', pid])
    except Exception as e:
        logger.error(f"Failed to kill server on port {port}: {e}")

if __name__ == "__main__":
    setup_logging()

    locust_file = str(c.ROOT_DIR / "locustfile.py")
    results_dir = c.ROOT_DIR / "results"
    results_dir.mkdir(exist_ok=True)

    host = "127.0.0.1"
    flask_port = 5000
    fastapi_port = 8000
    flask_address= f"{host}:{flask_port}"
    fastapi_address= f"{host}:{fastapi_port}"
    num_workers = 3
    duration = 60
    user_counts = [10, 100, 1_000, 5_000]

    logger.info("Ensure that no other processes are running on ports 5000 and 8000")
    kill_server(flask_port)
    kill_server(fastapi_port)

    logger.info(f"Starting Flask server on {flask_address} with {num_workers} workers")
    start_flask(num_workers, flask_address)
    for users in user_counts:
        logger.info(f"Starting Locust with {users} users for Flask")
        save_results_to = str(results_dir / f"flask_results_{users}")
        logger.info(f"Saving results to {save_results_to}")
        spawn_rate = min(users // 5, 100) # Limit spawn rate to 100, recommended by Locust
        swarm_server(
            address=flask_address,
            users=users,
            spawn_rate=spawn_rate,
            duration=duration,
            save_results_to=save_results_to,
            locust_file=locust_file,
        )
        time.sleep(10)
    logger.info(f"Killing Flask server")
    kill_server(flask_port)

    logger.info(f"Starting FastAPI server on {fastapi_address} with {num_workers} workers")
    start_fastapi(num_workers, fastapi_port)
    for users in user_counts:
        logger.info(f"Starting Locust with {users} users for FastAPI")
        save_results_to = str(results_dir / f"fastapi_results_{users}")
        logger.info(f"Saving results to {save_results_to}")
        spawn_rate = min(users // 5, 100) # Limit spawn rate to 100, recommended by Locust
        swarm_server(
            address=fastapi_address,
            users=users,
            spawn_rate=spawn_rate,
            duration=duration,
            save_results_to=save_results_to,
            locust_file=locust_file,
        )
        time.sleep(10)
    logger.info(f"Killing FastAPI server")
    kill_server(fastapi_port)
