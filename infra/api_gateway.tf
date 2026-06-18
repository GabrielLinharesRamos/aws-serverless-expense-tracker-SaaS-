# lançando o api gateway
resource "aws_apigatewayv2_api" "saas_project_api_gateway" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"

  tags = {
    Environment = var.tag_Environment
    Project     = var.tag_Project
  }
}

# integração do API Gateway com o Lambda
resource "aws_apigatewayv2_integration" "saas_project_api_integration" {
  api_id           = aws_apigatewayv2_api.saas_project_api_gateway.id
  integration_type = "AWS_PROXY"

  payload_format_version = "2.0"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.saas_project_create_expense.invoke_arn
}

# definindo as rotas do api gateway
resource "aws_apigatewayv2_route" "saas_project_api_routes_post_expense" {
  api_id    = aws_apigatewayv2_api.saas_project_api_gateway.id
  route_key = "POST /expenses"

  authorization_type = "JWT"

  authorizer_id = aws_apigatewayv2_authorizer.cognito_jwt_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.saas_project_api_integration.id}"
}

resource "aws_apigatewayv2_route" "saas_project_api_routes_get_expense" {
  api_id    = aws_apigatewayv2_api.saas_project_api_gateway.id
  route_key = "GET /expenses"

  authorization_type = "JWT"

  authorizer_id = aws_apigatewayv2_authorizer.cognito_jwt_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.saas_project_api_integration.id}"
}

resource "aws_apigatewayv2_route" "saas_project_api_routes_delete_expense" {
  api_id    = aws_apigatewayv2_api.saas_project_api_gateway.id
  route_key = "DELETE /expenses/{expense_id}"

  authorization_type = "JWT"

  authorizer_id = aws_apigatewayv2_authorizer.cognito_jwt_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.saas_project_api_integration.id}"
}

resource "aws_apigatewayv2_route" "saas_project_api_routes_put_expense" {
  api_id    = aws_apigatewayv2_api.saas_project_api_gateway.id
  route_key = "PUT /expenses/{expense_id}"

  authorization_type = "JWT"

  authorizer_id = aws_apigatewayv2_authorizer.cognito_jwt_authorizer.id

  target = "integrations/${aws_apigatewayv2_integration.saas_project_api_integration.id}"
}

# Criação do stage
resource "aws_apigatewayv2_stage" "saas_project_api_stage" {
  api_id      = aws_apigatewayv2_api.saas_project_api_gateway.id
  name        = var.stage
  auto_deploy = true
}