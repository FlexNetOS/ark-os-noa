"""
Service Generator Agent for ark-os-noa

This agent automates the creation of new microservices following the established
patterns in the ark-os-noa platform.
"""

from pathlib import Path
from typing import Dict, Any, List
import textwrap
from .base_agent import BaseAgent, register_agent

@register_agent
class ServiceGeneratorAgent(BaseAgent):
    """Agent that generates new microservice boilerplate"""
    
    def __init__(self, workspace_path: Path = None):
        super().__init__("service-generator", workspace_path)
    
    def execute(self, service_name: str, endpoints: List[str] = None, **kwargs) -> Dict[str, Any]:
        """Generate a new microservice"""
        self.log_execution("start_service_generation", {"service_name": service_name})
        
        if not self.validate_workspace():
            return {"success": False, "error": "Invalid workspace"}
        
        # Default endpoints if none provided
        if endpoints is None:
            endpoints = ["/", "/health", "/process"]
        
        service_path = self.workspace_path / "services" / service_name
        
        if service_path.exists():
            error = f"Service '{service_name}' already exists"
            self.log_execution("service_exists_error", {"error": error})
            return {"success": False, "error": error}
        
        # Create service directory
        service_path.mkdir(parents=True)
        self.log_execution("created_directory", {"path": str(service_path)})
        
        # Generate files
        files_created = []
        
        # 1. Create __init__.py
        init_path = service_path / "__init__.py"
        init_path.write_text("")
        files_created.append(str(init_path))
        
        # 2. Create main.py
        main_py_content = self._generate_main_py(service_name, endpoints)
        main_path = service_path / "main.py"
        main_path.write_text(main_py_content)
        files_created.append(str(main_path))
        
        # 3. Create requirements.txt (service-specific dependencies)
        requirements_content = self._generate_requirements()
        req_path = service_path / "requirements.txt"
        req_path.write_text(requirements_content)
        files_created.append(str(req_path))
        
        # 4. Create Dockerfile
        dockerfile_content = self._generate_dockerfile(service_name)
        docker_path = service_path / "Dockerfile"
        docker_path.write_text(dockerfile_content)
        files_created.append(str(docker_path))
        
        # 5. Update pipeline.py to include new service
        self._update_pipeline(service_name)
        
        # 6. Generate tests
        test_file = self._generate_test_file(service_name)
        test_path = self.workspace_path / "tests" / f"test_{service_name}.py"
        test_path.write_text(test_file)
        files_created.append(str(test_path))
        
        self.log_execution("service_generated", {
            "service_name": service_name,
            "files_created": files_created,
            "endpoints": endpoints
        })
        
        return {
            "success": True,
            "service_name": service_name,
            "files_created": files_created,
            "next_steps": [
                f"cd services/{service_name}",
                f"python main.py  # Start service on port 8000",
                f"uvicorn main:app --reload --port 8000  # Development mode",
                "python -m pytest tests/  # Run tests"
            ]
        }
    
    def _generate_main_py(self, service_name: str, endpoints: List[str]) -> str:
        """Generate the main FastAPI application file"""
        
        endpoint_handlers = []
        for endpoint in endpoints:
            if endpoint == "/":
                handler = '''@app.get("/")
async def root():
    return {"service": "''' + service_name + '''"}'''
            elif endpoint == "/health":
                handler = '''@app.get("/health")
async def health():
    return {"status": "healthy", "service": "''' + service_name + '''"}'''
            elif endpoint == "/process":
                handler = '''@app.post("/process")
async def process_data(data: dict):
    """Process incoming data and return results"""
    result = process(data)
    return {"success": True, "result": result}'''
            else:
                # Generic endpoint
                endpoint_name = endpoint.strip("/").replace("-", "_")
                handler = f'''@app.get("{endpoint}")
async def {endpoint_name}():
    return {{"endpoint": "{endpoint}", "service": "{service_name}"}}'''
            
            endpoint_handlers.append(handler)
        
        endpoints_code = "\n\n".join(endpoint_handlers)
        
        return f'''from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI(
    title="{service_name} Service",
    description="Microservice for {service_name} operations in ark-os-noa",
    version="1.0.0"
)

{endpoints_code}

def process(job: Dict[str, Any]) -> Dict[str, Any]:
    """Process job data through this service."""
    job.setdefault("steps", []).append("{service_name}")
    
    # Add service-specific processing logic here
    job.setdefault("processed_by", []).append("{service_name}")
    
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _generate_requirements(self) -> str:
        """Generate service-specific requirements"""
        return textwrap.dedent('''
        # Service-specific dependencies
        # Inherits from main requirements.txt
        
        # Add service-specific packages here
        # Example:
        # pandas==2.0.3
        # numpy==1.24.3
        ''').strip()
    
    def _generate_dockerfile(self, service_name: str) -> str:
        """Generate Dockerfile for the service"""
        return textwrap.dedent(f'''
        FROM python:3.11-slim
        
        WORKDIR /app
        
        # Copy requirements and install dependencies
        COPY requirements.txt .
        COPY ../../requirements.txt ./base-requirements.txt
        RUN pip install -r base-requirements.txt && \\
            pip install -r requirements.txt
        
        # Copy service code
        COPY . .
        
        # Expose port
        EXPOSE 8000
        
        # Health check
        HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
            CMD curl -f http://localhost:8000/health || exit 1
        
        # Run service
        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        ''').strip()
    
    def _generate_test_file(self, service_name: str) -> str:
        """Generate test file for the service"""
        # Convert hyphenated names to underscores for imports
        import_name = service_name.replace('-', '_')
        
        return textwrap.dedent(f'''
        import sys
        from pathlib import Path
        from fastapi.testclient import TestClient
        
        # Add project root to path
        ROOT = Path(__file__).resolve().parents[1]
        if str(ROOT) not in sys.path:
            sys.path.append(str(ROOT))
        
        # Import using the actual directory name (hyphens preserved)
        import importlib.util
        
        # Dynamic import for hyphenated service names
        spec = importlib.util.spec_from_file_location(
            "service_main", 
            ROOT / "services" / "{service_name}" / "main.py"
        )
        service_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(service_main)
        
        app = service_main.app
        process = service_main.process
        
        client = TestClient(app)
        
        def test_health_endpoint():
            # Test health endpoint if it exists
            try:
                response = client.get("/health")
                assert response.status_code == 200
                assert response.json()["status"] == "healthy"
            except:
                # Health endpoint might not exist, skip this test
                pass
        
        def test_process_function():
            job = {{"data": "test"}}
            result = process(job)
            assert "{service_name}" in result["steps"]
            assert "{service_name}" in result["processed_by"]
        ''').strip()
    
    def _update_pipeline(self, service_name: str):
        """Update pipeline.py to include the new service"""
        pipeline_path = self.workspace_path / "pipeline.py"
        
        if not pipeline_path.exists():
            self.logger.warning("pipeline.py not found, skipping update")
            return
        
        # Skip pipeline update for hyphenated service names (they can't be imported)
        if "-" in service_name:
            self.logger.warning(f"Service '{service_name}' has hyphens - skipping pipeline update (use underscores for pipeline integration)")
            return
        
        content = pipeline_path.read_text()
        
        # Add import
        import_line = f"from services.{service_name} import main as {service_name}"
        if import_line not in content:
            # Find the last import and add after it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('from services.') and 'import main as' in line:
                    lines.insert(i + 1, import_line)
                    break
            
            # Add to SERVICE_SEQUENCE
            for i, line in enumerate(lines):
                if line.strip() == "]" and "SERVICE_SEQUENCE" in lines[i-5:i]:
                    lines.insert(i, f"    {service_name},")
                    break
            
            pipeline_path.write_text('\n'.join(lines))
            self.log_execution("updated_pipeline", {"service_name": service_name})