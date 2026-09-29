from django.urls import path
from core import views as v

urlpatterns = [
    path("", v.index),
    path("api/maintenance/", v.maintenance),
    path("api/session/", v.session),
    path("api/auth/register/", v.register),
    path("api/auth/login/", v.sign_in),
    path("api/auth/logout/", v.sign_out),
    path("api/auth/verify/", v.verify_email),
    path("api/auth/resend/", v.resend_verification),
    path("api/auth/reset/", v.reset_request),
    path("api/auth/reset-confirm/", v.reset_confirm),
    path("api/auth/password/", v.password_change),
    path("api/preferences/", v.preferences),
    path("api/clients/", v.client_list),
    path("api/clients/<uuid:pk>/", v.client_detail),
    path("api/clients/<uuid:pk>/visits/", v.visit_create),
    path("api/clients/<uuid:pk>/photos/", v.photo_create),
    path("api/photos/<uuid:pk>/", v.photo_detail),
    path("api/export/", v.export_data),
]
