#!/usr/bin/env python3
"""
Script đối chiếu lý thuyết với thực tế backend/database
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set

class ProjectAnalyzer:
    """
    Phân tích dự án và đối chiếu với yêu cầu lý thuyết.
    
    Class này quét cấu trúc dự án, phát hiện các components (Backend, Frontend, 
    Database, Testing, Documentation, DevOps) và đánh giá tính đầy đủ so với 
    yêu cầu lý thuyết.
    
    Workflow:
    1. Khởi tạo ProjectAnalyzer với project_root
    2. Gọi generate_report() để tạo báo cáo đầy đủ
    3. Sử dụng print_report() để hiển thị kết quả
    
    Example:
        analyzer = ProjectAnalyzer(Path('/path/to/project'))
        report = analyzer.generate_report()
        print_report(report)
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def scan_project_structure(self) -> Dict[str, bool]:
        """
        Quét cấu trúc dự án và kiểm tra các thành phần cơ bản
        
        Returns:
            Dictionary với status của các components
        """
        structure_checks = {}
        
        # Backend patterns
        backend_indicators = [
            'server.js', 'app.js', 'index.js',  # Node.js
            'main.py', 'app.py', 'wsgi.py',  # Python
            'Program.cs', 'Startup.cs',  # .NET
            'main.go',  # Go
            'application.properties', 'application.yml'  # Spring Boot
        ]
        
        # Frontend patterns
        frontend_indicators = [
            'package.json', 'index.html',
            'src/App.js', 'src/App.tsx',
            'angular.json', 'vue.config.js'
        ]
        
        # Database patterns
        database_indicators = [
            'migrations/', 'schema.sql', 'models/',
            'database/', 'db/', 'alembic/'
        ]
        
        # Testing patterns
        testing_indicators = [
            'tests/', 'test/', '__tests__/',
            'spec/', 'pytest.ini', 'jest.config.js'
        ]
        
        # Documentation patterns
        doc_indicators = [
            'README.md', 'docs/', 'CONTRIBUTING.md',
            'API.md', 'swagger.yml', 'openapi.yml'
        ]
        
        # DevOps patterns
        devops_indicators = [
            '.github/workflows/', '.gitlab-ci.yml',
            'Dockerfile', 'docker-compose.yml',
            'kubernetes/', 'k8s/'
        ]
        
        # Check each category
        structure_checks['has_backend'] = self._check_patterns(backend_indicators)
        structure_checks['has_frontend'] = self._check_patterns(frontend_indicators)
        structure_checks['has_database'] = self._check_patterns(database_indicators)
        structure_checks['has_tests'] = self._check_patterns(testing_indicators)
        structure_checks['has_docs'] = self._check_patterns(doc_indicators)
        structure_checks['has_devops'] = self._check_patterns(devops_indicators)
        
        return structure_checks
    
    def _check_patterns(self, patterns: List[str]) -> bool:
        """
        Kiểm tra xem có pattern nào tồn tại không
        
        Args:
            patterns: List các patterns cần kiểm tra
            
        Returns:
            True nếu tìm thấy ít nhất 1 pattern
        """
        for pattern in patterns:
            path = self.project_root / pattern
            if path.exists():
                return True
        return False
    
    def count_files_by_extension(self, extensions: Set[str]) -> int:
        """
        Đếm số file theo extension
        
        Args:
            extensions: Set các extensions (.js, .py, etc.)
            
        Returns:
            Số lượng files
        """
        count = 0
        for ext in extensions:
            count += len(list(self.project_root.rglob(f'*{ext}')))
        return count
    
    def analyze_backend(self) -> Dict:
        """Phân tích backend implementation"""
        backend_files = self.count_files_by_extension({
            '.js', '.ts', '.py', '.java', '.cs', '.go', '.php'
        })
        
        # Check for common backend features
        has_api = self._check_patterns([
            'routes/', 'controllers/', 'api/',
            'endpoints/', 'handlers/'
        ])
        
        has_auth = self._check_patterns([
            'auth/', 'authentication/', 'middleware/auth'
        ])
        
        has_models = self._check_patterns([
            'models/', 'entities/', 'domain/'
        ])
        
        return {
            'backend_files': backend_files,
            'has_api_structure': has_api,
            'has_authentication': has_auth,
            'has_data_models': has_models
        }
    
    def analyze_database(self) -> Dict:
        """Phân tích database implementation"""
        has_migrations = self._check_patterns([
            'migrations/', 'migrate/', 'alembic/'
        ])
        
        has_schema = self._check_patterns([
            'schema.sql', 'schema.prisma', 'models.py'
        ])
        
        has_seeds = self._check_patterns([
            'seeds/', 'fixtures/', 'seed.sql'
        ])
        
        return {
            'has_migrations': has_migrations,
            'has_schema': has_schema,
            'has_seed_data': has_seeds
        }
    
    def analyze_testing(self) -> Dict:
        """Phân tích test coverage và infrastructure"""
        test_files = self.count_files_by_extension({
            '.test.js', '.spec.js', '.test.ts', '.spec.ts',
            '.test.py', '_test.go'
        })
        
        has_test_config = self._check_patterns([
            'jest.config.js', 'pytest.ini', 'karma.conf.js',
            '.coveragerc', 'coverage/'
        ])
        
        return {
            'test_files': test_files,
            'has_test_config': has_test_config
        }
    
    def analyze_documentation(self) -> Dict:
        """Phân tích documentation"""
        doc_files = self.count_files_by_extension({'.md'})
        
        has_readme = (self.project_root / 'README.md').exists()
        has_api_docs = self._check_patterns([
            'swagger.yml', 'openapi.yml', 'API.md', 'docs/api'
        ])
        
        return {
            'documentation_files': doc_files,
            'has_readme': has_readme,
            'has_api_docs': has_api_docs
        }
    
    def analyze_devops(self) -> Dict:
        """Phân tích DevOps setup"""
        has_ci = self._check_patterns([
            '.github/workflows/', '.gitlab-ci.yml',
            '.travis.yml', 'azure-pipelines.yml'
        ])
        
        has_docker = self._check_patterns([
            'Dockerfile', 'docker-compose.yml'
        ])
        
        has_env_config = self._check_patterns([
            '.env.example', 'config/', 'environment.yml'
        ])
        
        return {
            'has_ci_cd': has_ci,
            'has_containerization': has_docker,
            'has_env_config': has_env_config
        }
    
    def generate_report(self) -> Dict:
        """
        Tạo báo cáo tổng hợp
        
        Returns:
            Dictionary chứa báo cáo đầy đủ
        """
        structure = self.scan_project_structure()
        backend = self.analyze_backend()
        database = self.analyze_database()
        testing = self.analyze_testing()
        documentation = self.analyze_documentation()
        devops = self.analyze_devops()
        
        # Calculate completion score
        # Only count boolean checks for pass/fail, not file counts
        total_checks = 0
        passed_checks = 0
        
        for category in [structure, backend, database, testing, documentation, devops]:
            for key, value in category.items():
                # Only count boolean checks as completion criteria
                if isinstance(value, bool):
                    total_checks += 1
                    if value:
                        passed_checks += 1
        
        completion_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        return {
            'structure': structure,
            'backend': backend,
            'database': database,
            'testing': testing,
            'documentation': documentation,
            'devops': devops,
            'summary': {
                'total_checks': total_checks,
                'passed_checks': passed_checks,
                'completion_rate': completion_rate
            }
        }

def print_report(report: Dict):
    """In báo cáo ra console"""
    print("\n" + "=" * 70)
    print("BÁO CÁO ĐỐI CHIẾU LÝ THUYẾT VỚI THỰC TẾ")
    print("=" * 70 + "\n")
    
    # Structure
    print("📁 CẤU TRÚC DỰ ÁN:")
    structure = report['structure']
    print(f"  Backend: {'✅' if structure['has_backend'] else '❌'}")
    print(f"  Frontend: {'✅' if structure['has_frontend'] else '❌'}")
    print(f"  Database: {'✅' if structure['has_database'] else '❌'}")
    print(f"  Tests: {'✅' if structure['has_tests'] else '❌'}")
    print(f"  Documentation: {'✅' if structure['has_docs'] else '❌'}")
    print(f"  DevOps: {'✅' if structure['has_devops'] else '❌'}")
    
    # Backend
    print("\n🔧 BACKEND:")
    backend = report['backend']
    print(f"  Số file backend: {backend['backend_files']}")
    print(f"  API structure: {'✅' if backend['has_api_structure'] else '❌'}")
    print(f"  Authentication: {'✅' if backend['has_authentication'] else '❌'}")
    print(f"  Data models: {'✅' if backend['has_data_models'] else '❌'}")
    
    # Database
    print("\n💾 DATABASE:")
    database = report['database']
    print(f"  Migrations: {'✅' if database['has_migrations'] else '❌'}")
    print(f"  Schema: {'✅' if database['has_schema'] else '❌'}")
    print(f"  Seed data: {'✅' if database['has_seed_data'] else '❌'}")
    
    # Testing
    print("\n🧪 TESTING:")
    testing = report['testing']
    print(f"  Số file test: {testing['test_files']}")
    print(f"  Test configuration: {'✅' if testing['has_test_config'] else '❌'}")
    
    # Documentation
    print("\n📚 DOCUMENTATION:")
    documentation = report['documentation']
    print(f"  Số file docs: {documentation['documentation_files']}")
    print(f"  README: {'✅' if documentation['has_readme'] else '❌'}")
    print(f"  API docs: {'✅' if documentation['has_api_docs'] else '❌'}")
    
    # DevOps
    print("\n🚀 DEVOPS:")
    devops = report['devops']
    print(f"  CI/CD: {'✅' if devops['has_ci_cd'] else '❌'}")
    print(f"  Docker: {'✅' if devops['has_containerization'] else '❌'}")
    print(f"  Environment config: {'✅' if devops['has_env_config'] else '❌'}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TỔNG KẾT:")
    summary = report['summary']
    print(f"  Tổng số kiểm tra: {summary['total_checks']}")
    print(f"  Số kiểm tra đạt: {summary['passed_checks']}")
    print(f"  Tỷ lệ đạt yêu cầu: {summary['completion_rate']:.2f}%")
    print("=" * 70 + "\n")

def main():
    """Main function"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print(f"Đang phân tích dự án tại: {project_root}")
    
    analyzer = ProjectAnalyzer(project_root)
    report = analyzer.generate_report()
    
    print_report(report)
    
    # Save report to file
    report_file = project_root / 'docs' / 'reports' / 'cross_reference_report.json'
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Báo cáo đã được lưu tại: {report_file}")

if __name__ == '__main__':
    main()
