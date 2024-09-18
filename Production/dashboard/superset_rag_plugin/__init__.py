from superset.views.base import BaseSupersetView
from superset.extensions import appbuilder
from .plugin import RAGChatbotView, ChatbotViz

appbuilder.add_view_no_menu(RAGChatbotView)

def register_plugin(app):
    app.config['VIZ_TYPE_PLUGINS'] = ['ChatbotViz']