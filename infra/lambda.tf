#função create expense

# Zipa o codigo da função create expense
data "archive_file" "package_create_expense" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/create/saas-project-create-expense"
  output_path = "${path.module}/../lambda/create/saas-project-create-expense/function.zip"
}

# Função lambda create expense
resource "aws_lambda_function" "saas_project_create_expense" {
  filename         = data.archive_file.package_create_expense.output_path
  function_name    = "${var.project_name}-create-expense"
  role             = aws_iam_role.iam_lambda_create_expense.arn
  handler          = "index.lambda_handler"
  source_code_hash = data.archive_file.package_create_expense.output_base64sha256

  runtime = "python3.13"

  tags = {
    Environment = var.tag_Environment
    Project     = var.tag_Project
  }
}