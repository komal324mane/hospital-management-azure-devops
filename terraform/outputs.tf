output "resource_group_name" {
  description = "Name of the resource group created by this project."
  value       = azurerm_resource_group.hospital.name
}

output "web_app_name" {
  description = "Globally unique Azure Web App name."
  value       = azurerm_linux_web_app.hospital.name
}

output "web_app_default_hostname" {
  description = "Default hostname of the Web App."
  value       = azurerm_linux_web_app.hospital.default_hostname
}

output "web_app_url" {
  description = "HTTPS URL of the Web App."
  value       = "https://${azurerm_linux_web_app.hospital.default_hostname}"
}
