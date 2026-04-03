
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
                
                if (tabName === 'relatorios-kpi' && !document.querySelector('#kpiTable tbody tr')) {
                    carregarRelatoriosKPI();
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
            
            const nome_completo = document.getElementById('nome_completo').value;
            const cpf = document.getElementById('cpf').value;
            const tipo = document.getElementById('tipo').value;
            
            const dados = { nome_completo, cpf, tipo };
            
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

        // ================= ABA VINCULAR ACESSOS =================
        
        let todosOsVideosGlobal = [];
        
        function carregarVideosUsuario(usuarioId) {
            if (!usuarioId) {
                document.getElementById('listaVideosAcesso').style.display = 'none';
                return;
            }
            
            document.getElementById('usuarioAcessoId').value = usuarioId;
            document.getElementById('listaVideosAcesso').style.display = 'block';
            
            // Buscar todos os vídeos se ainda não carregados
            let promessaVideos = Promise.resolve(todosOsVideosGlobal);
            if (todosOsVideosGlobal.length === 0) {
                promessaVideos = fetch('/admin/listar_videos')
                    .then(r => r.json())
                    .then(videos => {
                        todosOsVideosGlobal = videos;
                        return videos;
                    });
            }
            
            // Buscar acessos atuais do usuário
            Promise.all([
                promessaVideos,
                fetch(`/admin/listar_acessos_usuario/${usuarioId}`).then(r => r.json())
            ]).then(([videos, acessosData]) => {
                const acessos = acessosData.acessos || [];
                const container = document.getElementById('videosCheckboxes');
                container.innerHTML = '';
                
                if (videos.length === 0) {
                    container.innerHTML = '<p>Nenhum vídeo cadastrado no sistema ainda.</p>';
                    return;
                }
                
                videos.forEach(video => {
                    const idCb = `cb_video_${video.id}`;
                    const checado = acessos.includes(video.id) ? 'checked' : '';
                    container.innerHTML += `
                        <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
                            <input type="checkbox" name="video_acessos" value="${video.id}" ${checado}>
                            <span>${video.titulo} <small style="color:#777">(${Math.floor(video.duracao/60)}m ${video.duracao%60}s)</small></span>
                        </label>
                    `;
                });
            }).catch(e => {
                mostrarNotificacao('Erro ao carregar permissões', 'error');
                console.error(e);
            });
        }
        
        function salvarAcessos(event) {
            event.preventDefault();
            const usuario_id = document.getElementById('usuarioAcessoId').value;
            const checkboxes = document.querySelectorAll('input[name="video_acessos"]:checked');
            const video_ids = Array.from(checkboxes).map(cb => parseInt(cb.value));
            
            fetch('/admin/salvar_acessos_usuario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario_id, video_ids })
            })
            .then(r => r.json())
            .then(data => {
                if(data.status === 'sucesso') {
                    mostrarNotificacao('Perrmissões salvas com sucesso!', 'success');
                } else {
                    mostrarNotificacao(data.mensagem, 'error');
                }
            })
            .catch(e => mostrarNotificacao('Erro ao salvar permissões', 'error'));
        }

        // ================= ABA RELATÓRIOS KPI =================
        function carregarRelatoriosKPI() {
            fetch('/admin/relatorios_kpi')
                .then(r => r.json())
                .then(dados => {
                    const tbody = document.querySelector('#kpiTable tbody');
                    tbody.innerHTML = '';
                    
                    if (dados.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 20px;">Nenhum dado auditável encontrado.</td></tr>';
                        return;
                    }
                    
                    dados.forEach(d => {
                        const statusClass = (d.concluido === 'Sim') ? 'completed' : 'pending';
                        
                        const tempoA = `${Math.floor(d.tempo_assistido / 60)}m ${Math.floor(d.tempo_assistido % 60)}s`;
                        const durV = `${Math.floor(d.video_duracao / 60)}m ${d.video_duracao % 60}s`;
                        
                        tbody.innerHTML += `
                            <tr>
                                <td><strong>${d.nome_completo}</strong></td>
                                <td>${d.cpf}</td>
                                <td>${d.video_titulo}</td>
                                <td>${durV}</td>
                                <td>${tempoA}</td>
                                <td>
                                    <div style="display:flex; align-items:center; gap:10px;">
                                        <div style="flex-grow:1; display:flex; gap:10px; align-items:center;">
                                           <div class="progress-bar-small" style="width:100px;">
                                               <div class="progress-bar-small-fill" style="width: ${d.percentual}%"></div>
                                           </div>
                                           <span>${d.percentual}%</span>
                                        </div>
                                    </div>
                                </td>
                                <td><span class="status-badge ${statusClass}">${d.concluido}</span></td>
                            </tr>
                        `;
                    });
                })
                .catch(e => {
                    mostrarNotificacao('Erro ao carregar KPI', 'error');
                    console.error(e);
                });
        }
