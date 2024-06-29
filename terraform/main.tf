resource "aws_iam_role" "iam_role" {
  name               = "prod-ci-${var.name_suffixes[0]}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.account_id}:root"
        }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "iam_policy" {
  name        = "prod-ci-${var.name_suffixes[1]}"
  description = "Policy allowing users/entities to assume prod-ci-${var.name_suffixes[0]}"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = "sts:AssumeRole"
        Resource  = aws_iam_role.iam_role.arn
      }
    ]
  })
}

resource "aws_iam_group" "iam_group" {
  name = "prod-ci-${var.name_suffixes[2]}"
}

resource "aws_iam_group_policy_attachment" "group_policy_attachment" {
  group      = aws_iam_group.iam_group.name
  policy_arn = aws_iam_policy.iam_policy.arn
}

resource "aws_iam_user" "iam_user" {
  count = length(var.group_users)
  name  = var.group_users[count.index]
}

resource "aws_iam_group_membership" "group_membership" {
  name = "prod-ci-${var.name_suffixes[2]}-${var.name_suffixes[3]}"
  users = aws_iam_user.iam_user[*].name
  group = aws_iam_group.iam_group.name
}
