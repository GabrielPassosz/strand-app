> Este arquivo descreve a alternativa Docker em servidor próprio. Para Vercel, Supabase e Netlify, use `GUIA_PUBLICACAO.md`.

# Implantação online

A configuração incluída destina-se a **um servidor Linux**, com Docker Compose, domínio apontando diretamente para ele e portas 80/443 liberadas. Não é uma publicação já concluída. Não suporta execução de Django dentro do link estático do protótipo.

## Preparação

1. Copie o projeto para o servidor.
2. Aponte o DNS de um domínio/subdomínio para o servidor.
3. Configure um remetente e credenciais SMTP em seu provedor.
4. Copie `production.env.example` para `production.env`.
5. Preencha os campos. Gere uma chave secreta e uma senha do banco distintas:

```bash
python3 -c "import secrets; print(secrets.token_hex(48))"
```

Execute duas vezes e use uma saída em cada campo. Use a senha hexadecimal no banco para evitar caracteres que exigem escape na URL. `DOMAIN` deve ser somente o hostname, sem `https://` nem caminho. O arquivo de produção é privado: não o envie para Git ou atendimento de terceiros.

```bash
chmod 600 production.env
docker compose --env-file production.env up -d --build
```

O proxy obtém o certificado HTTPS para o domínio configurado. O aplicativo executa as migrações antes de iniciar o Gunicorn. Banco e arquivos ficam em volumes persistentes. Somente o proxy publica portas; PostgreSQL e Django não devem ficar diretamente acessíveis na internet.

## Verificação obrigatória no servidor escolhido

```bash
docker compose --env-file production.env exec app python manage.py check --deploy
docker compose --env-file production.env logs --tail 100 app proxy
```

No navegador, crie duas contas e verifique entrega de e-mails, confirmação, login, recuperação, upload, isolamento entre contas e permanência dos dados após reiniciar os contêineres. Esses testes devem ser repetidos com o domínio e serviços reais.

A configuração de produção falha ao iniciar se faltar chave forte, URL HTTPS, banco externo ou configuração SMTP básica. Ela não garante que as credenciais SMTP fornecidas sejam válidas.

## Proxy e limites de acesso

`TRUST_PROXY=True` só deve ser usado na topologia fornecida, em que o aplicativo não tem porta pública e o Caddy substitui o cabeçalho `X-Real-IP`. O aplicativo usa esse endereço para limitar tentativas. Ao colocar outra CDN ou proxy à frente, revise a confiança e o encaminhamento do IP de origem. Não aceite cabeçalhos de cliente como prova de IP.

Não habilite `DEBUG` em produção. Não publique pastas de mídia, backups, `.env` ou e-mails. Não utilize `runserver` como servidor público. Mantenha os volumes e o host protegidos. HSTS inclui subdomínios: use um hostname dedicado e ajuste essa política se sua implantação exigir outra abrangência.

## Backups

Não existe agendamento de backup configurado automaticamente. Configure execução periódica e armazenamento externo protegido, com política de retenção e teste de restauração.

Para criar um backup consistente com interrupção temporária das gravações:

```bash
mkdir -p backups
docker compose --env-file production.env stop app
docker compose --env-file production.env exec -T db pg_dump -U strand -d strand -Fc > backups/strand.dump
docker compose --env-file production.env cp app:/app/data/private-media backups/private-media
docker compose --env-file production.env start app
```

A pasta de mídia só existe após o primeiro upload; ausência antes disso não significa perda. Utilize pastas novas/datadas em cada execução, confira os códigos de saída e não substitua o último backup válido por um arquivo vazio. Copie os arquivos para outro local protegido. Preserve `production.env` em um cofre de segredos separado. O procedimento acima não criptografa os arquivos.

Restaure primeiro em ambiente isolado usando `pg_restore` e a cópia de mídia. A restauração de produção pode sobrescrever registros e deve ter um procedimento próprio validado antes da operação.

## Operação

Agende diariamente:

```bash
docker compose --env-file production.env exec -T app python manage.py maintenance
```

Atualize dependências e imagens periodicamente, verificando notas de segurança e testando antes. Não use `docker compose down -v` para reiniciar: essa opção remove os volumes de dados.

A configuração atual usa um banco compartilhado com autorização por proprietário e disco privado compartilhado no servidor único. Para escalar a vários servidores, será necessário armazenamento privado compartilhado, procedimentos coordenados de migração, monitoramento e testes de carga. Não foi implementada infraestrutura de alta disponibilidade.

## Cobrança

A aplicação está em acesso inicial, sem cobrança automática. Para vender assinaturas com cobrança integrada, ainda é necessário definir plano/preço/moeda, conectar a conta comercial do provedor de pagamentos, implementar checkout e portal, processar webhooks com verificação e idempotência e aplicar as regras de acesso. Nenhum pagamento é simulado como concluído.

## Referências técnicas

- Django: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- Autenticação: https://docs.djangoproject.com/en/5.2/topics/auth/default/
- Limite de corpo no proxy: https://caddyserver.com/docs/caddyfile/directives/request_body
- Proxy reverso: https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
