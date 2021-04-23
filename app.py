import vrealizeautomation.vra as vrealize_automation
import appvars

# Create an instance of the vraauthentication class.
my_vra = vrealize_automation.vraauthentication(appvars.vra_prod_fqdn, 
                                               appvars.vra_prod_tenant_name,
                                               appvars.vra_prod_admin,
                                               appvars.vra_prod_passw)

# Request the bearer token.
# call, get_vra_bearer_token -
# Returns True, and updates value - self.vra_bearer_token
if my_vra.get_vra_bearer_token():
    # Get the deployments details :
    my_vra.obtain_deployments_info()

else:
    print("app.py terminated, as there was an issue authenticating to vRealize Automation platform")
