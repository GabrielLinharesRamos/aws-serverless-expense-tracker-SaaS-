# SaaS

Plataforma SaaS de finanças pessoais sem servidor, construída na AWS, que permite aos usuários gerenciar despesas, receitas e categorias financeiras em um ambiente multilocatário seguro. Desenvolvida com Terraform e GitHub Actions, utiliza o Amazon Cognito para autenticação, o DynamoDB para persistência e o CloudWatch para observabilidade, seguindo as melhores práticas nativas da nuvem.

## CI/CD

O projeto utiliza GitHub Actions com autenticação federada via OIDC para realizar deploy automatizado da infraestrutura na AWS.

### Utilizando o pipeline em um fork

Para utilizar o pipeline CI/CD em um fork do projeto, será necessário:

- Atualizar a variável `github_repo` no arquivo `variables.tf` para refletir o novo repositório.
- Executar pelo menos um `terraform apply` localmente para criar o OIDC Provider, IAM Role e demais recursos necessários para o pipeline.
- Configurar o Secret `AWS_ROLE_ARN` no GitHub Actions com o ARN da role criada para o OIDC.
- Configurar a Variable `AWS_REGION` no GitHub Actions com a região AWS utilizada pelo projeto.
- Atualizar a configuração do backend S3 caso deseje utilizar um bucket diferente para o `terraform.tfstate`.

Após essa configuração, os deploys poderão ser executados automaticamente através do GitHub Actions.

# DEVLOG

---

O projeto será desenvolvido de forma incremental:

- Fase 0 → CI/CD
- Fase 1 → Fundação Serverless com Terraform
- Fase 2 → Autenticação e Multi-Tenancy
- Fase 3 → Evolução do Domínio Financeiro
- Fase 4 → Segurança e Maturidade de Produção
- Fase 5 → Observabilidade
- Fase 6 → Refinamento e Nível Portfólio

# Fase 0 - CI/CD

---

### Dia 1:

Durante o desenvolvimento de hoje, foi realizada a configuração inicial do pipeline de CI/CD do projeto, permitindo que a infraestrutura seja provisionada automaticamente através do GitHub Actions.

Para acelerar a construção da base do projeto, foram reaproveitados componentes já utilizados no projeto Event-Driven, incluindo a integração entre GitHub Actions e AWS utilizando autenticação federada via OIDC (OpenID Connect), eliminando a necessidade de armazenar credenciais permanentes da AWS no repositório.

Além da reutilização da infraestrutura existente, também foram criados e configurados os recursos necessários no GitHub para suportar o pipeline de deploy automatizado, incluindo variáveis e secrets utilizados durante a autenticação e execução dos workflows.

Com isso, o projeto passa a contar com deploy automatizado desde as primeiras fases de desenvolvimento, permitindo que futuras alterações de infraestrutura sejam aplicadas diretamente através do fluxo de CI/CD.

# Fase 1 - Fundação Serverless com Terraform

---

### Dia 2:

Durante o desenvolvimento de hoje, foi iniciada a construção da fundação serverless da aplicação, com a criação dos primeiros recursos de infraestrutura necessários para suportar o domínio financeiro do sistema.

Foram provisionados, utilizando Terraform, o API Gateway responsável pela exposição dos endpoints da aplicação e a tabela DynamoDB destinada ao armazenamento das despesas. A modelagem inicial do banco foi construída utilizando Partition Key (PK) e Sort Key (SK), seguindo uma estratégia compatível com Single Table Design e preparada para a futura evolução do sistema para um ambiente multi-tenant.

Também foi desenvolvida a primeira função Lambda responsável pelo cadastro de despesas, incluindo validações iniciais da requisição, geração de identificadores únicos, persistência dos dados no DynamoDB e implementação de logs estruturados para facilitar futuras atividades de monitoramento e troubleshooting.

Além das funcionalidades, foi definida e implementada a estrutura organizacional do projeto, separando responsabilidades entre camadas de entrada (handlers), regras de negócio (services), acesso a dados (repositories) e componentes compartilhados. Essa organização foi planejada desde o início para suportar o crescimento da aplicação e facilitar a manutenção conforme novas funcionalidades forem adicionadas.

Com essas entregas, o projeto passa a possuir sua primeira operação de negócio implementada e estabelece a base arquitetural que será utilizada nas próximas etapas de desenvolvimento.

### Dia 3:

Durante o desenvolvimento de hoje, foi concluída a primeira versão funcional da camada de aplicação responsável pelo gerenciamento de despesas.

Foram implementados os endpoints de criação, listagem, atualização e exclusão de despesas, consolidando o CRUD principal da aplicação. Cada operação foi estruturada seguindo uma separação de responsabilidades entre handlers, services, repositories e utilitários compartilhados, preparando a base do projeto para futuras evoluções sem comprometer a organização do código.

Além disso, foram implementados logs estruturados em formato JSON para operações críticas, facilitando futuras atividades de monitoramento e troubleshooting através do CloudWatch.

Com essa entrega, a aplicação passa a possuir uma base funcional completa para gerenciamento de despesas, restando a integração final dos recursos da AWS para validação ponta a ponta da arquitetura serverless.

### Dia 4:

- Identifiquei e corrigi um problema que causava **Internal Server Error** nos endpoints. Durante os testes, percebi que módulos compartilhados (helpers, validators e repositories) não estavam sendo encontrados pelas funções Lambda.
- Para resolver esse problema e melhorar a reutilização de código, implementei um **AWS Lambda Layer**, centralizando componentes compartilhados utilizados por múltiplas funções do sistema.
- Refatorei a arquitetura da aplicação, migrando de uma abordagem com **uma Lambda por operação** para **uma Lambda por domínio**. Agora, as operações de CRUD são tratadas internamente pela mesma função através do método HTTP recebido pelo API Gateway.
- Essa mudança reduziu a quantidade de recursos provisionados na AWS, simplificou o gerenciamento da infraestrutura e tornou a estrutura do projeto mais organizada e escalável para futuras funcionalidades.
- Também concluí a configuração e validação das rotas HTTP do API Gateway para os endpoints de despesas, garantindo a integração correta com a nova arquitetura baseada em domínio.

# Fase 2 - Autenticação e Multi-Tenancy

---

### Dia 5:

Iniciei a implementação da camada de autenticação da aplicação utilizando Amazon Cognito.

Durante esta etapa, realizei o provisionamento da infraestrutura necessária por meio da criação do User Pool e do App Client responsáveis pelo gerenciamento e autenticação dos usuários.

Além disso, executei testes para validar o fluxo completo de cadastro, confirmação de conta por e-mail e autenticação, garantindo que o processo de criação e gerenciamento de usuários estivesse funcionando corretamente.

Também implementei um JWT Authorizer no API Gateway integrado ao Cognito, permitindo que os tokens emitidos durante o login sejam validados automaticamente antes que as requisições alcancem as funções Lambda.

Por fim, todas as rotas do domínio de despesas (Expenses) foram configuradas para exigir autenticação via JWT, garantindo que apenas usuários autenticados possam acessar os endpoints da API.

### Dia 6:

Finalizei a fase 2 do projeto, implementando o isolamento de dados entre usuários. Ajustei as funções principais do sistema — criação, listagem, atualização e exclusão de despesas — para que cada operação considere o identificador do usuário obtido a partir do token JWT. Com isso, cada usuário passa a acessar apenas os próprios dados, sem possibilidade de interferência nos registros de outros usuários. Essa mudança consolidou a base de autenticação e autorização do sistema, garantindo o isolamento no nível de usuário e fortalecendo a segurança da aplicação.

# Fase 3 - Evolução do Domínio Financeiro

---

### Dia 7:

Refleti sobre os requisitos do projeto e decidi evoluir o sistema para suportar uma nova funcionalidade de tenancy. O sistema deixa de ser uma aplicação de gestão financeira pessoal e passa a ser uma plataforma de gestão financeira familiar, na qual cada família possui acesso isolado aos seus próprios dados, sem possibilidade de visualização por outras famílias.

Nesse novo modelo, os dados de cada família são compostos pelo conjunto de informações fornecidas pelos seus integrantes, onde cada usuário possui seu próprio login e senha. Dentro da mesma família, os usuários podem visualizar os dados dos demais membros, mas não podem criar ou modificar informações diretamente em nome de outro usuário.

A maior parte do tempo foi dedicada à análise das mudanças necessárias na arquitetura e à forma como essa nova modelagem será implementada. Esse estudo é fundamental para garantir uma evolução consistente do sistema e evitar retrabalho em etapas futuras, especialmente na modelagem de dados e definição do modelo de tenancy.

### Dia 8:

Implementei um novo domínio responsável pela autenticação do sistema, contendo duas novas rotas principais: **signup** e **login**, responsáveis pela criação de usuários e autenticação via Cognito utilizando o modelo `USER_PASSWORD_AUTH`  sem suporte ao `REFRESH_TOKEN`. Essa decisão foi intencional para manter o sistema **stateless e simplificado na primeira versão**, reduzindo complexidade no gerenciamento de sessões e validação de tokens. Alguns bugs relacionados a autenticação e ao roteamento também foram consertados

Além disso, devido à evolução do escopo do projeto para um modelo de **multi-tenancy baseado em famílias**, foi necessário revisar a modelagem do banco de dados no DynamoDB. A estrutura passou a utilizar `family_id` como chave primária (PK), garantindo o isolamento dos dados por tenant, enquanto o identificador da despesa (`expense_id`) passou a ser utilizado como chave de ordenação (SK).

Também foi introduzido um **GSI (Global Secondary Index)** para suportar consultas baseadas em usuário, permitindo que cada integrante visualize tanto seus próprios gastos quanto os gastos agregados da sua família. Essa abordagem garante flexibilidade na forma de consulta sem comprometer o isolamento entre famílias.

algumas outras mudanças foram:

- `family_id` passou a ser carregado a partir dos **claims do JWT do Cognito**
- Criação de atributo customizado `custom:family_id`
- Ajuste nas rotas e serviços para refletir o novo modelo:
    - `/expenses` → dados da família
    - `/expenses/my` (planejado) → visão individual do usuário