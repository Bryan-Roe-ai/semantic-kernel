#!/usr/bin/env python
# Plugin Hot-Reload System - Auto-created by setup.py
import os
import sys
import time
import importlib
import threading
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler("plugin_hotreload.log"),
                             logging.StreamHandler()])

class PluginReloader(FileSystemEventHandler):
    """Watches plugin directory and reloads plugins on change"""
    
    def __init__(self, plugins_dir):
        self.plugins_dir = plugins_dir
        self.last_reload = {}
        self.lock = threading.Lock()
        
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return
            
        path = Path(event.src_path)
        plugin_name = path.stem
        
        # Avoid reloading too frequently (debounce)
        with self.lock:
            now = time.time()
            if plugin_name in self.last_reload and now - self.last_reload[plugin_name] < 2:
                return
            self.last_reload[plugin_name] = now
        
        try:
            # Try to reload the module if it's loaded
            if plugin_name in sys.modules:
                logging.info(f"Hot-reloading plugin: {plugin_name}")
                importlib.reload(sys.modules[plugin_name])
            else:
                logging.info(f"New plugin detected: {plugin_name}")
        except Exception as e:
            logging.error(f"Error reloading plugin {plugin_name}: {str(e)}")

def start_watching(plugins_dir):
    """Start watching the plugins directory"""
    event_handler = PluginReloader(plugins_dir)
    observer = Observer()
    observer.schedule(event_handler, plugins_dir, recursive=True)
    observer.start()
    logging.info(f"Watching for changes in: {plugins_dir}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    plugins_dir = Path(__file__).parent / "plugins"
    start_watching(plugins_dir)
