data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "hospital" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location

  tags = {
    project     = "hospital-management-demo"
    environment = var.environment
    managed_by  = "terraform"
  }
}

resource "azurerm_service_plan" "hospital" {
  name                = "asp-${var.project_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.hospital.name
  location            = azurerm_resource_group.hospital.location
  os_type             = "Linux"
  sku_name            = var.app_service_sku

  tags = azurerm_resource_group.hospital.tags
}

resource "azurerm_linux_web_app" "hospital" {
  name                = "${var.project_name}-${var.environment}-${substr(md5(data.azurerm_client_config.current.subscription_id), 0, 6)}"
  resource_group_name = azurerm_resource_group.hospital.name
  location            = azurerm_resource_group.hospital.location
  service_plan_id     = azurerm_service_plan.hospital.id
  https_only          = true

  site_config {
    always_on = false

    application_stack {
      python_version = "3.12"
    }

    minimum_tls_version = "1.2"
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE"       = "1"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  tags = azurerm_resource_group.hospital.tags
}
