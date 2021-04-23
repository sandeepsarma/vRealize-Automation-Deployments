## vRealize Automation version 7.5 - deployments report generator

A complex vRealize Automation environment can have hundreds of catalog items, that are either automatically kicked of by vRealize orchestrator, or by a user that has access to the catalog item. This simple report generates a list of all initiated deployments and their deployment status. 

The deployments report Excel file has has the following columns : `Deployment_Name`, `Submitted_Date`, `Requested_By`, `Requested_For`, `Deployment ID` and `Deployment State`

A sample output report can be [found here](https://github.com/rundotpy/vRealize-Automation-Deployments-Report/tree/main/sample-report)

## Required input data

```python
# File name : appvars.py
# Update the following data - 

# vRealize Automation Server URL :
vra_prod_fqdn = '<Insert-VRA-FQDN-Here>'
# vRealuze Automation Tenant Name :
vra_prod_tenant_name = '<Insert-VRA-Tenant-Name-Here>'
# vRealuze Automation Admin Credentials :
# Please use environment variables to save this info : 
vra_prod_admin = "<vRA-Admin>"
vra_prod_passw = "<vRA-Admin>"

```

## Usage
```python
(.venv) python app.py
VRA Authentication Successful and will be valid until : 2021-04-20T23:35:23.000Z
Total Number of Deployments :  2124
Total Number of Deployments spanned across pages :  22
Deployment reported saved as : vRealize-DeploymentsReport-20-Apr-2021-11-36-36.xlsx
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
