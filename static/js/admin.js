
        // ==================== FUNCIONALIDADES ADMIN ====================
console.log("admin.js carregado!");

        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const tabName = this.getAttribute('data-tab');
                
                // Remover active de todos os botões e conteúdos
                document.querySelectorAll('.tab-btn, .tab-content').forEach(el => {
                    el.classList.remove('active');
                });
                
                // Adicionar active ao botão clicado e seu conteúdo
                this.classList.add('active');
                document.getElementById(tabName).classList.add('active');
                
                // Carregar dados se necessário
                if (tabName === 'videos' && !document.querySelector('#videosTable tbody tr')) {
                    carregarVideos();
                }
            });
        });

        // Carregar Vídeos
        function carregarVideos() {
            fetch('/admin/listar_videos')
                .then(response => response.json())
                .then(videos => {
                    const tbody = document.querySelector('#videosTable tbody');
                    tbody.innerHTML = '';
                    
                    if (videos.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">Nenhum vídeo encontrado</td></tr>';
                        return;
                    }
                    
                    videos.forEach(video => {
                        const duracao = `${Math.floor(video.duracao / 60)}m ${video.duracao % 60}s`;
                        const row = `
                            <tr>
                                <td><strong>${video.titulo}</strong></td>
                                <td><code>${video.arquivo}</code></td>
                                <td>${duracao}</td>
                                <td>${video.usuarios_assistindo}</td>
                                <td>${video.usuarios_concluidos}</td>
                            </tr>
                        `;
                        tbody.innerHTML += row;
                    });
                })
                .catch(error => {
                    console.error('Erro ao carregar vídeos:', error);
                    mostrarNotificacao('Erro ao carregar vídeos', 'error');
                });
        }

        // Cadastrar Usuário
        function cadastrarUsuario(event) {
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const senha = document.getElementById('senha').value;
            const tipo = document.getElementById('tipo').value;
            
            const dados = { username, senha, tipo };
            
            fetch('/admin/cadastrar_usuario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'sucesso') {
                    mostrarNotificacao('✓ Usuário criado com sucesso!', 'success');
                    document.getElementById('formCadastroUsuario').reset();
                    // Recarregar tabela de usuários
                    location.reload();
                } else {
                    mostrarNotificacao('✕ ' + data.mensagem, 'error');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                mostrarNotificacao('Erro ao criar usuário', 'error');
            });
        }

        // Cadastrar Vídeo
        function cadastrarVideo(event) {
            event.preventDefault();
            
            const titulo = document.getElementById('titulo').value;
            const duracao = parseInt(document.getElementById('duracao').value);
            const tipo = document.getElementById('tipoVideo').value;

            let arquivo = '';
            let url = '';

            if (tipo === 'youtube') {
                url = document.getElementById('url').value;
            } else {
                arquivo = document.getElementById('arquivo').value;
            }

            const dados = { titulo, arquivo, duracao, tipo, url };

            fetch('/admin/cadastrar_video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'sucesso') {
                    mostrarNotificacao('✓ Vídeo criado com sucesso!', 'success');
                    document.getElementById('formCadastroVideo').reset();
                    carregarVideos();
                } else {
                    mostrarNotificacao('✕ ' + data.mensagem, 'error');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                mostrarNotificacao('Erro ao criar vídeo', 'error');
            });
        }

        // Ver Progresso do Usuário
        function verProgresso(usuarioId, usuarioNome) {
            document.getElementById('usuarioNome').textContent = usuarioNome;
            document.getElementById('progressoDetalhe').innerHTML = '<div class="spinner" style="margin-left: 20px;"></div>';
            document.getElementById('modalProgresso').classList.add('active');
            
            fetch(`/progresso_usuario/${usuarioId}`)
                .then(response => response.json())
                .then(progresso => {
                    let html = '';
                    
                    if (progresso.length === 0) {
                        html = '<p style="color: #999; text-align: center; padding: 20px;">Nenhum progresso registrado</p>';
                    } else {
                        progresso.forEach(p => {
                            const statusClass = p.concluido ? 'completed' : 'pending';
                            const statusText = p.concluido ? '✓ Concluído' : 'Em andamento';
                            
                            html += `
                                <div class="progress-item">
                                    <div class="progress-item-title">${p.titulo}</div>
                                    <div class="progress-bar-small">
                                        <div class="progress-bar-small-fill" style="width: ${p.percentual}%"></div>
                                    </div>
                                    <div class="progress-item-info">
                                        ${p.percentual.toFixed(1)}% - ${Math.floor(p.tempo / 60)}m ${Math.floor(p.tempo % 60)}s / ${Math.floor(p.duracao / 60)}m ${Math.floor(p.duracao % 60)}s
                                        <span class="status-badge ${statusClass}" style="margin-left: 10px;">${statusText}</span>
                                    </div>
                                </div>
                            `;
                        });
                    }
                    
                    document.getElementById('progressoDetalhe').innerHTML = html;
                })
                .catch(error => {
                    console.error('Erro:', error);
                    document.getElementById('progressoDetalhe').innerHTML = '<p style="color: #c33;">Erro ao carregar progresso</p>';
                });
        }

        // Deletar Usuário
        function deletarUsuario(usuarioId, usuarioNome) {
            if (!confirm(`Tem certeza que deseja deletar o usuário "${usuarioNome}"? Esta ação não pode ser desfeita.`)) {
                return;
            }
            
            fetch(`/admin/deletar_usuario/${usuarioId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'sucesso') {
                    mostrarNotificacao('✓ Usuário deletado com sucesso!', 'success');
                    location.reload();
                } else {
                    mostrarNotificacao('✕ ' + data.mensagem, 'error');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                mostrarNotificacao('Erro ao deletar usuário', 'error');
            });
        }

        // Gerenciar Modais
        function fecharModal(modalName) {
            document.getElementById(modalName).classList.remove('active');
        }

        // Fechar modal ao clicar fora
        window.addEventListener('click', function(event) {
            const modal = event.target;
            if (modal.classList && modal.classList.contains('modal')) {
                modal.classList.remove('active');
            }
        });

        // Mostrar Notificação
        function mostrarNotificacao(mensagem, tipo = 'success') {
            const notificacao = document.createElement('div');
            notificacao.className = 'notification ' + tipo;
            notificacao.textContent = mensagem;
            document.body.appendChild(notificacao);

            setTimeout(() => {
                notificacao.remove();
            }, 3000);
        }

        function toggleTipoVideo() {
            const tipo = document.getElementById('tipoVideo').value;
            
            if (tipo === 'youtube') {
                document.getElementById('campoArquivo').style.display = 'none';
                document.getElementById('campoUrl').style.display = 'block';
            } else {
                document.getElementById('campoArquivo').style.display = 'block';
                document.getElementById('campoUrl').style.display = 'none';
            }
        }
