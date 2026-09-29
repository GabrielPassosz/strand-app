# Verificação da versão 0.1.0

Executada em 26/09/2026, com Python 3.12, Django 5.2.17 e banco SQLite.

## Servidor

18 testes automatizados aprovados em `core/tests.py`:

1. Cadastro, confirmação de e-mail e login.
2. Cadastro duplicado sem conta adicional e rejeição de senha fraca.
3. Bloqueio de leitura, escrita e exportação sem autenticação.
4. Exigência de CSRF no login e nas alterações.
5. Aceitação de requisição autenticada com token CSRF válido.
6. Impedimento de forjar o proprietário na criação de clientes.
7. Isolamento entre contas na listagem, edição, atendimento e exportação.
8. Persistência em uma nova sessão, conflito de edição, arquivamento e restauração.
9. Idempotência do atendimento e validação de valor/data.
10. Foto privada, bloqueio de acesso/exclusão por outra conta e remoção do arquivo.
11. Rejeição de conteúdo falso como imagem e de vínculo com atendimento de outro cliente.
12. Recuperação de senha com token de uso único e invalidação de sessões antigas.
13. Alteração de senha preservando apenas a sessão atual.
14. Limitação de tentativas de login.
15. Persistência de preferências e rejeição de fuso inválido.
16. Logout e ausência de rota pública para os arquivos privados.
17. Rejeição de estrutura JSON e valores de ficha inválidos.
18. Conta nova sem cadastros fictícios.

Após adicionar bloqueio transacional na recuperação de senha, o teste correspondente foi executado novamente.

`manage.py check` e `manage.py check --deploy` passaram sem avisos na configuração validada. O segundo comando foi executado com parâmetros de produção de exemplo, não com uma hospedagem real. Verificação de migrações sem alterações pendentes.

## Integração da interface com servidor HTTP real

Teste automatizado com DOM JavaScript (jsdom) executando as chamadas HTTP contra Django:

- cadastro pela interface;
- leitura do e-mail local e confirmação pelo link;
- login;
- cadastro de cliente;
- escape de HTML digitado em observações;
- gravação de atendimento;
- preferência de idioma persistida após recarregar em uma nova instância da página;
- tela de configurações e logout.

Sintaxe do JavaScript verificada com `node --check`. A ferramenta de backup local também gerou um ZIP válido a partir do banco local.

## O que não foi validado

- Renderização visual em Chrome/Edge real: o navegador de teste não pôde ser instalado no ambiente. O teste com DOM não substitui inspeção visual.
- Implantação dos contêineres Docker e uso real de PostgreSQL.
- DNS, certificado HTTPS ou entrega SMTP em um provedor externo.
- Cobrança: não implementada.
- Carga elevada, alta disponibilidade, restauração operacional de produção ou auditoria independente de segurança.

Esses limites não impedem a execução local, mas precisam ser tratados antes de uma abertura comercial pública. Nenhuma afirmação de segurança absoluta é feita.


## Atualização cloud 0.2.0 — 27/09/2026

23 testes locais aprovados (18 existentes e 5 novos). Os novos verificam a configuração Vercel, bloqueiam SQLite, armazenamento local e DEBUG na Vercel, e exigem segredo na manutenção. Sintaxe JavaScript validada. Migrações sem alterações pendentes.

Configuração de build com parâmetros fictícios de produção validada sem conexão externa. A política RLS precisa ser confirmada no PostgreSQL real após aplicar as migrações. S3, PostgreSQL, SMTP, Vercel e Netlify não foram provisionados nem testados em suas contas. Não há integração Stripe nesta versão.
