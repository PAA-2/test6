from fastapi import FastAPI

from app.api.routes import (
    auth,
    users,
    projects,
    files,
    notifications,
    analytics,
    tasks,
    search,
    orgs,
    me_org,
    invites,
    public_api,
    dev_portal,
    password_reset,
    health_ext,
)
from app.feature_flags import routers as feature_flags_router
from app.settings import routers as settings_router
from app.observability.logging import (
    RequestLoggingMiddleware,
    configure_logging,
)
from app.observability.metrics import MetricsMiddleware, router as metrics_router
from app.observability.tracing import init_tracing
from app.core.security_hardening.csp_headers import CSPMiddleware
from app.core.security_hardening.payload_limits import PayloadLimitMiddleware
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
configure_logging()

app = FastAPI()
init_tracing(app)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(CSPMiddleware)
app.add_middleware(PayloadLimitMiddleware, max_body=2 * 1024 * 1024)

app.include_router(metrics_router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(files.router)
app.include_router(notifications.router)
app.include_router(analytics.router)
app.include_router(tasks.router)
app.include_router(search.router)
app.include_router(orgs.router)
app.include_router(invites.router)
app.include_router(me_org.router)
app.include_router(public_api.router)
app.include_router(dev_portal.router)
app.include_router(password_reset.router)
app.include_router(feature_flags_router.router)
app.include_router(settings_router.router)
app.include_router(health_ext.router)
