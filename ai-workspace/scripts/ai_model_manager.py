#!/usr/bin/env python3
"""
AI Model Manager
Advanced model lifecycle management for the AI workspace.
"""

import os
import sys
import json
import shutil
import hashlib
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import logging
import subprocess
import tempfile
import zipfile

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIModelManager:
    def __init__(self, workspace_root="/workspaces/semantic-kernel/ai-workspace"):
        self.workspace_root = Path(workspace_root)
        self.models_dir = self.workspace_root / "models"
        self.models_dir.mkdir(exist_ok=True)
        
        self.registry_file = self.models_dir / "model_registry.json"
        self.cache_dir = self.models_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.model_registry = self._load_registry()
        
    def _load_registry(self) -> Dict[str, Any]:
        """Load model registry from file."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading registry: {e}")
        
        return {
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "models": {}
        }
    
    def _save_registry(self):
        """Save model registry to file."""
        self.model_registry["last_updated"] = datetime.now().isoformat()
        with open(self.registry_file, 'w') as f:
            json.dump(self.model_registry, f, indent=2)
    
    def list_models(self, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all registered models."""
        models = []
        
        for model_id, model_info in self.model_registry["models"].items():
            if filter_type and model_info.get("type") != filter_type:
                continue
                
            # Add runtime information
            model_path = Path(model_info["path"])
            model_info_extended = model_info.copy()
            model_info_extended.update({
                "id": model_id,
                "exists": model_path.exists(),
                "size_mb": self._get_model_size(model_path),
                "last_used": self._get_last_used(model_id)
            })
            
            models.append(model_info_extended)
        
        return sorted(models, key=lambda x: x.get("created", ""), reverse=True)
    
    def download_model(self, source: str, model_id: Optional[str] = None, 
                      model_type: str = "transformers") -> str:
        """Download model from various sources."""
        print(f"📥 Downloading model from: {source}")
        
        if model_id is None:
            model_id = self._generate_model_id(source)
        
        if model_id in self.model_registry["models"]:
            print(f"⚠️  Model {model_id} already exists. Use update_model() to replace.")
            return model_id
        
        # Determine download method based on source
        if source.startswith("http"):
            model_path = self._download_from_url(source, model_id)
        elif source.startswith("hf:") or "/" in source:
            model_path = self._download_from_huggingface(source.replace("hf:", ""), model_id)
        elif source.startswith("file:"):
            model_path = self._import_local_model(source.replace("file:", ""), model_id)
        else:
            # Try as Hugging Face model
            model_path = self._download_from_huggingface(source, model_id)
        
        # Register model
        self._register_model(model_id, model_path, model_type, source)
        
        print(f"✅ Model {model_id} downloaded successfully")
        return model_id
    
    def _download_from_url(self, url: str, model_id: str) -> Path:
        """Download model from URL."""
        model_dir = self.models_dir / model_id
        model_dir.mkdir(exist_ok=True)
        
        filename = url.split("/")[-1] or "model.bin"
        model_path = model_dir / filename
        
        print(f"⬇️  Downloading from URL...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r📊 Progress: {progress:.1f}%", end="", flush=True)
        
        print()  # New line after progress
        return model_path
    
    def _download_from_huggingface(self, model_name: str, model_id: str) -> Path:
        """Download model from Hugging Face."""
        try:
            from transformers import AutoModel, AutoTokenizer
            from huggingface_hub import snapshot_download
        except ImportError:
            raise ImportError("transformers and huggingface_hub required for HF downloads")
        
        model_dir = self.models_dir / model_id
        
        print(f"🤗 Downloading from Hugging Face: {model_name}")
        
        # Download model files
        snapshot_download(
            repo_id=model_name,
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
        
        return model_dir
    
    def _import_local_model(self, local_path: str, model_id: str) -> Path:
        """Import model from local file system."""
        source_path = Path(local_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Local model not found: {local_path}")
        
        model_dir = self.models_dir / model_id
        model_dir.mkdir(exist_ok=True)
        
        if source_path.is_file():
            # Single file model
            shutil.copy2(source_path, model_dir / source_path.name)
            return model_dir / source_path.name
        else:
            # Directory model
            shutil.copytree(source_path, model_dir, dirs_exist_ok=True)
            return model_dir
    
    def _register_model(self, model_id: str, model_path: Path, 
                       model_type: str, source: str):
        """Register model in registry."""
        model_info = {
            "path": str(model_path.relative_to(self.workspace_root)),
            "type": model_type,
            "source": source,
            "created": datetime.now().isoformat(),
            "checksum": self._calculate_checksum(model_path),
            "metadata": self._extract_metadata(model_path)
        }
        
        self.model_registry["models"][model_id] = model_info
        self._save_registry()
    
    def update_model(self, model_id: str, source: Optional[str] = None) -> bool:
        """Update existing model."""
        if model_id not in self.model_registry["models"]:
            raise ValueError(f"Model {model_id} not found")
        
        model_info = self.model_registry["models"][model_id]
        
        # Create backup
        backup_id = f"{model_id}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self._backup_model(model_id, backup_id)
        
        try:
            # Remove old model
            old_path = Path(model_info["path"])
            if old_path.exists():
                if old_path.is_file():
                    old_path.unlink()
                else:
                    shutil.rmtree(old_path)
            
            # Download new version
            source = source or model_info["source"]
            new_path = self._download_from_source(source, model_id)
            
            # Update registry
            model_info.update({
                "path": str(new_path.relative_to(self.workspace_root)),
                "updated": datetime.now().isoformat(),
                "checksum": self._calculate_checksum(new_path),
                "metadata": self._extract_metadata(new_path)
            })
            
            self._save_registry()
            print(f"✅ Model {model_id} updated successfully")
            return True
            
        except Exception as e:
            # Restore backup on failure
            print(f"❌ Update failed: {e}")
            self._restore_backup(backup_id, model_id)
            return False
    
    def delete_model(self, model_id: str, confirm: bool = False) -> bool:
        """Delete model and remove from registry."""
        if model_id not in self.model_registry["models"]:
            raise ValueError(f"Model {model_id} not found")
        
        if not confirm:
            print(f"⚠️  This will permanently delete model {model_id}")
            return False
        
        model_info = self.model_registry["models"][model_id]
        model_path = Path(model_info["path"])
        
        # Remove files
        if model_path.exists():
            if model_path.is_file():
                model_path.unlink()
            else:
                shutil.rmtree(model_path)
        
        # Remove from registry
        del self.model_registry["models"][model_id]
        self._save_registry()
        
        print(f"🗑️  Model {model_id} deleted")
        return True
    
    def optimize_model(self, model_id: str, optimization_type: str = "quantization") -> str:
        """Optimize model for deployment."""
        if model_id not in self.model_registry["models"]:
            raise ValueError(f"Model {model_id} not found")
        
        model_info = self.model_registry["models"][model_id]
        optimized_id = f"{model_id}_optimized_{optimization_type}"
        
        print(f"🔧 Optimizing model {model_id} with {optimization_type}")
        
        if optimization_type == "quantization":
            optimized_path = self._quantize_model(model_info, optimized_id)
        elif optimization_type == "pruning":
            optimized_path = self._prune_model(model_info, optimized_id)
        elif optimization_type == "distillation":
            optimized_path = self._distill_model(model_info, optimized_id)
        else:
            raise ValueError(f"Unknown optimization type: {optimization_type}")
        
        # Register optimized model
        optimized_info = model_info.copy()
        optimized_info.update({
            "path": str(optimized_path.relative_to(self.workspace_root)),
            "created": datetime.now().isoformat(),
            "optimized_from": model_id,
            "optimization_type": optimization_type,
            "checksum": self._calculate_checksum(optimized_path)
        })
        
        self.model_registry["models"][optimized_id] = optimized_info
        self._save_registry()
        
        print(f"✅ Optimized model created: {optimized_id}")
        return optimized_id
    
    def benchmark_model(self, model_id: str) -> Dict[str, Any]:
        """Benchmark model performance."""
        if model_id not in self.model_registry["models"]:
            raise ValueError(f"Model {model_id} not found")
        
        print(f"🏃 Benchmarking model {model_id}")
        
        model_info = self.model_registry["models"][model_id]
        model_path = Path(model_info["path"])
        
        benchmarks = {
            "model_id": model_id,
            "timestamp": datetime.now().isoformat(),
            "file_size": self._get_model_size(model_path),
            "load_time": self._benchmark_load_time(model_path),
            "inference_time": self._benchmark_inference_time(model_path),
            "memory_usage": self._benchmark_memory_usage(model_path)
        }
        
        # Save benchmark results
        benchmark_file = self.models_dir / f"benchmark_{model_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(benchmark_file, 'w') as f:
            json.dump(benchmarks, f, indent=2)
        
        return benchmarks
    
    def cleanup_models(self, keep_days: int = 30) -> Dict[str, Any]:
        """Clean up old and unused models."""
        print(f"🧹 Cleaning up models older than {keep_days} days")
        
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        cleanup_results = {
            "removed_models": [],
            "space_freed": 0,
            "errors": []
        }
        
        for model_id, model_info in list(self.model_registry["models"].items()):
            try:
                created_date = datetime.fromisoformat(model_info["created"])
                last_used = self._get_last_used_date(model_id)
                
                # Check if model should be removed
                should_remove = (
                    created_date < cutoff_date and
                    (last_used is None or last_used < cutoff_date)
                )
                
                if should_remove:
                    model_path = Path(model_info["path"])
                    size_before = self._get_model_size(model_path)
                    
                    self.delete_model(model_id, confirm=True)
                    
                    cleanup_results["removed_models"].append(model_id)
                    cleanup_results["space_freed"] += size_before
                    
            except Exception as e:
                cleanup_results["errors"].append(f"Error cleaning {model_id}: {e}")
        
        print(f"🗑️  Removed {len(cleanup_results['removed_models'])} models")
        print(f"💾 Freed {cleanup_results['space_freed']/1024/1024:.2f} MB")
        
        return cleanup_results
    
    def export_model(self, model_id: str, export_path: str, 
                    format_type: str = "zip") -> str:
        """Export model for sharing or deployment."""
        if model_id not in self.model_registry["models"]:
            raise ValueError(f"Model {model_id} not found")
        
        model_info = self.model_registry["models"][model_id]
        model_path = Path(model_info["path"])
        export_path = Path(export_path)
        
        print(f"📦 Exporting model {model_id} to {export_path}")
        
        if format_type == "zip":
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if model_path.is_file():
                    zipf.write(model_path, model_path.name)
                else:
                    for file_path in model_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(model_path)
                            zipf.write(file_path, arcname)
                
                # Add metadata
                metadata = {
                    "model_id": model_id,
                    "export_date": datetime.now().isoformat(),
                    "model_info": model_info
                }
                zipf.writestr("metadata.json", json.dumps(metadata, indent=2))
        
        elif format_type == "tar":
            import tarfile
            with tarfile.open(export_path, 'w:gz') as tar:
                tar.add(model_path, arcname=model_id)
        
        else:
            # Direct copy
            if model_path.is_file():
                shutil.copy2(model_path, export_path)
            else:
                shutil.copytree(model_path, export_path)
        
        print(f"✅ Model exported to {export_path}")
        return str(export_path)
    
    def import_model(self, import_path: str, model_id: Optional[str] = None) -> str:
        """Import model from exported package."""
        import_path = Path(import_path)
        
        if not import_path.exists():
            raise FileNotFoundError(f"Import file not found: {import_path}")
        
        print(f"📥 Importing model from {import_path}")
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Extract if needed
            if import_path.suffix == '.zip':
                with zipfile.ZipFile(import_path, 'r') as zipf:
                    zipf.extractall(temp_path)
                    
                    # Load metadata if available
                    metadata_file = temp_path / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            if not model_id:
                                model_id = metadata.get("model_id")
                            # Remove metadata file from import
                            metadata_file.unlink()
            
            elif import_path.suffix in ['.tar', '.gz']:
                import tarfile
                with tarfile.open(import_path, 'r') as tar:
                    tar.extractall(temp_path)
            
            else:
                # Direct file/directory
                if import_path.is_file():
                    shutil.copy2(import_path, temp_path)
                else:
                    shutil.copytree(import_path, temp_path / import_path.name)
            
            # Generate model ID if not provided
            if not model_id:
                model_id = f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Move to models directory
            model_dir = self.models_dir / model_id
            if model_dir.exists():
                shutil.rmtree(model_dir)
            
            # Find the actual model files in temp directory
            temp_contents = list(temp_path.iterdir())
            if len(temp_contents) == 1 and temp_contents[0].is_dir():
                # Single directory, move contents
                shutil.move(temp_contents[0], model_dir)
            else:
                # Multiple files, move all
                model_dir.mkdir()
                for item in temp_contents:
                    dest = model_dir / item.name
                    shutil.move(item, dest)
        
        # Register imported model
        self._register_model(model_id, model_dir, "imported", str(import_path))
        
        print(f"✅ Model imported as {model_id}")
        return model_id
    
    # Helper methods
    def _generate_model_id(self, source: str) -> str:
        """Generate unique model ID from source."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        source_hash = hashlib.md5(source.encode()).hexdigest()[:8]
        return f"model_{timestamp}_{source_hash}"
    
    def _get_model_size(self, model_path: Path) -> float:
        """Get model size in MB."""
        if not model_path.exists():
            return 0.0
        
        if model_path.is_file():
            return model_path.stat().st_size / (1024 * 1024)
        else:
            total_size = sum(
                f.stat().st_size for f in model_path.rglob('*') if f.is_file()
            )
            return total_size / (1024 * 1024)
    
    def _calculate_checksum(self, path: Path) -> str:
        """Calculate SHA256 checksum of model."""
        sha256_hash = hashlib.sha256()
        
        if path.is_file():
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
        else:
            # For directories, hash all file contents
            for file_path in sorted(path.rglob('*')):
                if file_path.is_file():
                    with open(file_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def _extract_metadata(self, model_path: Path) -> Dict[str, Any]:
        """Extract metadata from model."""
        metadata = {}
        
        # Check for common metadata files
        metadata_files = ["config.json", "model_config.json", "tokenizer_config.json"]
        
        for file_name in metadata_files:
            if model_path.is_dir():
                metadata_file = model_path / file_name
            else:
                metadata_file = model_path.parent / file_name
                
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        file_metadata = json.load(f)
                        metadata[file_name] = file_metadata
                except Exception as e:
                    logger.warning(f"Could not read {file_name}: {e}")
        
        return metadata
    
    def _get_last_used(self, model_id: str) -> Optional[str]:
        """Get last used timestamp for model."""
        # This would typically be tracked in a usage log
        # For now, return None
        return None
    
    def _get_last_used_date(self, model_id: str) -> Optional[datetime]:
        """Get last used date for model."""
        last_used = self._get_last_used(model_id)
        if last_used:
            return datetime.fromisoformat(last_used)
        return None
    
    # Optimization methods (placeholders for now)
    def _quantize_model(self, model_info: Dict, optimized_id: str) -> Path:
        """Quantize model to reduce size."""
        # Placeholder implementation
        optimized_dir = self.models_dir / optimized_id
        optimized_dir.mkdir(exist_ok=True)
        
        # In a real implementation, this would use libraries like:
        # - torch.quantization
        # - transformers optimization
        # - ONNX quantization
        
        print("⚠️  Quantization is a placeholder implementation")
        return optimized_dir
    
    def _prune_model(self, model_info: Dict, optimized_id: str) -> Path:
        """Prune model to reduce parameters."""
        optimized_dir = self.models_dir / optimized_id
        optimized_dir.mkdir(exist_ok=True)
        print("⚠️  Pruning is a placeholder implementation")
        return optimized_dir
    
    def _distill_model(self, model_info: Dict, optimized_id: str) -> Path:
        """Distill model to smaller version."""
        optimized_dir = self.models_dir / optimized_id
        optimized_dir.mkdir(exist_ok=True)
        print("⚠️  Distillation is a placeholder implementation")
        return optimized_dir
    
    # Benchmarking methods (placeholders)
    def _benchmark_load_time(self, model_path: Path) -> float:
        """Benchmark model loading time."""
        import time
        start = time.time()
        # Simulate loading
        time.sleep(0.1)
        return time.time() - start
    
    def _benchmark_inference_time(self, model_path: Path) -> float:
        """Benchmark inference time."""
        import time
        # Simulate inference
        time.sleep(0.05)
        return 0.05
    
    def _benchmark_memory_usage(self, model_path: Path) -> float:
        """Benchmark memory usage."""
        # Placeholder - would use actual model loading and memory profiling
        return self._get_model_size(model_path) * 1.5  # Approximate
    
    def _backup_model(self, model_id: str, backup_id: str):
        """Create backup of model."""
        # Implementation would copy model to backup location
        pass
    
    def _restore_backup(self, backup_id: str, model_id: str):
        """Restore model from backup."""
        # Implementation would restore model from backup
        pass
    
    def _download_from_source(self, source: str, model_id: str) -> Path:
        """Download model from source URL."""
        if source.startswith("http"):
            return self._download_from_url(source, model_id)
        elif source.startswith("hf:") or "/" in source:
            return self._download_from_huggingface(source.replace("hf:", ""), model_id)
        else:
            return self._download_from_huggingface(source, model_id)

def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Model Manager")
    parser.add_argument("command", choices=[
        "list", "download", "update", "delete", "optimize", 
        "benchmark", "cleanup", "export", "import"
    ])
    parser.add_argument("--model-id", help="Model ID")
    parser.add_argument("--source", help="Model source (URL, HF model name, etc.)")
    parser.add_argument("--type", default="transformers", help="Model type")
    parser.add_argument("--path", help="File path for import/export")
    parser.add_argument("--format", default="zip", help="Export format")
    parser.add_argument("--optimization", default="quantization", help="Optimization type")
    parser.add_argument("--days", type=int, default=30, help="Days for cleanup")
    parser.add_argument("--confirm", action="store_true", help="Confirm destructive operations")
    parser.add_argument("--workspace", default="/workspaces/semantic-kernel/ai-workspace")
    
    args = parser.parse_args()
    
    manager = AIModelManager(args.workspace)
    
    try:
        if args.command == "list":
            models = manager.list_models()
            print(json.dumps(models, indent=2))
            
        elif args.command == "download":
            if not args.source:
                print("Error: --source required for download")
                sys.exit(1)
            model_id = manager.download_model(args.source, args.model_id, args.type)
            print(f"Downloaded model: {model_id}")
            
        elif args.command == "update":
            if not args.model_id:
                print("Error: --model-id required for update")
                sys.exit(1)
            success = manager.update_model(args.model_id, args.source)
            sys.exit(0 if success else 1)
            
        elif args.command == "delete":
            if not args.model_id:
                print("Error: --model-id required for delete")
                sys.exit(1)
            success = manager.delete_model(args.model_id, args.confirm)
            sys.exit(0 if success else 1)
            
        elif args.command == "optimize":
            if not args.model_id:
                print("Error: --model-id required for optimize")
                sys.exit(1)
            optimized_id = manager.optimize_model(args.model_id, args.optimization)
            print(f"Optimized model: {optimized_id}")
            
        elif args.command == "benchmark":
            if not args.model_id:
                print("Error: --model-id required for benchmark")
                sys.exit(1)
            results = manager.benchmark_model(args.model_id)
            print(json.dumps(results, indent=2))
            
        elif args.command == "cleanup":
            results = manager.cleanup_models(args.days)
            print(json.dumps(results, indent=2))
            
        elif args.command == "export":
            if not args.model_id or not args.path:
                print("Error: --model-id and --path required for export")
                sys.exit(1)
            export_path = manager.export_model(args.model_id, args.path, args.format)
            print(f"Exported to: {export_path}")
            
        elif args.command == "import":
            if not args.path:
                print("Error: --path required for import")
                sys.exit(1)
            model_id = manager.import_model(args.path, args.model_id)
            print(f"Imported model: {model_id}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
