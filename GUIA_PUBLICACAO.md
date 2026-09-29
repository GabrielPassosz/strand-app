# Publicação do Strand: Vercel, Supabase, Netlify e Stripe

Atualizado em 27/09/2026. Use o pacote `strand-cloud-v0.2.0.zip`, e não o ZIP do protótipo nem a versão 0.1.0.

## 1. Escolha a combinação

| Serviço | Função |
|---|---|
| Vercel | Executar o site e o servidor Django. Caminho recomendado para este código. |
| Supabase | PostgreSQL permanente e armazenamento privado das fotos. |
| Serviço SMTP, por exemplo Resend | Enviar confirmação de e-mail e recuperação de senha. |
| Netlify, opcional | Endereço público que encaminha ao Django em outro provedor, como Render. |
| Stripe | Preparação da conta comercial; a integração de assinaturas ainda não está implementada neste pacote. |

Vercel e Netlify são alternativas. Você não precisa contratar as duas. O Supabase não substitui a hospedagem Django, e os usuários deste projeto são gerenciados pelo Django, não pelo Supabase Auth.

Estado desta entrega: código adaptado e 23 testes locais aprovados. Nenhum projeto real foi criado ou publicado em suas contas, nenhum banco externo foi provisionado e nenhuma entrega SMTP externa foi confirmada. Os testes de conexão indicados abaixo devem ser executados com seus serviços reais. Cobrança automática permanece pendente.

## 2. Criar o projeto no Supabase

1. Acesse https://supabase.com/dashboard e entre na sua conta.
2. Crie um **New project**, em uma organização sua.
3. Nome sugerido: `strand-production`.
4. Defina uma senha forte do banco e guarde-a em um gerenciador de senhas.
5. Escolha a região pensando no público principal e na proximidade do servidor da aplicação.
6. Aguarde a criação do projeto.
7. Abra **Connect** e copie a string do **Transaction pooler**. Use a string completa retornada pelo painel; não deduza o hostname pela região. Essa será a `DATABASE_URL` na Vercel.
8. Copie também a string do **Session pooler**, útil para executar as migrações pelo seu computador. Os usuários e as portas diferem entre tipos de conexão; não troque somente um pedaço da URL.
9. Substitua o marcador da senha pela senha do banco. Caracteres especiais na senha precisam ser codificados para URL.

A aplicação já desabilita prepared statements e cursores de servidor no PostgreSQL e usa conexões curtas na Vercel. A configuração cloud exige SSL.

Não crie as tabelas manualmente pelo editor: as migrações do Django farão isso.

### Fotos privadas

1. Abra **Storage** e crie um bucket chamado `strand-private`.
2. Mantenha **Public bucket desativado**.
3. Nas configurações S3 do Storage, gere as credenciais de acesso.
4. Guarde exatamente os valores exibidos: endpoint, região, Access Key ID e Secret Access Key.
5. Eles serão usados em `S3_ENDPOINT_URL`, `S3_REGION`, `S3_ACCESS_KEY_ID` e `S3_SECRET_ACCESS_KEY`.

Não confunda credenciais S3 com a chave pública `anon`/publishable do Supabase. As credenciais S3 são secretas e ficam somente no servidor. Não crie políticas de leitura pública para fotos nem coloque essas chaves no JavaScript.

## 3. Configurar envio de e-mails

Exemplo com Resend, que pode ser substituído por outro serviço SMTP:

1. Crie sua conta em https://resend.com.
2. Cadastre um domínio de sua propriedade na área **Domains**.
3. Adicione no DNS os registros fornecidos pelo painel e aguarde a verificação.
4. Crie uma API key para envio e guarde-a de forma privada.
5. Use:

| Variável | Valor com Resend |
|---|---|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | `smtp.resend.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_HOST_USER` | `resend` |
| `EMAIL_HOST_PASSWORD` | Sua API key do Resend |
| `EMAIL_USE_TLS` | `True` |
| `DEFAULT_FROM_EMAIL` | `Strand <noreply@seu-dominio.com>` |

O domínio do remetente precisa estar verificado. O endereço gratuito `vercel.app` não é um domínio seu para verificar no serviço de e-mail. Se você ainda não tem domínio próprio, use um serviço que autorize um remetente seu conforme as regras dele.

## 4. Preparar o código e o banco

1. Extraia o ZIP e abra a pasta `strand-app` no VS Code.
2. No terminal PowerShell dessa pasta, execute:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Copie `cloud.env.example` para `.env.cloud`.
4. Preencha as variáveis conforme a tabela abaixo. Para esses comandos administrativos, use a URL do **Session pooler** em `DATABASE_URL`.
5. Gere dois segredos diferentes executando duas vezes:

```powershell
py -c "import secrets; print(secrets.token_urlsafe(64))"
```

Use um resultado em `SECRET_KEY` e o outro em `CRON_SECRET`. Preserve `SECRET_KEY` entre publicações.

| Variável | Preenchimento |
|---|---|
| `DEBUG` | `False` |
| `SECRET_KEY` | Segredo aleatório de pelo menos 50 caracteres |
| `PUBLIC_ORIGIN` | URL HTTPS pública real da aplicação, sem barra final |
| `ALLOWED_HOSTS` | Hostname dessa URL, sem `https://` |
| `CSRF_TRUSTED_ORIGINS` | A URL HTTPS pública real |
| `DATABASE_URL` | String completa do Supabase com a senha preenchida |
| `DATABASE_SSL_REQUIRED` | `True` |
| `STORAGE_BACKEND` | `s3` |
| `S3_ENDPOINT_URL` | Endpoint copiado das configurações S3 |
| `S3_REGION` | Região copiada do Supabase |
| `S3_ACCESS_KEY_ID` | Credencial S3 |
| `S3_SECRET_ACCESS_KEY` | Segredo S3 |
| `S3_BUCKET_NAME` | `strand-private` |
| Variáveis `EMAIL_*` e `DEFAULT_FROM_EMAIL` | Dados do serviço SMTP |
| `CRON_SECRET` | Segundo segredo aleatório |

Se ainda não reservou o endereço na hospedagem, finalize os campos de URL depois de criar/importar o projeto. Não teste links de confirmação enquanto `PUBLIC_ORIGIN` contiver um exemplo.

6. Selecione a configuração cloud e crie as tabelas:

```powershell
$env:STRAND_ENV_FILE = ".env.cloud"
.venv\Scripts\python.exe manage.py migrate --noinput
.venv\Scripts\python.exe manage.py protect_database
.venv\Scripts\python.exe manage.py check --deploy --fail-level WARNING
```

Esses comandos alteram o banco apontado pela `.env.cloud`. Use um projeto dedicado à aplicação e confirme a URL antes de executar. Na primeira instalação ele estará vazio. Em atualizações com dados, faça backup primeiro.

A proteção ativa RLS nas tabelas Django e remove privilégios dos papéis públicos, `anon` e `authenticated`. O servidor deve conectar como o proprietário das tabelas, usando a mesma identidade do banco que aplicou as migrações. Não adicione políticas públicas para tentar contornar um erro de conexão.

7. Teste os serviços:

```powershell
.venv\Scripts\python.exe manage.py verify_services --storage --email seu-email@exemplo.com
```

Esse comando verifica o banco, grava/lê/remove um pequeno arquivo de teste e envia um e-mail para o endereço informado. Verifique a caixa de entrada. Sucesso no teste S3 não confirma a privacidade: confira que o bucket continua marcado como privado no painel.

8. Ao terminar os comandos administrativos, remova a seleção cloud do terminal:

```powershell
Remove-Item Env:STRAND_ENV_FILE
```

Não use `start_windows.bat` para testar credenciais de produção: ele é o inicializador local.

## 5. Colocar o código no GitHub

1. Crie um repositório privado, por exemplo `strand-platform`.
2. Envie os arquivos do pacote com `manage.py` na raiz do repositório, ou anote a subpasta para configurar como Root Directory na hospedagem.
3. Não envie `.env`, `.env.cloud`, `production.env`, banco local, fotos, backups nem a pasta `.venv`.
4. A `.gitignore` já exclui esses caminhos para quem usa Git. Se usar envio manual pelo navegador, confira a seleção antes de enviar.
5. Confirme que `requirements.txt`, `vercel.json`, `pyproject.toml`, `core`, `strand`, `templates` e `static` estão no repositório.

## 6. Publicar na Vercel

1. Acesse https://vercel.com e conecte a conta GitHub.
2. Use **Add New / Project** e importe o repositório.
3. Escolha um nome de projeto e configure a Root Directory na pasta que contém `manage.py`.
4. Use a detecção de **Django**. O pacote informa `strand.wsgi:application` e o comando de verificação de build em `pyproject.toml`.
5. Não configure uma exportação de HTML nem diretório de saída estático manual. A Vercel coleta os arquivos estáticos do Django automaticamente.
6. Em **Environment Variables**, cadastre os valores do `cloud.env.example` para Production. Na Vercel, use a URL do **Transaction pooler**, e não a URL administrativa do Session pooler.
7. Não crie a variável `VERCEL` manualmente; a plataforma a fornece. Não ative `DEBUG` para resolver erros.
8. Confira o endereço atribuído ao projeto em Domains. Ajuste `PUBLIC_ORIGIN`, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` para esse endereço exato. Se a primeira publicação tiver sido iniciada antes disso, corrija e execute **Redeploy**.
9. Depois das migrações e da configuração, publique com **Deploy**.
10. Abra a URL, crie uma conta, receba a confirmação e faça login.
11. Cadastre um cliente, um atendimento e uma foto. Saia, entre novamente e confira os dados.
12. Crie uma segunda conta e confirme que ela não vê os registros da primeira.
13. Teste a recuperação de senha e a interface nos dois idiomas.

O projeto inclui uma limpeza diária em `/api/maintenance/`, protegida por `CRON_SECRET`. Confira a execução no painel de Cron Jobs. Isso limpa sessões e contadores expirados; **não é backup**.

Não conecte publicações Preview ao banco de produção. Use projeto/banco/bucket e variáveis separados para homologação. Se ainda não tiver esses recursos, publique só o ambiente de produção escolhido e evite gerar previews com os segredos de produção.

Se a implantação não encontrar tabelas, volte ao passo das migrações. Elas não são executadas automaticamente durante cada build, para evitar que builds simultâneos alterem o banco.

## 7. Alternativa: Netlify com Django no Render

Netlify não executa diretamente este projeto Django como suas funções nativas. O caminho abaixo usa a Netlify como proxy para um servidor Django no Render; portanto, precisa dos dois serviços. Para reduzir componentes, prefira o caminho Vercel acima.

### Servidor Django no Render

1. Acesse https://render.com e crie um **Web Service** conectado ao mesmo repositório.
2. Selecione runtime Python e a pasta que contém `manage.py`.
3. Configure o build:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

4. Configure o início:

```bash
gunicorn strand.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60
```

5. Cadastre no Render as mesmas variáveis de banco, Storage e e-mail. Para esse servidor permanente, pode usar o **Session pooler**.
6. Acrescente `TRUST_PROXY=True` para reconhecer HTTPS atrás do proxy. Deixe `TRUST_CLIENT_IP_HEADER=False`, salvo se configurar um proxy que comprovadamente substitua esse cabeçalho. Sem um IP confiável individual, os limites por origem podem ser compartilhados; valide isso antes de escalar.
7. Inicialmente use o endereço real do Render em `PUBLIC_ORIGIN`, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.
8. Aplique as migrações conforme o passo 4, usando o mesmo banco, e publique.
9. Confirme login, dados e fotos pelo endereço do Render antes de acrescentar a Netlify.

### Endereço público na Netlify

1. Abra `netlify-proxy/_redirects` no pacote.
2. Substitua o endereço de exemplo pela URL real do Render. O arquivo deve ficar assim, usando seu hostname:

```text
/* https://SEU-BACKEND.onrender.com/:splat 200!
```

3. Acesse https://app.netlify.com, escolha adicionar um site com publicação manual e envie **somente a pasta `netlify-proxy`**.
4. Não envie o código Python, `.env.cloud`, senhas ou banco nessa publicação manual.
5. Copie o endereço `https://...netlify.app` realmente atribuído.
6. Volte às variáveis do **Render**, ajuste `PUBLIC_ORIGIN` para a URL Netlify e adicione esse endereço a `CSRF_TRUSTED_ORIGINS`. Em `ALLOWED_HOSTS`, permita os hostnames Render e Netlify, separados por vírgula, sem protocolos.
7. Reinicie/republique o serviço Render para aplicar as variáveis.
8. Acesse pela Netlify e repita login, logout, upload e recuperação de senha. Os e-mails devem apontar para a URL Netlify.

As requisições passam pela Netlify até o Render, inclusive `/api/` e `/static/`, mantendo chamadas da interface na mesma origem. O backend envia `Cache-Control: no-store` para páginas, dados e fotos privadas. Não adicione regras de cache público nessas rotas.

O proxy da Netlify tem timeout de 26 segundos. O backend precisa responder dentro desse prazo; partidas lentas de serviços que dormem podem provocar erro. Esta topologia não foi validada em contas reais nesta entrega.

No Render, configure a rotina de manutenção no agendador escolhido usando `python manage.py maintenance`. O `vercel.json` não agenda tarefas no Render ou na Netlify.

## 8. Stripe: o que pode ser preparado agora

A cobrança **não está implementada no pacote**. Não cadastre um webhook apontando para `/api/stripe/webhook/` ou outro caminho inventado: a rota não existe.

Você pode preparar a conta:

1. Crie sua conta em https://stripe.com e conclua as verificações exigidas pelo serviço.
2. Comece no ambiente de teste/sandbox.
3. Crie o produto `Strand Professional`.
4. Defina os preços recorrentes que você pretende vender, por exemplo um em BRL e outro em USD, com valores escolhidos por você.
5. Guarde os IDs dos preços e configure as opções desejadas do portal do cliente.

Para ativar assinaturas dentro do Strand ainda faltam: endpoint de Checkout, associação entre usuário e cliente Stripe, portal, webhook com assinatura verificada, atualização de status e regras de acesso, além dos testes de pagamento, renovação, falha e cancelamento. Não basta colocar uma chave Stripe nas variáveis. Nenhuma variável Stripe é consumida por esta versão.

## 9. Antes de abrir para clientes

Confirme no ambiente realmente publicado: duas contas isoladas; e-mails recebidos; senha antiga recusada após recuperação; arquivos privados; persistência após nova publicação; domínio/HTTPS; backup do PostgreSQL e cópia das fotos; restauração testada. Backups de banco não devem ser presumidos como cópia dos objetos do Storage: estabeleça a cópia e restauração de ambos.

Os planos, limites e recursos pagos são definidos por cada provedor. Confira os termos de uso comercial e recursos de backup do plano escolhido. Esta documentação não afirma gratuidade nem segurança absoluta.

## Documentação de referência

- Vercel Django: https://vercel.com/docs/frameworks/full-stack/django
- Limites Vercel: https://vercel.com/docs/functions/limitations
- Supabase PostgreSQL: https://supabase.com/docs/guides/database/connecting-to-postgres
- Supabase S3: https://supabase.com/docs/guides/storage/s3/authentication
- Buckets: https://supabase.com/docs/guides/storage/buckets/creating-buckets
- SMTP Resend: https://resend.com/docs/send-with-smtp
- Django no Render: https://render.com/docs/deploy-django
- Proxy Netlify: https://docs.netlify.com/manage/routing/redirects/rewrites-proxies/
- Stripe webhooks: https://docs.stripe.com/webhooks
