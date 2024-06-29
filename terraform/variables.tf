variable "name_suffixes" {
  description = "Suffixes to append to resource names"
  type        = list(string)
  default     = ["role","policy","group","membership"]
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "group_users" {
  description = "AWS users to add to the group"
  type        = list(string)
}
