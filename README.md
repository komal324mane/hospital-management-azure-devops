# Hospital Management System — Azure + Terraform + GitHub Actions

A learning/portfolio project for an Azure DevOps Engineer. It contains:
- A small demo hospital appointment web application (Flask; in-memory demo data only).
- Terraform code to provision an Azure Resource Group, Linux App Service Plan, and Linux Web App.
- GitHub Actions CI to test the app and validate Terraform automatically on pushes and pull requests.

**Learning demo only:** Do not enter real patient data or use this for real medical operations. Appointment data is held in memory and resets when the process restarts. This starter does not provision a database.

## Project structure

```text
hospital-management-azure-devops/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── test_app.py
│   └── templates/index.html
├── terraform/
│   ├── versions.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
└── .github/workflows/ci.yml
```

## 1. Run the demo app locally (Windows / PowerShell)

From the project root:

```powershell
cd app
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again.

Run tests:

```powershell
python -m unittest -v
```

## 2. Validate Terraform locally

From the project root:

```powershell
cd terraform
terraform fmt -recursive
terraform init -backend=false
terraform validate
```

These commands do not create Azure resources.

## 3. Create a new GitHub repository and push this new project

Create an empty repository named `hospital-management-azure-devops`. Keep it private while learning if unsure. Open PowerShell in the extracted project root:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "Initial hospital management Terraform project"
git remote add origin https://github.com/YOUR-USERNAME/hospital-management-azure-devops.git
git push -u origin main
```

Replace `YOUR-USERNAME`. Review `git status` before committing. Never commit `.tfstate`, credentials, real patient information, `.env`, or `terraform.tfvars`.

## 4. Automatic GitHub Actions pipeline

`.github/workflows/ci.yml` runs on pushes to `main`, pull requests targeting `main`, and manual workflow dispatch. It:
1. Runs Python unit tests.
2. Checks Terraform formatting.
3. Initializes Terraform without a backend.
4. Validates Terraform configuration.

After pushing, open the repository → **Actions** to see the run. This workflow does not sign in to Azure or create cloud resources.

## 5. Optional: provision Azure infrastructure (may incur charges)

First sign in:

```powershell
az login
az account show
```

Copy `terraform.tfvars.example` to `terraform.tfvars` and set your subscription ID. `terraform.tfvars` is ignored by Git. From the `terraform` directory:

```powershell
terraform init
terraform plan -out main.tfplan
terraform apply main.tfplan
```

Review the plan carefully. App Service resources can incur charges. To remove resources created by this project:

```powershell
terraform destroy
```

Only destroy resources you know belong to this project and no longer need.

### Azure authentication and deployment

Local Terraform can use your Azure CLI login through AzureRM. GitHub Actions CI does not authenticate to Azure and does not deploy infrastructure. Before automated cloud deployment, configure Microsoft Entra workload identity federation (OIDC), a GitHub federated credential, and least-privilege Azure permissions. Add remote Terraform state and approval controls before enabling deployment. Never place client secrets in source code.

## Suggested next enhancements

- Add Azure Storage remote backend for Terraform state and locking.
- Add GitHub OIDC and a manual, approval-protected deployment workflow.
- Deploy the Flask application to Azure App Service.
- Add Azure SQL Database only after reviewing networking, secrets, backups, and cost.
- Add Application Insights monitoring.
- Add proper authentication, authorization, and security controls before any real-world use.

## Interview explanation

“I built a sample Hospital Management System as a DevOps portfolio project. Terraform defines the Azure infrastructure, while GitHub Actions automatically tests the Python application and validates Terraform on each push and pull request. CI does not deploy resources automatically, which avoids accidental cloud costs. The next phase is secure OIDC-based deployment and remote Terraform state.”
