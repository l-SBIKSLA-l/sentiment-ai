output "container_id" {
  description = "ID du conteneur staging"
  value       = docker_container.sentiment_staging.id
}

output "app_url" {
  description = "URL de l'application staging"
  value       = "http://localhost:${var.app_port}"
}

output "network_name" {
  description = "Nom du réseau Docker créé"
  value       = docker_network.cicd.name
}

output "prometheus_url" {
  description = "URL de Prometheus"
  value       = "http://localhost:9090"
}

output "grafana_url" {
  description = "URL de Grafana"
  value       = "http://localhost:3000"
}
