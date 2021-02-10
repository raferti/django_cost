def cart(request):
    return {'cart': request.session.get('prod_id', [])}