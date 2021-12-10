# cioos-dashboards

The three jupyter notebooks outline three dashboards which also require the png file to run.

First a conda environment can be created using the environment.yml file
```bash
conda env create -f environment.yml
```
Once an environment is created, a dashboard, or multiple dashboards can be launched using the CLI command,
```bash
panel serve FORCE_dashboardv1.ipynb CMAR_dashboardv3.ipynb HurricaneLarryDashboard.ipynb --index "\path\to\index\cioos-dashboards\index.html" 
```
Additionally serving with --index gives the ability to specify a template to be used for the site's index.
The panel serve command has the following options:
```bash
positional arguments:
  DIRECTORY-OR-SCRIPT   The app directories or scripts or notebooks to serve 
                        (serve empty document if not specified)

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           Port to listen on
  --address ADDRESS     Address to listen on
  --log-level LOG-LEVEL
                        One of: trace, debug, info, warning, error or critical
  --log-format LOG-FORMAT
                        A standard Python logging format string (default:
                        '%(asctime)s %(message)s')
  --log-file LOG-FILE   A filename to write logs to, or None to write to the
                        standard stream (default: None)
  --args ...            Any command line arguments remaining are passed on to
                        the application handler
  --show                Open server app(s) in a browser
  --allow-websocket-origin HOST[:PORT]
                        Public hostnames which may connect to the Bokeh
                        websocket
  --prefix PREFIX       URL prefix for Bokeh server URLs
  --keep-alive MILLISECONDS
                        How often to send a keep-alive ping to clients, 0 to
                        disable.
  --check-unused-sessions MILLISECONDS
                        How often to check for unused sessions
  --unused-session-lifetime MILLISECONDS
                        How long unused sessions last
  --stats-log-frequency MILLISECONDS
                        How often to log stats
  --mem-log-frequency MILLISECONDS
                        How often to log memory usage information
  --use-xheaders        Prefer X-headers for IP/protocol information
  --auth-module AUTH_MODULE
                        Absolute path to a Python module that implements auth hooks
  --enable-xsrf-cookies
                        Whether to enable Tornado support for XSRF cookies.
                        All PUT, POST, or DELETE handlers must be properly
                        instrumented when this setting is enabled.
  --exclude-headers EXCLUDE_HEADERS [EXCLUDE_HEADERS ...]
                        A list of request headers to exclude from the session
                        context (by default all headers are included).
  --exclude-cookies EXCLUDE_COOKIES [EXCLUDE_COOKIES ...]
                        A list of request cookies to exclude from the session
                        context (by default all cookies are included).
  --include-headers INCLUDE_HEADERS [INCLUDE_HEADERS ...]
                        A list of request headers to make available in the
                        session context (by default all headers are included).
  --include-cookies INCLUDE_COOKIES [INCLUDE_COOKIES ...]
                        A list of request cookies to make available in the
                        session context (by default all cookies are included).
  --session-ids MODE    One of: unsigned, signed, or external-signed
  --index INDEX         Path to a template to use for the site index
  --disable-index       Do not use the default index on the root path
  --disable-index-redirect
                        Do not redirect to running app from root path
  --default-app FILENAME
                        The app to redirect to from the root. When enabled
                        no index is served.
  --num-procs N         Number of worker processes for an app. Using 0 will
                        autodetect number of cores (defaults to 1)
  --warm                Whether to execute scripts on startup to warm up the server.
  --autoreload
                        Whether to automatically reload user sessions when the application or any of its imports change.
  --static-dirs KEY=VALUE [KEY=VALUE ...]        
                        Static directories to serve specified as key=value
                        pairs mapping from URL route to static file directory.

  --dev [FILES-TO-WATCH [FILES-TO-WATCH ...]]
                        Enable live reloading during app development.By
                        default it watches all *.py *.html *.css *.yaml
                        filesin the app directory tree. Additional files can
                        be passedas arguments. NOTE: This setting only works
                        with a single app.It also restricts the number of
                        processes to 1.
  --session-token-expiration N
                        Duration in seconds that a new session token is valid
                        for session creation. After the expiry time has elapsed,
                        the token will not be able create a new session
                        (defaults to seconds).
  --websocket-max-message-size BYTES
                        Set the Tornado websocket_max_message_size value
                        (defaults to 20MB) NOTE: This setting has effect ONLY
                        for Tornado>=4.5
  --websocket-compression-level LEVEL
                        Set the Tornado WebSocket compression_level
  --websocket-compression-mem-level LEVEL
                        Set the Tornado WebSocket compression mem_level
  --oauth-provider OAUTH_PROVIDER
                        The OAuth2 provider to use.
  --oauth-key OAUTH_KEY
                        The OAuth2 key to use
  --oauth-secret OAUTH_SECRET
                        The OAuth2 secret to use
  --oauth-redirect-uri OAUTH_REDIRECT_URI
                        The OAuth2 redirect URI
  --oauth-extra-params OAUTH_EXTRA_PARAMS
                        Additional parameters to use.
  --oauth-jwt-user OAUTH_JWT_USER
                        The key in the ID JWT token to consider the user.
  --oauth-encryption-key OAUTH_ENCRYPTION_KEY
                        A random string used to encode the user information.
  --rest-provider REST_PROVIDER
                        The interface to use to serve REST API
  --rest-endpoint REST_ENDPOINT
                        Endpoint to store REST API on.
  --rest-session-info   
                        Whether to serve session info on the REST API
  --session-history SESSION_HISTORY
                        The length of the session history to record.
```
Additional information on deployment can be found at https://panel.holoviz.org/user_guide/Deploy_and_Export.html
