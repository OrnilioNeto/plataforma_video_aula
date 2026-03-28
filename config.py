# Configuração do Sistema de Treinamento com Vídeo

# ==================== BANCO DE DADOS ====================
DATABASE_PATH = 'database.db'

# ==================== FLASK ====================
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
SECRET_KEY = 'sua-chave-secreta-muito-segura-2024'

# Tempo de sessão em horas
SESSION_LIFETIME_HOURS = 24

# ==================== SEGURANÇA ====================
# Máximo de segundos que pode ser pulado no vídeo
MAX_SEEK_FORWARD = 30

# Percentual mínimo para marcar como concluído
COMPLETION_PERCENTAGE = 0.9  # 90%

# Intervalo de envio de progresso (segundos)
PROGRESS_SAVE_INTERVAL = 5

# ==================== VALIDAÇÃO ====================
# Comprimento mínimo de senha
MIN_PASSWORD_LENGTH = 6

# Comprimento mínimo de nome de usuário
MIN_USERNAME_LENGTH = 3

# Comprimento máximo de nome de usuário
MAX_USERNAME_LENGTH = 30

# ==================== UPLOAD ====================
# Pasta para armazenar vídeos
VIDEOS_FOLDER = 'static/videos'

# Extensões de vídeo permitidas (deixar vazio para permitir todas)
ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'webm', 'ogv', 'mov']

# ==================== INTERFACE ====================
# Itens por página em tabelas
ITEMS_PER_PAGE = 20

# ==================== EMAIL (FUTURO) ====================
# Para envio de notificações
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

# ==================== LOG ====================
LOG_FILE = 'logs/app.log'
LOG_LEVEL = 'INFO'
