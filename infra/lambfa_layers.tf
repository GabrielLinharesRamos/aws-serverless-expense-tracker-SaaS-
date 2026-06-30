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