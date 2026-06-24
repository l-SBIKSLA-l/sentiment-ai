variable "image_name" {
  description = "Nom de l'image Docker"
  type        = string
  default     = "sentiment-ai"
}

variable "image_tag" {
  description = "Tag de l'image Docker à déployer"
  type        = string
  default     = "latest"
}

variable "app_port" {
  description = "Port exposé en staging"
  type        = number
  default     = 8001
}

variable "container_name" {
  description = "Nom du conteneur staging"
  type        = string
  default     = "sentiment-staging"
}

variable "registry" {
  description = "Registry Docker (ex: ghcr.io/monpseudo)"
  type        = string
  default     = "ghcr.io/VOTRE_PSEUDO"
}
