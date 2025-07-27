#!/usr/bin/env python3
"""
Python Test Application - Verify all installed tools
"""

import subprocess
import sys


def test_python_packages():
    """Test all installed Python packages"""
    print("🐍 Testing Python Packages...")
    print("=" * 50)
    
    packages_to_test = [
        ("torch", "import torch; print(f'PyTorch: {torch.__version__}')"),
        ("tensorflow", "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"),
        ("fastapi", "import fastapi; print(f'FastAPI: {fastapi.__version__}')"),
        ("openai", "import openai; print(f'OpenAI: {openai.__version__}')"),
        ("anthropic", "import anthropic; print(f'Anthropic: {anthropic.__version__}')"),
        ("transformers", "import transformers; print(f'Transformers: {transformers.__version__}')"),
        ("pandas", "import pandas as pd; print(f'Pandas: {pd.__version__}')"),
        ("numpy", "import numpy as np; print(f'NumPy: {np.__version__}')"),
        ("scikit-learn", "import sklearn; print(f'Scikit-learn: {sklearn.__version__}')"),
        ("streamlit", "import streamlit; print(f'Streamlit: {streamlit.__version__}')"),
        ("gradio", "import gradio; print(f'Gradio: {gradio.__version__}')"),
        ("plotly", "import plotly; print(f'Plotly: {plotly.__version__}')"),
        ("sqlalchemy", "import sqlalchemy; print(f'SQLAlchemy: {sqlalchemy.__version__}')"),
        ("redis", "import redis; print('Redis: Available')"),
        ("celery", "import celery; print(f'Celery: {celery.__version__}')"),
        ("pydantic", "import pydantic; print(f'Pydantic: {pydantic.__version__}')"),
        ("cryptography", "import cryptography; print(f'Cryptography: {cryptography.__version__}')"),
        ("pytest", "import pytest; print(f'Pytest: {pytest.__version__}')"),
        ("black", "import black; print(f'Black: {black.__version__}')"),
        ("flake8", "import flake8; print('Flake8: Available')"),
        ("mypy", "import mypy; print('MyPy: Available')"),
        ("sphinx", "import sphinx; print(f'Sphinx: {sphinx.__version__}')"),
        ("mkdocs", "import mkdocs; print(f'MkDocs: {mkdocs.__version__}')"),
        ("pinecone-client", "import pinecone; print('Pinecone: Available')"),
        ("weaviate-client", "import weaviate; print('Weaviate: Available')"),
        ("qdrant-client", "import qdrant_client; print('Qdrant: Available')"),
        ("milvus", "import pymilvus; print('Milvus: Available')"),
        ("faiss-cpu", "import faiss; print('FAISS: Available')"),
        ("fhirclient", "import fhirclient; print('FHIR Client: Available')"),
        ("hl7", "import hl7; print('HL7: Available')"),
        ("pydicom", "import pydicom; print('DICOM: Available')"),
        ("kubernetes", "import kubernetes; print('Kubernetes: Available')"),
        ("helm", "import helm; print('Helm: Available')"),
        ("ansible", "import ansible; print('Ansible: Available')"),
        ("grafana", "import grafana_api; print('Grafana: Available')"),
        ("elasticsearch", "import elasticsearch; print('Elasticsearch: Available')"),
        ("kibana", "import kibana; print('Kibana: Available')"),
        ("logstash", "import logstash; print('Logstash: Available')"),
        ("keycloak", "import keycloak; print('Keycloak: Available')"),
        ("langchain", "import langchain; print('LangChain: Available')"),
        ("autogpt", "import autogpt; print('AutoGPT: Available')"),
        ("langgraph", "import langgraph; print('LangGraph: Available')"),
        ("haystack", "import haystack; print('Haystack: Available')"),
        ("rasa", "import rasa; print('Rasa: Available')"),
        ("lightgbm", "import lightgbm; print('LightGBM: Available')"),
        ("xgboost", "import xgboost; print('XGBoost: Available')"),
        ("catboost", "import catboost; print('CatBoost: Available')"),
        ("google-cloud-storage", "import google.cloud.storage; print('Google Cloud Storage: Available')"),
        ("azure-storage-blob", "import azure.storage.blob; print('Azure Storage: Available')"),
        ("boto3", "import boto3; print('AWS Boto3: Available')"),
        ("matplotlib", "import matplotlib; print(f'Matplotlib: {matplotlib.__version__}')"),
        ("seaborn", "import seaborn; print(f'Seaborn: {seaborn.__version__}')"),
        ("opencv-python", "import cv2; print(f'OpenCV: {cv2.__version__}')"),
        ("pillow", "import PIL; print(f'Pillow: {PIL.__version__}')"),
        ("altair", "import altair; print(f'Altair: {altair.__version__}')"),
        ("wordcloud", "import wordcloud; print('WordCloud: Available')"),
        ("nltk", "import nltk; print('NLTK: Available')"),
        ("spacy", "import spacy; print('SpaCy: Available')"),
        ("textblob", "import textblob; print('TextBlob: Available')"),
        ("gensim", "import gensim; print(f'Gensim: {gensim.__version__}')"),
        ("psycopg2-binary", "import psycopg2; print('PostgreSQL: Available')"),
        ("loguru", "import loguru; print('Loguru: Available')")
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for package_name, test_code in packages_to_test:
        try:
            result = subprocess.run([sys.executable, "-c", test_code], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {package_name}: {result.stdout.strip()}")
                successful_tests += 1
            else:
                print(f"❌ {package_name}: Failed")
                failed_tests += 1
        except Exception as e:
            print(f"❌ {package_name}: Error - {str(e)}")
            failed_tests += 1
    
    print(f"\n📊 Python Test Results:")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {round((successful_tests / (successful_tests + failed_tests)) * 100, 1)}%")
    
    return successful_tests, failed_tests

def test_ai_functionality():
    """Test AI functionality"""
    print("\n🤖 Testing AI Functionality...")
    print("=" * 50)
    
    try:
        # Test PyTorch
        import torch
        x = torch.randn(3, 3)
        print(f"✅ PyTorch tensor created: {x.shape}")
        
        # Test TensorFlow
        import tensorflow as tf
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        print("✅ TensorFlow model created successfully")
        
        # Test OpenAI
        import openai
        print("✅ OpenAI package imported successfully")
        
        # Test Pandas
        import pandas as pd
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        print(f"✅ Pandas DataFrame created: {df.shape}")
        
        # Test NumPy
        import numpy as np
        arr = np.array([1, 2, 3, 4, 5])
        print(f"✅ NumPy array created: {arr.shape}")
        
        print("🎉 All AI functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ AI functionality test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 EHB AI Development System - Python Tools Test")
    print("=" * 60)
    
    # Test Python packages
    python_success, python_failed = test_python_packages()
    
    # Test AI functionality
    ai_success = test_ai_functionality()
    
    print("\n" + "=" * 60)
    print("🎯 FINAL PYTHON TEST RESULTS:")
    print(f"✅ Python Packages Working: {python_success}")
    print(f"❌ Python Packages Failed: {python_failed}")
    print(f"🤖 AI Functionality: {'✅ Working' if ai_success else '❌ Failed'}")
    
    if python_success >= 40 and ai_success:
        print("🎉 EXCELLENT! Python tools are ready for production!")
    elif python_success >= 30:
        print("👍 GOOD! Most Python tools are working!")
    else:
        print("⚠️  NEEDS ATTENTION! Many Python tools failed!")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 