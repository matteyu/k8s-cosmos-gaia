output "role_arn" {
  value = aws_iam_role.iam_role.arn
}

output "policy_arn" {
  value = aws_iam_policy.iam_policy.arn
}

output "group_name" {
  value = aws_iam_group.iam_group.name
}

output "user_names" {
  value = aws_iam_user.iam_user[*].name
}
