#função create expense

# Zipa o codigo da função create expense
data "archive_file" "package_create_expense" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/expenses/create"
  output_path = "${path.module}/../lambda/expenses/create/function.zip"
}

data "aws_iam_policy_document" "assume_role_expenses" {
  statement {
    effect = "Allow"

    principals {
      type = "Service"

      identifiers = [
        "lambda.amazonaws.com"
      ]
    }

    actions = [
      "sts:AssumeRole"
    ]
  }
}

resource "aws_iam_role" "iam_lambda_expense" {
  name               = "${var.project_name}-expense-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_expenses.json
}

# Função lambda create expense
resource "aws_lambda_function" "saas_project_create_expense" {
  filename         = data.archive_file.package_create_expense.output_path
  function_name    = "${var.project_name}-create-expense"
  role             = aws_iam_role.iam_lambda_expense.arn
  handler          = "index.lambda_handler"
  source_code_hash = data.archive_file.package_create_expense.output_base64sha256

  runtime = "python3.13"
  
  environment {
    variables = {
      EXPENSES_TABLE = aws_dynamodb_table.saas_project_expenses.name
    }
  }

  tags = {
    Environment = var.tag_Environment
    Project     = var.tag_Project
  }
}

resource "aws_lambda_permission" "api_gateway_create_expense" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"

  function_name = aws_lambda_function.saas_project_create_expense.function_name

  principal = "apigateway.amazonaws.com"
}

data "aws_iam_policy_document" "expense_permissions_policy_json" {
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem"
    ]

    resources = [
      aws_dynamodb_table.saas_project_expenses.arn,
    ]
  }


  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "expense_permissions_policy" {
  name   = "${var.project_name}-expense-policy"
  policy = data.aws_iam_policy_document.expense_permissions_policy_json.json
}

resource "aws_iam_role_policy_attachment" "lambda_expense_attachment" {
  role       = aws_iam_role.iam_lambda_expense.name
  policy_arn = aws_iam_policy.expense_permissions_policy.arn
}