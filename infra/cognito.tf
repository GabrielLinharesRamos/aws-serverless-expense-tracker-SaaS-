resource "aws_cognito_user_pool" "saas_project_user_pool" {
  name = "${var.project_name}-users"

  username_attributes = ["email"]

  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length = 8
  }
  schema {
    attribute_data_type = "String"
    name                = "family_id"
    required            = false
    mutable             = true

    string_attribute_constraints {
      min_length = 1
      max_length = 64
    }
  }
}

resource "aws_cognito_user_pool_client" "cognito_client" {
  name = "${var.project_name}-client"

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]

  user_pool_id = aws_cognito_user_pool.saas_project_user_pool.id
}

resource "aws_apigatewayv2_authorizer" "cognito_jwt_authorizer" {
  api_id           = aws_apigatewayv2_api.saas_project_api_gateway.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name             = "${var.project_name}-jwt-authorizer"
  jwt_configuration {
    issuer   = "https://cognito-idp.${var.region}.amazonaws.com/${aws_cognito_user_pool.saas_project_user_pool.id}"
    audience = [aws_cognito_user_pool_client.cognito_client.id]
  }

}