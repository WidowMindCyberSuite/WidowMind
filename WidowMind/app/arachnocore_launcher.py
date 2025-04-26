import threading
import platform
import subprocess
from agents.network_monitor import scan_ports
from agents.file_monitor import watch_files
from agents.process_monitor import check_processes
from agents.huntsman import huntsman_loop
from core.system_logger import log_system_event
from agents.intelli_spider import launch_intelli_spider
from agents.recluse import launch_recluse

def launch_agent(target_function, name):
    """Helper to launch an agent in its own thread."""
    thread = threading.Thread(target=target_function, name=name)
    thread.daemon = True
    thread.start()
    log_system_event(f"Started agent: {name}")
    return thread

def launch_dashboard():
    """Launch the Flask dashboard server."""
    try:
        subprocess.Popen(["python", "dashboard/dashboard_server.py"])
        log_system_event("Started WidowMind Dashboard server.")
    except Exception as e:
        log_system_event(f"Failed to launch dashboard: {e}")

if __name__ == "__main__":
    print("🕷️ WidowMind: Launching Arachnocore threat agents and dashboard...\n")
    log_system_event("WidowMind Arachnocore initializing...")
    log_system_event(f"Detected OS: {platform.system()}")

    # Launch all agents
    agents = [
        launch_agent(scan_ports, "NetworkMonitor"),
        launch_agent(watch_files, "FileMonitor"),
        launch_agent(check_processes, "ProcessMonitor"),
        launch_agent(huntsman_loop, "Huntsman")
    ]

    # LAUNCH INTELLISPIDER SEPARATELY
    launch_intelli_spider()
    log_system_event("Started agent: IntelliSpider")

    # Launch Recluse Active Threat Neutralizer
    launch_recluse()
    log_system_event("Started agent: Recluse (Active Threat Neutralizer)")

    # Launch dashboard
    launch_dashboard()

    print("\n[+] All agents launched. WidowMind is active.\n")
    print("[+] Dashboard accessible at http://localhost:5000\n")
    log_system_event("All agents and dashboard launched successfully.")

    # Keep main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[!] WidowMind Arachnocore shutting down...")
        log_system_event("WidowMind Arachnocore shutdown requested by user.")
