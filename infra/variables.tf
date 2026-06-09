variable "project_name" {
  description = "prefixo de todos os recursos lançados no projeto para identificação"
  type        = string
  default     = "SaaS-project"
}

variable "github_allowed_repo_and_branch" {
  description = "O repositório GitHub que tem permissão para assumir a função OIDC."
  type        = string

  # caso queira testar em um fork altere aqui 
  default = "repo:GabrielLinharesRamos/aws-serverless-expense-tracker-SaaS-:ref:refs/heads/main"
}