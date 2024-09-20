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

1. Initialize the project

```bash
 terraform init
```

2. Apply the changes

```bash
 terraform apply
```

> This will create the `vyaguta_db` database locally with `vyaguta_user` with admin role.
