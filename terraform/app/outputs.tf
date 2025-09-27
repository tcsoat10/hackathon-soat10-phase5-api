output "main_api_lb_endpoint" {
  description = "Endpoint do Load Balancer da API principal"
  value       = "${kubernetes_service.main_api_lb.status[0].load_balancer[0].ingress[0].hostname}/api/v1"
}