class PrivateResponses:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        length = request.META.get("CONTENT_LENGTH", "")
        if length.isdigit() and int(length) > 4 * 1024 * 1024:
            from django.http import JsonResponse

            return JsonResponse({"error": "invalid_photo"}, status=413)
        response = self.get_response(request)
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "no-referrer"
        response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if not request.path.startswith("/static/"):
            response["Cache-Control"] = "no-store, private"
        return response
