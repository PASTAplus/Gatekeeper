# PASTA Gatekeeper

The PASTA Gatekeeper service is the public facing entry point for access to the
more general services of the PASTA data repository. The Gatekeeper acts as 
both an authentication service and a reverse proxy.

As an authentication service, the Gatekeeper consumes either a standard
*authorization* header using the *Basic* scheme or a custom PASTA authentication
token set as a Cookie using the *auth-token* key. See
[here](https://pastaplus-core.readthedocs.io/en/latest/doc_tree/pasta_design/gatekeeper.html) for more 
information about the PASTA Gatekeeper.

As a reverse proxy, the Gatekeeper routes requests to either the Data Package
Manager service or the Audit Manager service.

The Gatekeeper service is the first of the PASTA primary services to migrate
from a Java servlet model to a Python framework based on the high-performance
and asynchronous *FastAPI*.

![Gatekeeper](https://github.com/PASTAplus/Gatekeeper/actions/workflows/gatekeeper-build.yml/badge.svg?branch=main) - Main

![Gatekeeper](https://github.com/PASTAplus/Gatekeeper/actions/workflows/gatekeeper-build.yml/badge.svg?branch=staging) - Staging

![Gatekeeper](https://github.com/PASTAplus/Gatekeeper/actions/workflows/gatekeeper-build.yml/badge.svg?branch=development) - Development
