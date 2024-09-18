from setuptools import setup, find_packages

setup(
    name='superset_rag_chatbot',
    version='0.1',
    description='RAG Chatbot plugin for Apache Superset',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'apache-superset',
        'requests',
    ],
    entry_points={
        'superset.viz_type': [
            'chatbot=superset_rag_chatbot.plugin:ChatbotViz',
        ],
    },
)