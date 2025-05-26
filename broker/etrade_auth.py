# broker/etrade_auth.py

import json
from pathlib import Path
from rauth import OAuth1Service
from config_loader import get_config

def get_etrade_session():
    """
    Return an OAuth1 session authenticated with E*TRADE.
    - Loads consumer_key/secret and base_url from config.yaml.
    - Reads saved tokens from oauth_token_path, or runs the PIN-based flow.
    """
    # 1. Load config
    cfg = get_config()
    et_cfg = cfg["etrade"]
    base_url = et_cfg["base_url"].rstrip("/")
    ck = et_cfg["consumer_key"]
    cs = et_cfg["consumer_secret"]
    token_file = Path(et_cfg["oauth_token_path"])

    # 2. Build the OAuth1Service
    service = OAuth1Service(
        name="etrade",
        consumer_key=ck,
        consumer_secret=cs,
        request_token_url=f"{base_url}/oauth/request_token",
        authorize_url=f"{base_url}/oauth/authorize",
        access_token_url=f"{base_url}/oauth/access_token",
        base_url=base_url  # for future REST calls (e.g., /v1/accounts)
    )

    # 3. Load or fetch tokens
    if token_file.exists():
        data = json.loads(token_file.read_text())
        oauth_token = data["oauth_token"]
        oauth_token_secret = data["oauth_token_secret"]
    else:
        # 3a. Obtain request token
        req_token, req_token_secret = service.get_request_token(
            method="POST", params={"oauth_callback": "oob"}
        )
        # 3b. Direct user to authorize
        auth_url = service.get_authorize_url(req_token)
        print(f"Go to this URL and authorize the app:\n\n  {auth_url}\n")
        verifier = input("Enter the PIN provided by E*TRADE: ").strip()
        # 3c. Exchange for access token
        oauth_token, oauth_token_secret = service.get_access_token(
            method="POST",
            request_token=req_token,
            request_token_secret=req_token_secret,
            params={"oauth_verifier": verifier}
        )
        # 3d. Save for future runs
        token_file.write_text(json.dumps({
            "oauth_token": oauth_token,
            "oauth_token_secret": oauth_token_secret
        }))

    # 4. Return an authorized session
    session = service.get_session((oauth_token, oauth_token_secret))
    return session
