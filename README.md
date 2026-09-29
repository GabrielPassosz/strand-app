> Vercel / Supabase / Netlify: consulte `GUIA_PUBLICACAO.md` para a configuração cloud desta versão. Cobrança automática continua pendente.

# Strand — aplicação funcional, versão 0.2.0

Sistema web para cabeleireiros independentes com cadastro de clientes, fichas capilares e histórico. Interface em inglês e português do Brasil. Esta versão substitui os dados temporários do protótipo por servidor e banco de dados reais.

## O que funciona

- Cadastro de profissionais, confirmação do e-mail, login, logout, recuperação e alteração de senha.
- Senhas com hash pelo sistema de autenticação do Django; sessões armazenadas no banco.
- Cada profissional acessa somente seus próprios clientes, atendimentos, fotos e exportações.
- Cadastro, edição, arquivamento e restauração de clientes.
- Ficha capilar, preferências, fórmulas, serviços, valores e histórico permanente de atendimentos.
- Upload de fotos privadas, vinculadas opcionalmente a um atendimento, e exclusão de fotos.
- Idioma, moeda e fuso horário salvos por conta.
- Exportação dos registros em JSON. As imagens não são embutidas nesse JSON; os links exigem login.
- Proteção CSRF, limites de tentativas por conta e endereço de origem, validação de entradas e registro de ações no banco.
- Controle de versão na edição do cliente para detectar conflito entre sessões.
- Identificador de requisição nos atendimentos para impedir duplicação ao reenviar a mesma gravação.

Não existem contas, clientes nem senhas de demonstração no pacote.

## Iniciar no Windows

Recomendado: Python 3.12 ou 3.13. A versão testada foi Python 3.12.

1. Extraia todo o ZIP em uma pasta, por exemplo `C:\Projetos\Strand`.
2. Execute `start_windows.bat`.
3. Aguarde a instalação das dependências e a criação do banco.
4. Abra http://127.0.0.1:8000.
5. Clique em **Create account** ou troque para português e clique em **Criar conta**.
6. No modo local, abra o arquivo mais recente de `data\emails`. Copie o link de confirmação e abra no navegador.
7. Faça login com o e-mail e a senha cadastrados.

O arquivo `.env` é criado uma única vez com uma chave aleatória. O inicializador não apaga bancos nem substitui uma configuração existente. Mantenha o terminal aberto enquanto utiliza o sistema; Ctrl+C encerra o servidor. Os dados permanecem após fechar o programa.

### Execução manual

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe setup_local.py
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Em Linux/macOS, crie o ambiente com `python3 -m venv .venv` e use `.venv/bin/python` nos comandos restantes.

**O programa deve ser aberto pelo servidor.** Abrir `templates/index.html` com dois cliques não inicia a aplicação.

## E-mail: local e real

No modo local, o conteúdo dos e-mails é salvo em arquivos de `data/emails`, para permitir testar confirmação e recuperação sem contratar um provedor. Não é enviado à caixa de entrada.

Para entrega real, configure o backend SMTP, host, porta, usuário, senha e remetente verificado. Nunca publique o backend de e-mails em arquivo nem uma pasta `data` acessível na web. Links de confirmação expiram em 24 horas e links de recuperação em uma hora. Os links usados deixam de funcionar.

Se um e-mail de confirmação falhar, use **Reenviar confirmação de e-mail** depois de corrigir o serviço. Cadastro existente e recuperação utilizam respostas genéricas para reduzir exposição de contas.

## Onde os dados ficam

- `data/db.sqlite3`: banco local.
- `data/private-media/`: imagens privadas.
- `data/emails/`: e-mails de desenvolvimento.
- `.env`: configuração e chave secreta; não compartilhar.

No servidor online, a configuração fornecida usa PostgreSQL e volumes persistentes. Nenhuma rota pública expõe a pasta de imagens: o aplicativo verifica a conta antes de entregar cada foto.

## Publicar online

Consulte `DEPLOYMENT.md`. Foram incluídos Dockerfile, Docker Compose, PostgreSQL e configuração de proxy HTTPS.

**Esta entrega não publica a aplicação funcional nem altera o endereço do protótipo.** São necessários um servidor/domínio sob seu controle e um serviço de e-mail. A implantação externa e a entrega SMTP real ainda precisam ser executadas e validadas no ambiente escolhido.

## Assinaturas e limites de escopo

Esta versão permite uso real das fichas e contas. A tela de assinatura informa **acesso inicial sem cobrança automática**. Não há processador de pagamentos, plano cobrado, checkout, webhooks ou bloqueio por inadimplência. Essa integração exige definir provedor, moeda/preço da assinatura e configurar a conta comercial.

Ainda não inclui agenda, gestão de salões/equipes, importação em massa, MFA, aplicativo móvel nativo, termos contratuais ou consentimento eletrônico. Arquivar preserva os registros; não equivale a excluir definitivamente dados de uma pessoa. Não foi implementado fluxo de exclusão completa de conta/cliente.

As anotações não são traduzidas automaticamente. A moeda escolhida é o padrão dos novos atendimentos e não converte valores antigos. O fuso horário define a data inicial do atendimento, que é armazenado por dia, sem horário de agenda. Fotos são reprocessadas em JPEG, com remoção dos metadados e redução para até 2400 pixels no maior lado; não são arquivos originais de qualidade integral.

## Backup local

Encerre o servidor antes do backup para manter banco e arquivos coerentes:

```powershell
.venv\Scripts\python.exe manage.py backup_local --output backups\strand-2026-09-26.zip
```

Use um nome novo em cada backup. Guarde uma cópia fora do computador, em local protegido. O pacote contém dados privados e não é criptografado por esta ferramenta.

Restauração: com o servidor parado e após guardar o estado atual, extraia `db.sqlite3` e `private-media/` do seu backup para `data/`. Execute `manage.py migrate` e inicie o servidor. Preserve a configuração `.env` separadamente. Teste a restauração antes de depender do processo.

## Testes e manutenção

```powershell
.venv\Scripts\python.exe manage.py test core
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py maintenance
```

A suíte cria seu próprio banco temporário e não utiliza os registros normais. Consulte `VALIDATION.md` para o que foi e não foi verificado. Execute `maintenance` diariamente em produção para remover sessões e contadores expirados.

## Estrutura do código

- `strand/settings.py`: configuração, banco, e-mail e controles de implantação.
- `strand/urls.py`: rotas.
- `core/models.py`: usuários, clientes, atendimentos, fotos, auditoria e limites de tentativas.
- `core/forms.py`: validação dos dados.
- `core/views.py`: APIs e verificações de acesso.
- `core/tests.py`: testes de comportamento e segurança.
- `core/migrations/`: criação e evolução do banco.
- `static/app.js`: telas, traduções e chamadas ao servidor.
- `static/style.css`: aparência responsiva.
- `templates/index.html`: entrada da aplicação.
- `start_windows.bat`: instalação e início local.

As dependências diretas estão fixadas em `requirements.txt`, salvo o pacote de fusos horários. Revise atualizações de segurança regularmente.
