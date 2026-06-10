resource "aws_dynamodb_table" "saas_project_expenses" {
    name         = var.expenses_table
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "PK"
    range_key = "SK"

    tags = {
    Environment = var.tag_Environment
    Project     = var.tag_Project
    }

    attribute {
    name = "PK"
    type = "S"
    }

    attribute {
    name = "SK"
    type = "S"
    }
}