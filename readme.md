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