# Infrastructure

Setup the necessary infrastructures.

```text
├── main.tf                 # This file references other components and serves as the entry point for running the Terraform configuration.
├── providers.tf            # This file defines the PostgreSQL provider configuration.
├── settings.tf             # This file contains the resources for creating the database, user, and granting permissions.
├── variables.tf            # This file defines the variables used in the configuration.
└── terraform.tfvars        # This file is used to store sensitive values.
```

## Prerequisites

* [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli#install-cli)

## Setup

1. Copy `terraform.tfvars.example` as `terraform.tfvars` and update the credentials

    ```bash
    cp terraform.tfvars.example terraform.tfvars
    ```

2. Initialize the project

    ```bash
    terraform init
    ```

    ![image](https://github.com/user-attachments/assets/742b3605-3f17-4d8c-b9c6-f45573d8a4df)

3. Apply the changes

    ```bash
    terraform apply
    ```

    ![image](https://github.com/user-attachments/assets/cc23f2ff-95e5-4e85-bdad-1e8fe78dec36)

> This creates the `vyaguta_db` database locally with `vyaguta_user` with admin role.
