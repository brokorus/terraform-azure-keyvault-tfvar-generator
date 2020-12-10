<h1 align="center">

Welcome to terraform-azure-keyvault-tfvar-generator 👋

</h1>
<p>
<img alt="Version" src="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000" />

<a href="https://github.com/brokorus/terraform-azure-keyvault-tfvar-generator/graphs/commit-activity" target="_blank"><img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
<a href="None" target="_blank"><img alt="License:MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>

</p>

> Create a terraform.tfvars.json from variables stored in Azure Key Vault. Instead of failing, variables that do not have a value either defined in the variables.tf by default or in Azure Key Vault get a value of NOVALUEFOUND



## Usage
```sh
python3 main.py -i variables.tf -o terraform.tfvars.json -k mykeyvaul -t vault

```


## Author
👤 **Tyler Walker**


* GitHub: [@brokorus](https://github.com/{github_username})
* LinkedIn: [@tyler-walker-9b8605122](https://linkedin.com/in/{author_linkedin_username})




## Show your support
Give a ⭐️ if this project helped you!



---
_This README was created with the [markdown-readme-generator](https://github.com/pedroermarinho/markdown-readme-generator)_
