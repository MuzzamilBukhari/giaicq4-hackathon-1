from setuptools import setup, find_packages

setup(
    name="rag_backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "python-dotenv",
        "google-generativeai",
        "qdrant-client",
        "sqlalchemy",
        "asyncpg",
        "pydantic",
    ],
)