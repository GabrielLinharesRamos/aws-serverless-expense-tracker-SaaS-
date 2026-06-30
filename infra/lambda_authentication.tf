
# Zipa o codigo da função auth
data "archive_file" "package_auth" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/auth"
  output_path = "${path.module}/../lambda/auth/function.zip"
}

data "aws_iam_policy_document" "assume_role_auth" {
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

resource "aws_iam_role" "iam_lambda_auth" {
  name               = "${var.project_name}-auth-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_auth.json
}

# Função lambda auth
resource "aws_lambda_function" "saas_project_auth" {
  filename         = data.archive_file.package_auth.output_path
  function_name    = "${var.project_name}-auth"
  role             = aws_iam_role.iam_lambda_auth.arn
  handler          = "index.lambda_handler"
  source_code_hash = data.archive_file.package_auth.output_base64sha256

  runtime = "python3.13"

  layers = [
    aws_lambda_layer_version.shared_layer.arn
  ]

  environment {
    variables = {
      COGNITO_CLIENT_ID = aws_cognito_user_pool_client.cognito_client.id
    }
  }
  
}

resource "aws_lambda_permission" "api_gateway_auth" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"

  function_name = aws_lambda_function.saas_project_auth.function_name

  principal = "apigateway.amazonaws.com"
}

data "aws_iam_policy_document" "auth_permissions_policy_json" {
  statement {
    effect = "Allow"

    actions = [
      "cognito-idp:AdminCreateUser",
      "cognito-idp:AdminUpdateUserAttributes",
      "cognito-idp:AdminInitiateAuth"
    ]

    resources = [
      aws_cognito_user_pool.saas_project_user_pool.arn
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

resource "aws_iam_policy" "auth_permissions_policy" {
  name   = "${var.project_name}-auth-policy"
  policy = data.aws_iam_policy_document.auth_permissions_policy_json.json
}

resource "aws_iam_role_policy_attachment" "lambda_auth_attachment" {
  role       = aws_iam_role.iam_lambda_auth.name
  policy_arn = aws_iam_policy.auth_permissions_policy.arn
}

# layer da função

data "archive_file" "shared_layer_zip" {
  type = "zip"

  source_dir  = "${path.module}/../lambda/layers"
  output_path = "${path.module}/../lambda/layers/shared-layer.zip"
}

resource "aws_lambda_layer_version" "shared_layer" {
  filename   = data.archive_file.shared_layer_zip.output_path
  layer_name = "${var.project_name}-shared-layer"

  source_code_hash = data.archive_file.shared_layer_zip.output_base64sha256

  compatible_runtimes = [
    "python3.13"
  ]
}