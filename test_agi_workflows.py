import asyncio
import importlib.util
import sys
import types
from pathlib import Path


def load_module(path: str, name: str, strip_instance: bool = False):
    """Load a module from a path. If strip_instance is True, remove the
    autonomous instance creation line to avoid side effects."""

    if strip_instance:
        source = Path(path).read_text()
        source = source.replace("autonomous_file_updater = AutonomousFileUpdater()", "autonomous_file_updater = None")
        spec = importlib.util.spec_from_loader(name, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(source, module.__dict__)
        sys.modules[name] = module
        return module

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def run_chat_integration():
    chat_mod = load_module(str(Path(__file__).parent / '09-agi-development' / 'agi_chat_integration.py'), 'agi_chat_integration')
    agi = chat_mod.NeuralSymbolicAGIIntegration()

    # Patch heavy methods with lightweight stubs
    agi._create_neural_model = lambda: 'dummy'
    agi._create_symbolic_reasoner = lambda: types.SimpleNamespace(reason=lambda q: {
        "confidence": 0.9,
        "reasoning_steps": [],
        "conclusion": "demo"
    })
    agi._create_knowledge_graph = lambda: types.SimpleNamespace(query=lambda q: [])

    async def stub_process(message, history):
        return {
            "content": "ok",
            "reasoning": "demo",
            "confidence": 0.9,
            "capabilities_used": []
        }

    agi._neural_symbolic_processing = stub_process
    agi._reasoning_processing = stub_process
    agi._creative_processing = stub_process
    agi._analytical_processing = stub_process
    agi._general_processing = stub_process

    assert agi.initialize_neural_symbolic_system()

    resp = await agi.process_chat_message("hello", agent_type="neural-symbolic")
    assert resp["content"] == "ok"
    assert resp["agent_type"] == "neural-symbolic"
    assert len(agi.conversation_memory) == 1


async def run_file_update(tmp_dir: Path):
    fu_mod = load_module(
        '09-agi-development/agi_file_update_system.py',
        'agi_file_update_system',
        strip_instance=True,
    )
    FileUpdateTask = fu_mod.FileUpdateTask
    AutonomousFileUpdater = fu_mod.AutonomousFileUpdater

    # Build instance without running original __init__
    updater = AutonomousFileUpdater.__new__(AutonomousFileUpdater)
    updater.update_tasks = []
    updater.execution_log = []
    updater.workspace_path = tmp_dir
    updater.backup_path = tmp_dir / '.agi_backups'
    updater.config_path = tmp_dir / '.agi_file_config.json'
    updater.neural_model = None
    updater.symbolic_reasoner = None
    updater.knowledge_graph = None
    updater.safe_directories = [str(tmp_dir)]
    updater.restricted_files = []
    updater.backup_path.mkdir(exist_ok=True)
    updater.logger = logging.getLogger("AutonomousFileUpdaterTest")

    # Test file creation
    task = FileUpdateTask(str(tmp_dir / 'demo.txt'), 'create', content='sample', backup=False)
    success = await updater.execute_file_task(task)
    assert success
    assert (tmp_dir / 'demo.txt').exists()

    # Test file update
    update_task = FileUpdateTask(str(tmp_dir / 'demo.txt'), 'update', content='updated content', backup=False)
    update_success = await updater.execute_file_task(update_task)
    assert update_success
    with open(tmp_dir / 'demo.txt', 'r') as f:
        assert f.read() == 'updated content'

    # Test file delete
    delete_task = FileUpdateTask(str(tmp_dir / 'demo.txt'), 'delete', backup=False)
    delete_success = await updater.execute_file_task(delete_task)
    assert delete_success
    assert not (tmp_dir / 'demo.txt').exists()

    # Test file creation with backup
    task_with_backup = FileUpdateTask(str(tmp_dir / 'demo2.txt'), 'create', content='backup test', backup=True)
    backup_success = await updater.execute_file_task(task_with_backup)
    assert backup_success
    assert (tmp_dir / 'demo2.txt').exists()
    # Now update with backup enabled and check backup exists
    update_with_backup = FileUpdateTask(str(tmp_dir / 'demo2.txt'), 'update', content='backup updated', backup=True)
    update_backup_success = await updater.execute_file_task(update_with_backup)
    assert update_backup_success
    backup_files = list(updater.backup_path.glob('demo2.txt*'))
    assert len(backup_files) > 0

    # Test restricted file scenario
    restricted_file = tmp_dir / 'restricted.txt'
    restricted_file.write_text('restricted')
    updater.restricted_files = [str(restricted_file)]
    restricted_task = FileUpdateTask(str(restricted_file), 'update', content='should not update', backup=False)
    restricted_success = await updater.execute_file_task(restricted_task)
    assert not restricted_success
    # File content should remain unchanged
    with open(restricted_file, 'r') as f:
        assert f.read() == 'restricted'
    updater.restricted_files = []
def test_agi_workflow(tmp_path):
    asyncio.run(run_chat_integration())
    asyncio.run(run_file_update(tmp_path))
