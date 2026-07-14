variable "project_name" {
  description = "prefixo de todos os recursos lançados no projeto para identificação"
  type        = string
  default     = "saas-project"
}

variable "region" {
  description = "nome da região do projeto"
  type        = string
  default     = "sa-east-1"
}

variable "github_allowed_repo_and_branch" {
  description = "O repositório GitHub que tem permissão para assumir a função OIDC."
  type        = string

  # caso queira testar em um fork altere aqui 
  default = "repo:GabrielLinharesRamos/aws-serverless-expense-tracker-SaaS-:ref:refs/heads/main"
}

#api_gateway

variable "stage" {
  description = "nome do stage da api gateway"
  type        = string
  default     = "dev"
}

variable "expenses_table" {
  description = "nome da tabela do dynamoDB"
  type        = string
  default     = "saas-project-table"
}

#tags

variable "tag_Environment" {
  description = "tag de Environment"
  type        = string
  default     = "dev"
}

variable "tag_Project" {
  description = "tag de Project"
  type        = string
  default     = "saas-project"
}